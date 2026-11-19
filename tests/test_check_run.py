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
    (run_dir / 'input.txt').write_text("Synthetic rule: permission only allows entry to the reading room.\nPermission does not impose a duty on the custodian to hand over books.\n", encoding='utf-8')
    lecture = "<a id=\"c1\"></a>\n# Permission and duty\n\nThis is a teaching explanation of synthetic rules. Permission to enter means entry is not prohibited; it does not confer a claim-right to have the custodian hand over books. Permission alone therefore does not entail another person's duty to hand over books.\n"
    (run_dir / 'chapter.md').write_text(lecture, encoding='utf-8')
    (run_dir / 'lecture.md').write_text(lecture, encoding='utf-8')
    (run_dir / 'review.md').write_text("Synthetic mechanical-fixture review evidence: both rules are accounted for. This is not a model behavior test.\n", encoding='utf-8')
    data = {
        'schema_version':'1.0','run_id':'synthetic-fixture','status':'complete','stage':'deliver',
        'course':{'title':"Permission and duty",'scope':"Two synthetic rules",'jurisdiction':'fictional','time_context':'unknown','audience':"University students",'assumptions':[]},
        'inputs':[{'id':'i1','path':'input.txt','sha256':checker.sha256(run_dir/'input.txt'),'kind':'synthetic_transcript','normalized_path':'input.txt','normalized_sha256':checker.sha256(run_dir/'input.txt')}],
        'source_review':[{'input_id':'i1','start_line':1,'end_line':2,'status':'reviewed'}],
        'content_units':[{'id':'u1','proposition':"Permission to enter does not entail a duty to hand over books",'locations':[{'input_id':'i1','start_line':1,'end_line':2}],'type':'concept','status':'represented','reason':"The manuscript explains conditions and inference",'targets':[{'chapter_id':'c1','anchor':'c1'}],'source_ids':[]}],
        'sources':[], 'chapters':[{'id':'c1','path':'chapter.md','anchor':'c1','status':'assembled','learning_object':"Permission and claim-rights",'relations':["The difference between permitted conduct and another person having a duty"],'prerequisites':[],'approach':"Explain two synthetic rules",'role':"The whole course",'content_unit_ids':['u1']}],
        'terms':[{'term':"Permission",'decision':"Means that entry is permitted"}], 'open_issues':[],
        'runtime_revision':{'files':[{'path':p,'sha256':checker.sha256(repo/p)} for p in ['SKILL.md','references/method.md']],'host':'unknown','model':'unknown','settings':{}},
        'checks':[{'id':'s1','kind':'semantic','scope':'full_manuscript','status':'pass','method':"Mechanical fixture, not independent review of actual behavior",'evidence':'review.md','date':'2026-11-15','output_sha256':checker.sha256(run_dir/'lecture.md')}],
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

    def test_complete_primary_text_without_a_transcript(self):
        self.data['inputs'][0]['kind'] = 'course_rule'
        self.data['course']['scope'] = 'Redesigned lesson based on two written rules'
        self.assertEqual(0, self.validate()['exit_code'])

    def test_changed_input_requires_review(self):
        (self.run/'input.txt').write_text("New rule\n")
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
        (self.run/'lecture.md').write_text((self.run/'lecture.md').read_text()+"\nAdd the reviewed explanation.\n")
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
        (self.run/'lecture.md').write_text((self.run/'lecture.md').read_text()+"A new paragraph.\n")
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
        self.data['content_units'][0].update(status='unresolved',blocking=True,blocking_reason="Core terminology is unclear")
        self.rejects('BLOCKING_CONTENT')

    def test_complete_rejects_blocking_issue(self):
        self.data['open_issues']=[{'id':'q1','question':"Meaning of the rule?",'impact':"The conclusion changes",'resolution_condition':"Check the original audio",'status':'open','blocking':True,'blocking_reason':"Core condition unknown"}]
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
