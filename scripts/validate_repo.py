#!/usr/bin/env python3
"""Check package structure and portable source registration, not teaching quality."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

REQUIRED = ['SKILL.md', 'AGENTS.md', 'README.md', 'intent.md', 'spec.md', 'plan.md',
            'LICENSE', 'NOTICE.md', '.gitignore', 'references/teaching-design.md',
            'references/law-reasoning.md', 'references/transcript-repair.md',
            'references/reconstruction-workflow.md', 'schemas/run.schema.json',
            'scripts/validate_repo.py', 'scripts/check_run.py', 'evals/acceptance.md',
            'fidelity-ledger/source-manifest.json', 'fidelity-ledger/validation.md']
RUNTIME = ['SKILL.md', 'references/teaching-design.md', 'references/law-reasoning.md',
           'references/transcript-repair.md', 'references/reconstruction-workflow.md']
EXPECTED_SOURCES = {'indwell-via-shared-discern', 'legal-reasoning-advisor',
                    'transcript-proofreader', 'Models-and-Machines-colleague'}
SHA = re.compile(r'^[0-9a-f]{64}$')
LINK = re.compile(r'(?<!!)\[[^\]\n]+\]\((<[^>\n]+>|[^\s)]+)(?:\s+["\'][^\n]*?["\'])?\)')
ABSOLUTE = re.compile(r'(?<![\w:/<>.~])(?:/[A-Za-z0-9._~-]+(?:/[^\s`<>\)]*)?|[A-Za-z]:[\\/][^\s`<>\)]*|file://[^\s`<>\)]*|~/[^\s`<>\)]*)')


def validate_repo(root):
    root = Path(root).resolve()
    errors = []
    def error(code, at, message):
        errors.append({'code': code, 'at': at, 'message': message})
    def portable(value):
        if not isinstance(value, str) or not value.strip():
            return False
        p = Path(value)
        return not p.is_absolute() and '..' not in p.parts and not re.match(r'^[A-Za-z]:[\\/]', value)
    def exists(rel):
        p = (root / rel).resolve()
        return p.is_relative_to(root) and p.is_file() and p.stat().st_size > 0
    for rel in REQUIRED:
        if not exists(rel):
            error('REQUIRED_FILE', rel, 'missing, empty, or outside package')
    cases = root / 'evals/cases'
    if not cases.is_dir() or not any(p.is_file() and p.stat().st_size for p in cases.rglob('*')):
        error('MISSING_CASES', 'evals/cases', 'requires substantive test inputs')
    skill_path = root / 'SKILL.md'
    skill = skill_path.read_text(encoding='utf-8') if skill_path.is_file() else ''
    front = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', skill, re.S)
    if not front:
        error('FRONTMATTER', 'SKILL.md', 'missing YAML frontmatter')
    else:
        fields = dict(re.findall(r'^([a-z_-]+):\s*(.+)$', front.group(1), re.M))
        if fields.get('name', '').strip('"\'') != 'lecture-reconstructor':
            error('SKILL_NAME', 'SKILL.md', 'expected name: lecture-reconstructor')
        if not fields.get('description', '').strip('"\''):
            error('SKILL_DESCRIPTION', 'SKILL.md', 'nonempty description required')
    for rel in RUNTIME:
        path = root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding='utf-8')
        for match in ABSOLUTE.finditer(text):
            error('RUNTIME_ABSOLUTE_PATH', rel, match.group())
        for raw in LINK.findall(text):
            link = unquote(raw.strip('<>'))
            if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', link):
                if not link.startswith(('http://', 'https://', 'mailto:')):
                    error('RUNTIME_EXTERNAL_SCHEME', rel, link)
                continue
            target = link.split('#', 1)[0].split('?', 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if Path(target).is_absolute() or not resolved.is_relative_to(root):
                error('RUNTIME_EXTERNAL_LINK', rel, link)
            elif not resolved.exists():
                error('BROKEN_LINK', rel, link)
            if 'prc-legal-sources' in target:
                error('EXCLUDED_DEPENDENCY', rel, link)
        # Text explaining that a dependency is excluded is permitted; a load/import
        # directive or concrete path to it is not. Engineering documents are not scanned.
        for line_no, line in enumerate(text.splitlines(), 1):
            if 'prc-legal-sources' not in line:
                continue
            if re.search(r'(?:\.\./|references/|skills/)[^\s`]*prc-legal-sources|prc-legal-sources[/\\]', line):
                error('EXCLUDED_DEPENDENCY', f'{rel}:{line_no}', line)
            elif re.search(r'(?:load|import|require|读取|加载|依赖)\s*[`"\']?prc-legal-sources', line, re.I) and not re.search(r'不|无|排除|禁止|不得|not|never|exclude|without', line, re.I):
                error('EXCLUDED_DEPENDENCY', f'{rel}:{line_no}', line)
    # Link existence is a package-wide documentation concern. Dependency/path
    # restrictions above remain scoped to runtime instructions only.
    for path in root.rglob('*.md'):
        rel = path.relative_to(root)
        if any(part in {'.work', '.git', 'runs', '__pycache__'} for part in rel.parts) or str(rel) in RUNTIME:
            continue
        for raw in LINK.findall(path.read_text(encoding='utf-8')):
            link = unquote(raw.strip('<>'))
            if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', link):
                continue
            target = link.split('#', 1)[0].split('?', 1)[0]
            if target and not (path.parent / target).exists():
                error('BROKEN_LINK', str(rel), link)
    manifest_path = root / 'fidelity-ledger/source-manifest.json'
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        if not isinstance(manifest, dict):
            raise ValueError('manifest must be an object')
        if manifest.get('schema_version') != '1.0':
            error('MANIFEST_VERSION', str(manifest_path.relative_to(root)), 'expected schema_version 1.0')
        sources = manifest.get('sources')
        if not isinstance(sources, list):
            raise ValueError('sources must be an array')
        seen, destinations = set(), set()
        for n, source in enumerate(sources):
            at = f'sources[{n}]'
            if not isinstance(source, dict):
                error('MANIFEST_TYPE', at, 'expected object')
                continue
            repo = source.get('repo')
            if not isinstance(repo, str) or not re.fullmatch(r'[A-Za-z0-9_.-]+', repo):
                error('MANIFEST_REPO', at, 'expected portable repo identifier')
            elif repo in seen:
                error('MANIFEST_DUPLICATE', at, repo)
            else:
                seen.add(repo)
            for field in ('head', 'role'):
                if not isinstance(source.get(field), str) or not source[field].strip():
                    error('MANIFEST_FIELD', at + '.' + field, 'required nonempty string; unknown allowed for unavailable HEAD')
            files = source.get('files')
            if not isinstance(files, list) or not files:
                error('MANIFEST_FILES', at, 'requires selected source files')
                continue
            file_paths = set()
            for m, item in enumerate(files):
                loc = f'{at}.files[{m}]'
                if not isinstance(item, dict):
                    error('MANIFEST_TYPE', loc, 'expected object')
                    continue
                value = item.get('path')
                if not portable(value):
                    error('MANIFEST_PATH', loc, 'expected repo-relative source path')
                elif value in file_paths:
                    error('MANIFEST_DUPLICATE', loc, value)
                else:
                    file_paths.add(value)
                if not isinstance(item.get('sha256'), str) or not SHA.fullmatch(item['sha256']):
                    error('MANIFEST_HASH', loc, 'expected source SHA-256')
                for key in ('worktree_status', 'adaptation'):
                    if not isinstance(item.get(key), str) or not item[key].strip():
                        error('MANIFEST_FIELD', loc + '.' + key, 'required nonempty string')
                sections = item.get('sections')
                if not isinstance(sections, list) or not sections or any(not isinstance(s, str) or not s.strip() for s in sections):
                    error('MANIFEST_SECTIONS', loc, 'requires selected sections/ranges')
                targets = item.get('destinations')
                if not isinstance(targets, list) or not targets:
                    error('MANIFEST_DESTINATIONS', loc, 'requires actual package destinations')
                else:
                    for target in targets:
                        if not portable(target) or not exists(target):
                            error('MANIFEST_DESTINATION', loc, str(target))
                        else:
                            destinations.add(target)
            if 'LICENSE' not in file_paths:
                error('MANIFEST_LICENSE', at, 'selected source LICENSE must be registered')
        for missing in EXPECTED_SOURCES - seen:
            error('MANIFEST_SOURCE', 'sources', 'missing ' + missing)
        for target in ('references/teaching-design.md', 'references/law-reasoning.md', 'references/transcript-repair.md', 'LICENSE', 'NOTICE.md'):
            if target not in destinations:
                error('MANIFEST_COVERAGE', target, 'adaptation provenance not registered')
        manifest_text = manifest_path.read_text(encoding='utf-8')
        if ABSOLUTE.search(manifest_text) or 'local_root' in manifest:
            error('MANIFEST_LOCAL_PATH', 'source-manifest.json', 'publishable manifest must omit personal absolute paths')
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        error('MANIFEST_READ', 'fidelity-ledger/source-manifest.json', str(exc))
    return {'status': 'fail' if errors else 'pass', 'scope': 'package_structure_and_source_registration',
            'limitation': '仅检查包结构、有限路径及来源登记；哈希是内容身份记录，不证明来源正确性、教学质量或学习效果。',
            'errors': errors, 'exit_code': 1 if errors else 0}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path, nargs='?', default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:
        result = validate_repo(args.root)
    except (OSError, UnicodeError) as exc:
        result = {'status': 'fail', 'errors': [{'code': 'READ', 'at': str(args.root), 'message': str(exc)}], 'exit_code': 1}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result['status'] + ': ' + result.get('limitation', 'package could not be read'))
        for item in result['errors']:
            print(f"{item['code']} {item['at']}: {item['message']}")
    return result['exit_code']


if __name__ == '__main__':
    sys.exit(main())
