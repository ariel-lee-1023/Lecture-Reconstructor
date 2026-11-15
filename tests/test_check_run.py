"""Executable normal and fault records; synthetic teaching-only material."""
from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('check_run', ROOT / 'scripts/check_run.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def build_fixture(base):
    """Create a valid complete record and actual files in an isolated directory."""
    base = Path(base)
    repo = base / 'package'
    run_dir = base / 'run'
    repo.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)
    (repo / 'references').mkdir(exist_ok=True)
    (repo / 'SKILL.md').write_text('Synthetic runtime fixture.\n', encoding='utf-8')
    (repo / 'references/method.md').write_text('Explain the changed condition.\n', encoding='utf-8')
    (run_dir / 'input.txt').write_text('合成规则：许可仅允许进入阅览室。\n许可不使保管员负有递书义务。\n', encoding='utf-8')
    lecture = '<a id="c1"></a>\n# 许可与义务\n\n以下是合成规则的教学解释。获准进入意味着进入不被禁止；它没有授予要求保管员递书的请求权。因此，单凭许可不能推出他人负有递书义务。\n'
    (run_dir / 'chapter.md').write_text(lecture, encoding='utf-8')
    (run_dir / 'lecture.md').write_text(lecture, encoding='utf-8')
    (run_dir / 'review.md').write_text('合成机械夹具评审证据：两项规则都有去向。这不是模型行为测试。\n', encoding='utf-8')
    data = {
        'schema_version':'1.0','run_id':'synthetic-fixture','status':'complete','stage':'deliver',
        'course':{'title':'许可与义务','scope':'两项合成规则','jurisdiction':'fictional','time_context':'unknown','audience':'大学生','assumptions':[]},
        'inputs':[{'id':'i1','path':'input.txt','sha256':checker.sha256(run_dir/'input.txt'),'kind':'synthetic_transcript','normalized_path':'input.txt','normalized_sha256':checker.sha256(run_dir/'input.txt')}],
        'source_review':[{'input_id':'i1','start_line':1,'end_line':2,'status':'reviewed'}],
        'content_units':[{'id':'u1','proposition':'进入许可不推出递书义务','locations':[{'input_id':'i1','start_line':1,'end_line':2}],'type':'concept','status':'represented','reason':'正文解释条件与推论','targets':[{'chapter_id':'c1','anchor':'c1'}],'source_ids':[]}],
        'sources':[], 'chapters':[{'id':'c1','path':'chapter.md','anchor':'c1','status':'assembled','learning_object':'许可和请求权','relations':['行为被允许与他人有义务的区别'],'prerequisites':[],'approach':'解释两项合成规则','role':'全课','content_unit_ids':['u1']}],
        'terms':[{'term':'许可','decision':'指进入行为被允许'}], 'open_issues':[],
        'runtime_revision':{'files':[{'path':p,'sha256':checker.sha256(repo/p)} for p in ['SKILL.md','references/method.md']],'host':'unknown','model':'unknown','settings':{}},
        'checks':[{'id':'s1','kind':'semantic','scope':'full_manuscript','status':'pass','method':'机械夹具，不是独立实际行为评审','evidence':'review.md','date':'2026-11-15','output_sha256':checker.sha256(run_dir/'lecture.md')}],
        'revision_round':0,'output':{'path':'lecture.md'},'resume':{'completed':['c1'],'remaining':[],'next_action':'deliver'}
    }
    (run_dir/'run.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return data, run_dir, repo


class RunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data, self.run, self.repo = build_fixture(self.temp.name)

    def validate(self):
        (self.run/'run.json').write_text(json.dumps(self.data,ensure_ascii=False),encoding='utf-8')
        return checker.validate_run(self.run/'run.json',self.repo)

    def rejects(self, code):
        result=self.validate()
        self.assertIn(code,[e['code'] for e in result['errors']], result)
        return result

    def test_complete_fixture(self):
        self.assertEqual(0,self.validate()['exit_code'])

    def test_dangling_id(self):
        self.data['content_units'][0]['targets'][0]['chapter_id']='missing'
        self.rejects('DANGLING_ID')

    def test_duplicate_ids(self):
        self.data['content_units'].append(copy.deepcopy(self.data['content_units'][0]))
        self.rejects('DUPLICATE_ID')

    def test_merge_cycle(self):
        unit=self.data['content_units'][0]
        unit.update(status='merged',merge_into='u2')
        other=copy.deepcopy(unit); other.update(id='u2',merge_into='u1')
        self.data['content_units'].append(other)
        self.data['chapters'][0]['content_unit_ids'].append('u2')
        self.rejects('MERGE_CYCLE')

    def test_out_of_bounds(self):
        self.data['content_units'][0]['locations'][0]['end_line']=3
        self.rejects('RANGE')

    def test_negative_and_bool_bounds(self):
        self.data['source_review'][0]['start_line']=True
        self.rejects('RANGE')

    def test_missing_chapter_anchor(self):
        (self.run/'chapter.md').write_text('# Missing stable anchor\n')
        self.rejects('MISSING_ANCHOR')

    def test_missing_output_anchor(self):
        (self.run/'lecture.md').write_text('# Missing stable anchor\n')
        self.rejects('MISSING_OUTPUT_ANCHOR')

    def test_changed_input_requires_review(self):
        (self.run/'input.txt').write_text('新规则\n')
        self.assertEqual(2,self.rejects('INPUT_CHANGED')['exit_code'])

    def test_changed_core_requires_review(self):
        (self.repo/'SKILL.md').write_text('changed')
        self.assertEqual(2,self.rejects('RUNTIME_CHANGED')['exit_code'])

    def test_changed_reference_requires_review(self):
        before=checker.sha256(self.run/'input.txt')
        (self.repo/'references/method.md').write_text('changed')
        self.assertEqual(2,self.rejects('RUNTIME_CHANGED')['exit_code'])
        self.assertEqual(before,checker.sha256(self.run/'input.txt'))

    def test_missing_semantic_review(self):
        self.data['checks']=[]
        self.rejects('MISSING_SEMANTIC_REVIEW')

    def test_later_failed_review_supersedes_pass(self):
        failed=copy.deepcopy(self.data['checks'][0]); failed.update(id='s2',status='fail')
        self.data['checks'].append(failed)
        self.rejects('MISSING_SEMANTIC_REVIEW')

    def test_historical_review_preserved_after_manuscript_revision(self):
        old_hash=self.data['checks'][0]['output_sha256']
        (self.run/'lecture.md').write_text((self.run/'lecture.md').read_text()+'\n补足已复核的解释。\n')
        current=copy.deepcopy(self.data['checks'][0])
        current.update(id='s2',output_sha256=checker.sha256(self.run/'lecture.md'))
        self.data['checks'].append(current)
        self.assertEqual(0,self.validate()['exit_code'])
        self.assertEqual(old_hash,self.data['checks'][0]['output_sha256'])
        current['output_sha256']=old_hash
        self.rejects('STALE_REVIEW')
        for state in ('fail','not_run'):
            current['status']=state
            self.rejects('MISSING_SEMANTIC_REVIEW')

    def test_not_run_review(self):
        self.data['checks'][0]['status']='not_run'
        self.rejects('MISSING_SEMANTIC_REVIEW')

    def test_stale_semantic_review(self):
        (self.run/'lecture.md').write_text((self.run/'lecture.md').read_text()+'新的一段。\n')
        self.rejects('STALE_REVIEW')

    def test_missing_evidence(self):
        (self.run/'review.md').unlink()
        self.rejects('MISSING_SEMANTIC_REVIEW')

    def test_empty_evidence(self):
        (self.run/'review.md').write_text('')
        self.rejects('EMPTY_EVIDENCE')

    def test_planned_missing_file_and_anchor_allowed(self):
        self.data.update(status='partial',stage='plan')
        self.data['chapters'][0].update(status='planned',path='not-yet.md')
        self.data['checks']=[]
        self.data['output']['path']='not-yet-lecture.md'
        self.data['resume'].update(completed=[],remaining=['c1'],next_action='write c1')
        self.assertEqual(0,self.validate()['exit_code'])

    def test_needs_review_missing_file_requires_reason(self):
        self.data.update(status='partial',stage='draft')
        self.data['chapters'][0].update(status='needs_review',path='missing.md',missing_reason='input changed; previous draft absent')
        self.data['checks']=[]
        self.assertEqual(0,self.validate()['exit_code'])
        del self.data['chapters'][0]['missing_reason']
        self.rejects('VALUE')

    def test_complete_rejects_planned(self):
        self.data['chapters'][0]['status']='planned'
        self.rejects('INCOMPLETE_CHAPTER')

    def test_complete_rejects_blocking_content(self):
        self.data['content_units'][0].update(status='unresolved',blocking=True,blocking_reason='核心术语不明')
        self.rejects('BLOCKING_CONTENT')

    def test_complete_rejects_blocking_issue(self):
        self.data['open_issues']=[{'id':'q1','question':'规则含义?','impact':'结论改变','resolution_condition':'原音核对','status':'open','blocking':True,'blocking_reason':'核心条件未知'}]
        self.rejects('BLOCKING_ISSUE')

    def test_unread_and_untracked_ranges(self):
        self.data['source_review'][0]['status']='unread'
        self.rejects('UNREVIEWED_RANGE')
        self.data['source_review']=[]
        self.rejects('UNTRACKED_RANGE')

    def test_empty_input_can_need_input(self):
        self.data.update(status='needs_input',stage='ingest',inputs=[],source_review=[],content_units=[],chapters=[],checks=[])
        self.assertEqual(0,self.validate()['exit_code'])
        self.data.update(status='complete',stage='deliver')
        self.rejects('EMPTY_INPUT')

    def test_path_escape(self):
        self.data['output']['path']='../escape.md'
        self.rejects('PATH')

    def test_malformed_structure_reports_instead_of_crashing(self):
        for key in list(self.data):
            data=copy.deepcopy(self.data)
            with self.subTest(key=key):
                self.data[key]=None
                result=self.validate()
                self.assertNotEqual(0,result['exit_code'])
            self.data=data

    def test_cli_codes_and_locator(self):
        self.data['content_units'][0]['locations'][0]['end_line']=99
        self.validate()
        result=subprocess.run([sys.executable,str(ROOT/'scripts/check_run.py'),str(self.run/'run.json'),'--repo-root',str(self.repo),'--json'],capture_output=True,text=True)
        self.assertEqual(1,result.returncode)
        self.assertIn('content_units[0].locations[0]',result.stdout)


if __name__=='__main__':
    unittest.main()
