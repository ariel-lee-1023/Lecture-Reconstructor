"""Isolated package faults, independent of the work-in-progress repo contents."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('validate_repo',ROOT/'scripts/validate_repo.py')
validator=importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class RepoTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        for rel in validator.REQUIRED:
            p=self.root/rel; p.parent.mkdir(parents=True,exist_ok=True);p.write_text('Substantive fixture.\n')
        for rel, target in validator.ALIASES.items():
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.symlink_to(target, target_is_directory=rel.startswith('.agents/'))
        routes = [f'[{name}]({name})' for name in [*validator.METHODS, 'WORKFLOW.md']]
        (self.root/'SKILL.md').write_text(
            '---\nname: lecture-reconstructor\ndescription: Reconstruct a supplied transcript into a lecture.\n---\n'
            '\nTeach the supplied class.\n\n## Loading depth (host-agent note)\n' + '\n'.join(routes) + '\n'
        )
        (self.root/'evals/cases').mkdir()
        (self.root/'evals/cases/input.md').write_text('Synthetic transcript: a permission need not impose a duty.\n')
        self.manifest={'schema_version':'1.0','sources':[]}
        for repo in sorted(validator.EXPECTED_SOURCES):
            self.manifest['sources'].append({'repo':repo,'head':'unknown','role':'adaptation','files':[{'path':'LICENSE','sha256':'a'*64,'worktree_status':'clean','sections':['full MIT notice'],'destinations':['LICENSE','NOTICE.md'],'adaptation':'Preserve attribution.'},{'path':'SKILL.md','sha256':'b'*64,'worktree_status':'clean','sections':['selected methods'],'destinations':validator.METHODS,'adaptation':'Adapt selected mechanisms to lecture writing.'}]})

    def validate(self):
        (self.root/'fidelity-ledger/source-manifest.json').write_text(json.dumps(self.manifest))
        return validator.validate_repo(self.root)

    def rejects(self,code):
        result=self.validate();self.assertIn(code,[x['code'] for x in result['errors']],result)

    def test_valid_package(self):
        self.assertEqual(0,self.validate()['exit_code'])

    def test_missing_runtime(self):
        (self.root / validator.METHODS[0]).unlink()
        self.rejects('REQUIRED_FILE')
        self.rejects('BROKEN_LINK')

    def test_discovery_alias_is_required(self):
        (self.root / '.agents/skills/lecture-reconstructor').unlink()
        self.rejects('PACKAGE_ALIAS')

    def test_legacy_copy_is_not_an_alias(self):
        path = self.root / 'references/law-reasoning.md'
        content = path.read_bytes()
        path.unlink()
        path.write_bytes(content)
        self.rejects('PACKAGE_ALIAS')

    def test_legacy_path_cannot_replace_canonical_route(self):
        skill = self.root / 'SKILL.md'
        method = validator.METHODS[0]
        skill.write_text(skill.read_text().replace(f']({method})', '](references/teaching-design.md)'))
        self.rejects('MISSING_ROUTE')

    def test_workflow_links_use_canonical_directory(self):
        workflow = self.root / 'WORKFLOW.md'
        workflow.write_text('[Methods](references/reference-teaching-design.md)')
        self.assertEqual(0, self.validate()['exit_code'])
        workflow.write_text('Read `/srv/private/workflow.md`.')
        self.rejects('RUNTIME_ABSOLUTE_PATH')

    def test_legacy_source_manifest_destinations(self):
        for source in self.manifest['sources']:
            source['files'][1]['destinations'] = [
                'references/teaching-design.md', 'references/law-reasoning.md', 'references/transcript-repair.md'
            ]
        self.assertEqual(0, self.validate()['exit_code'])

    def test_absolute_runtime_dependency(self):
        (self.root/'references/teaching-design.md').write_text('Read `/Users/example/private/SKILL.md`.')
        self.rejects('RUNTIME_ABSOLUTE_PATH')

    def test_other_absolute_roots_without_url_or_anchor_false_positive(self):
        path=self.root/'references/teaching-design.md'
        for absolute in ('/srv/shared/method.md','/Applications/Tool/app','/custom-root/file.txt'):
            path.write_text('Read `'+absolute+'`.')
            self.rejects('RUNTIME_ABSOLUTE_PATH')
        path.write_text('Source https://example.com/a/b and <a id="chapter"></a>. Use `../schemas/run.schema.json` and `.work/<run-id>/run.json`.')
        self.assertEqual(0,self.validate()['exit_code'])

    def test_sibling_link(self):
        (self.root/'references/teaching-design.md').write_text('[Sibling](../../other/SKILL.md)')
        self.rejects('RUNTIME_EXTERNAL_LINK')

    def test_excluded_dependency(self):
        (self.root/'references/law-reasoning.md').write_text('load prc-legal-sources')
        self.rejects('EXCLUDED_DEPENDENCY')

    def test_exclusion_in_prose_and_engineering_doc_is_allowed(self):
        # Escaped Unicode preserves the original non-English regression coverage.
        (self.root/'references/law-reasoning.md').write_text("\u4e0d\u4f9d\u8d56 prc-legal-sources\u3002")
        (self.root/'plan.md').write_text("\u68c0\u67e5\u6392\u9664 prc-legal-sources\u3002\u5386\u53f2\u7edd\u5bf9\u8def\u5f84 /Users/example/source\u3002")
        self.assertEqual(0,self.validate()['exit_code'])

    def test_manifest_personal_path(self):
        self.manifest['sources'][0]['local_root']='/Users/example/private'
        self.rejects('MANIFEST_LOCAL_PATH')

    def test_manifest_missing_source_identity(self):
        self.manifest['sources'][0]['files'][0]['sha256']='unknown'
        self.rejects('MANIFEST_HASH')

    def test_manifest_source_missing(self):
        self.manifest['sources'].pop()
        self.rejects('MANIFEST_SOURCE')

    def test_readme_broken_link(self):
        (self.root/'README.md').write_text('[Missing](docs/not-here.md)')
        self.rejects('BROKEN_LINK')

    def test_frontmatter_required(self):
        (self.root/'SKILL.md').write_text('# No metadata\n')
        self.rejects('FRONTMATTER')


if __name__=='__main__':
    unittest.main()
