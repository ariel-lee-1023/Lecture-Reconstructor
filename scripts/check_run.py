#!/usr/bin/env python3
"""Check documented, finite run invariants using only Python's standard library.

This is deliberately NOT a general JSON Schema validator. It cannot certify
meaning coverage, legal truth, teaching quality, or learning outcomes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

STATUSES = {'in_progress', 'needs_input', 'partial', 'complete'}
STAGES = {'ingest', 'map', 'plan', 'draft', 'review', 'assemble', 'deliver'}
CHAPTER_STATES = {'planned', 'drafted', 'needs_review', 'reviewed', 'assembled'}
UNIT_STATES = {'represented', 'merged', 'corrected', 'excluded', 'unresolved'}
HASH = re.compile(r'^[0-9a-f]{64}$')
ANCHOR = re.compile(r'<a\s+(?:id|name)=["\']([^"\']+)["\']\s*>\s*</a>|\{#([^}\s]+)\}')
LIMITATION = '仅通过有限结构检查；不证明法律正确性、意义覆盖、教学质量或学习效果。'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def anchors(text):
    return {a or b for a, b in ANCHOR.findall(text)}


class Checker:
    def __init__(self, run_path, repo_root):
        self.run_path = Path(run_path).resolve()
        self.base = self.run_path.parent
        self.repo = Path(repo_root).resolve()
        self.errors = []
        self.changed = False
        self.texts = {}
        self.lines = {}

    def error(self, code, at, message):
        self.errors.append({'code': code, 'at': at, 'message': message})
        if code in {'INPUT_CHANGED', 'RUNTIME_CHANGED'}:
            self.changed = True

    def obj(self, value, at):
        if not isinstance(value, dict):
            self.error('TYPE', at, 'expected object')
            return {}
        return value

    def array(self, value, at):
        if not isinstance(value, list):
            self.error('TYPE', at, 'expected array')
            return []
        return value

    def string(self, value, at, nonempty=True):
        if not isinstance(value, str) or (nonempty and not value.strip()):
            self.error('VALUE', at, 'expected nonempty string' if nonempty else 'expected string')
            return ''
        return value

    def enum(self, value, allowed, at):
        if not isinstance(value, str) or value not in allowed:
            self.error('STATE', at, 'expected one of: ' + ', '.join(sorted(allowed)))

    def strings(self, value, at):
        items = self.array(value, at)
        for n, item in enumerate(items):
            self.string(item, f'{at}[{n}]')
        return [v for v in items if isinstance(v, str)]

    def path(self, value, at, root=None, required=True):
        if not isinstance(value, str) or not value.strip():
            self.error('PATH', at, 'expected a nonempty relative path')
            return None
        root = root or self.base
        p = Path(value)
        resolved = (root / p).resolve()
        if p.is_absolute() or not resolved.is_relative_to(root):
            self.error('PATH', at, 'path must stay inside its declared root')
            return None
        if required and not resolved.is_file():
            self.error('MISSING_FILE', at, value)
            return None
        return resolved

    def read(self, path, at):
        if path is None or not path.is_file():
            return ''
        try:
            return path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            self.error('READ', at, str(exc))
            return ''

    def hashed(self, path, expected, at, code):
        if not isinstance(expected, str) or not HASH.fullmatch(expected):
            self.error('HASH', at, 'expected lowercase SHA-256')
        elif path is not None and path.is_file():
            try:
                actual = sha256(path)
                if actual != expected:
                    self.error(code, at, f'needs_review: expected {expected}, actual {actual}; perform impact review before updating hashes')
            except OSError as exc:
                self.error('READ', at, str(exc))

    def indexed(self, raw, name):
        items, by_id = [], {}
        for n, item in enumerate(self.array(raw, name)):
            at = f'{name}[{n}]'
            item = self.obj(item, at)
            ident = self.string(item.get('id'), at + '.id')
            if ident in by_id:
                self.error('DUPLICATE_ID', at + '.id', ident)
            if ident:
                by_id[ident] = item
            items.append((item, at))
        return items, by_id

    def ref(self, ident, by_id, at):
        if not isinstance(ident, str) or ident not in by_id:
            self.error('DANGLING_ID', at, str(ident))
            return False
        return True

    def location(self, loc, at, inputs):
        loc = self.obj(loc, at)
        ident = loc.get('input_id')
        valid_id = self.ref(ident, inputs, at + '.input_id')
        start, end = loc.get('start_line'), loc.get('end_line')
        if type(start) is not int or type(end) is not int or start < 1 or end < start:
            self.error('RANGE', at, 'expected inclusive 1-based start_line <= end_line')
            return None
        if valid_id and end > self.lines.get(ident, 0):
            self.error('RANGE', at, f'end_line exceeds normalized text ({self.lines.get(ident, 0)} lines)')
            return None
        if not valid_id:
            return None
        return ident, start, end

    def blocking(self, item, at):
        if type(item.get('blocking')) is not bool:
            self.error('TYPE', at + '.blocking', 'expected boolean')
        self.string(item.get('blocking_reason'), at + '.blocking_reason')

    def check(self):
        try:
            raw = json.loads(self.run_path.read_text(encoding='utf-8'))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            self.error('RUN_READ', 'run', str(exc))
            return self.result()
        run = self.obj(raw, 'run')
        self.enum(run.get('schema_version'), {'1.0'}, 'schema_version')
        self.string(run.get('run_id'), 'run_id')
        self.enum(run.get('status'), STATUSES, 'status')
        self.enum(run.get('stage'), STAGES, 'stage')
        complete = run.get('status') == 'complete'
        if complete and run.get('stage') != 'deliver':
            self.error('COMPLETE_STAGE', 'stage', 'complete requires deliver')
        course = self.obj(run.get('course'), 'course')
        for key in ('title', 'scope', 'jurisdiction', 'time_context', 'audience'):
            self.string(course.get(key), 'course.' + key)
        self.strings(course.get('assumptions'), 'course.assumptions')
        rounds = run.get('revision_round')
        if type(rounds) is not int or rounds < 0:
            self.error('VALUE', 'revision_round', 'expected nonnegative integer')

        input_items, inputs = self.indexed(run.get('inputs'), 'inputs')
        if complete and not inputs:
            self.error('EMPTY_INPUT', 'inputs', 'complete requires readable transcript input')
        for item, at in input_items:
            self.string(item.get('kind'), at + '.kind')
            original = self.path(item.get('path'), at + '.path')
            self.hashed(original, item.get('sha256'), at + '.sha256', 'INPUT_CHANGED')
            normalized = self.path(item.get('normalized_path'), at + '.normalized_path')
            self.hashed(normalized, item.get('normalized_sha256'), at + '.normalized_sha256', 'INPUT_CHANGED')
            text = self.read(normalized, at + '.normalized_path')
            if isinstance(item.get('id'), str):
                self.lines[item['id']] = len(text.splitlines())
            if complete and not text.strip():
                self.error('EMPTY_INPUT', at, 'complete cannot use an empty normalized input')

        reviewed = {key: set() for key in inputs}
        unread = {key: set() for key in inputs}
        for n, value in enumerate(self.array(run.get('source_review'), 'source_review')):
            at = f'source_review[{n}]'
            item = self.obj(value, at)
            loc = self.location(item, at, inputs)
            self.enum(item.get('status'), {'reviewed', 'unread'}, at + '.status')
            if loc:
                ident, start, end = loc
                if item.get('status') == 'reviewed':
                    reviewed[ident].update(range(start, end + 1))
                elif item.get('status') == 'unread':
                    unread[ident].update(range(start, end + 1))
        for ident in inputs:
            all_lines = set(range(1, self.lines.get(ident, 0) + 1))
            missing = all_lines - reviewed[ident] - unread[ident]
            if missing:
                self.error('UNTRACKED_RANGE', 'source_review', f'{ident}: untracked lines {min(missing)}..{max(missing)}')
            if complete and (all_lines - reviewed[ident] or unread[ident]):
                self.error('UNREVIEWED_RANGE', 'source_review', f'{ident}: complete requires every line reviewed and no unread intervals')

        source_items, sources = self.indexed(run.get('sources'), 'sources')
        for item, at in source_items:
            for key in ('uri', 'version', 'locator'):
                self.string(item.get(key), at + '.' + key)
            self.enum(item.get('read_status'), {'read', 'unread', 'unavailable'}, at + '.read_status')
            uri = item.get('uri')
            if isinstance(uri, str) and not re.match(r'^[A-Za-z][A-Za-z0-9+.-]*://', uri):
                self.path(uri, at + '.uri', required=item.get('read_status') == 'read')

        chapter_items, chapters = self.indexed(run.get('chapters'), 'chapters')
        unit_items, units = self.indexed(run.get('content_units'), 'content_units')
        if complete and (not chapters or not units):
            self.error('EMPTY_COMPLETE', 'chapters/content_units', 'complete requires chapter and substantive content mappings')
        for item, at in chapter_items:
            state = item.get('status') if isinstance(item.get('status'), str) else None
            self.enum(state, CHAPTER_STATES, at + '.status')
            for key in ('anchor', 'learning_object', 'approach', 'role'):
                self.string(item.get(key), at + '.' + key)
            for key in ('relations', 'prerequisites'):
                self.strings(item.get(key), at + '.' + key)
            required = state in {'drafted', 'reviewed', 'assembled'}
            path = self.path(item.get('path'), at + '.path', required=required)
            if state == 'needs_review' and (path is None or not path.is_file()):
                self.string(item.get('missing_reason'), at + '.missing_reason')
            text = self.read(path, at + '.path')
            if isinstance(item.get('id'), str):
                self.texts[item['id']] = text
            if required and (not isinstance(item.get('anchor'), str) or item.get('anchor') not in anchors(text)):
                self.error('MISSING_ANCHOR', at + '.anchor', str(item.get('anchor')))
            for n, uid in enumerate(self.array(item.get('content_unit_ids'), at + '.content_unit_ids')):
                self.ref(uid, units, f'{at}.content_unit_ids[{n}]')
            if complete and state not in {'reviewed', 'assembled'}:
                self.error('INCOMPLETE_CHAPTER', at + '.status', str(state))

        graph = {}
        for item, at in unit_items:
            for key in ('proposition', 'type', 'reason'):
                self.string(item.get(key), at + '.' + key)
            state = item.get('status') if isinstance(item.get('status'), str) else None
            self.enum(state, UNIT_STATES, at + '.status')
            locs = self.array(item.get('locations'), at + '.locations')
            for n, loc in enumerate(locs):
                self.location(loc, f'{at}.locations[{n}]', inputs)
            source_ids = self.array(item.get('source_ids'), at + '.source_ids')
            for n, sid in enumerate(source_ids):
                if self.ref(sid, sources, f'{at}.source_ids[{n}]') and complete and sources[sid].get('read_status') != 'read':
                    self.error('UNREAD_SOURCE', at + '.source_ids', sid)
            if not locs and not source_ids:
                self.error('NO_PROVENANCE', at, 'content item needs input location or source_id')
            targets = self.array(item.get('targets'), at + '.targets')
            if state in {'represented', 'merged', 'corrected'} and not targets:
                self.error('NO_TARGET', at + '.targets', 'represented/merged/corrected requires target')
            for n, raw_target in enumerate(targets):
                target_at = f'{at}.targets[{n}]'
                target = self.obj(raw_target, target_at)
                cid = target.get('chapter_id')
                anchor = self.string(target.get('anchor'), target_at + '.anchor')
                if self.ref(cid, chapters, target_at + '.chapter_id'):
                    chapter = chapters[cid]
                    if isinstance(chapter.get('status'), str) and chapter.get('status') in {'drafted', 'reviewed', 'assembled'} and anchor not in anchors(self.texts.get(cid, '')):
                        self.error('MISSING_ANCHOR', target_at, f'{cid}#{anchor}')
                    if item.get('id') not in (chapter.get('content_unit_ids') if isinstance(chapter.get('content_unit_ids'), list) else []):
                        self.error('MAPPING_MISMATCH', target_at, 'target chapter must list this content unit')
            if state == 'merged':
                target = item.get('merge_into')
                if self.ref(target, units, at + '.merge_into') and isinstance(item.get('id'), str):
                    graph[item['id']] = target
            if state == 'corrected':
                self.string(item.get('original_meaning'), at + '.original_meaning')
                self.string(item.get('correction_basis'), at + '.correction_basis')
            if state == 'unresolved':
                self.blocking(item, at)
                if complete and item.get('blocking') is True:
                    self.error('BLOCKING_CONTENT', at, 'unresolved substantive issue')
        for start in graph:
            visited = set()
            node = start
            while node in graph:
                if node in visited:
                    self.error('MERGE_CYCLE', 'content_units', f'cycle reachable from {start}: {node}')
                    break
                visited.add(node)
                node = graph[node]
        for chapter, at in chapter_items:
            for uid in chapter.get('content_unit_ids', []) if isinstance(chapter.get('content_unit_ids'), list) else []:
                if isinstance(uid, str) and uid in units:
                    target_chapters = [x.get('chapter_id') for x in units[uid].get('targets', []) if isinstance(x, dict)] if isinstance(units[uid].get('targets'), list) else []
                    if chapter.get('id') not in target_chapters:
                        self.error('MAPPING_MISMATCH', at + '.content_unit_ids', f'{uid} must point back to this chapter')

        for n, raw_term in enumerate(self.array(run.get('terms'), 'terms')):
            at = f'terms[{n}]'
            term = self.obj(raw_term, at)
            self.string(term.get('term'), at + '.term')
            self.string(term.get('decision'), at + '.decision')
        issue_items, _ = self.indexed(run.get('open_issues'), 'open_issues')
        for issue, at in issue_items:
            for key in ('question', 'impact', 'resolution_condition'):
                self.string(issue.get(key), at + '.' + key)
            self.enum(issue.get('status'), {'open', 'resolved'}, at + '.status')
            self.blocking(issue, at)
            if complete and issue.get('status') == 'open' and issue.get('blocking') is True:
                self.error('BLOCKING_ISSUE', at, 'complete cannot retain blocking open issue')

        runtime = self.obj(run.get('runtime_revision'), 'runtime_revision')
        for key in ('host', 'model'):
            self.string(runtime.get(key), 'runtime_revision.' + key)
        self.obj(runtime.get('settings'), 'runtime_revision.settings')
        runtime_files = self.array(runtime.get('files'), 'runtime_revision.files')
        runtime_paths = set()
        for n, raw_file in enumerate(runtime_files):
            at = f'runtime_revision.files[{n}]'
            item = self.obj(raw_file, at)
            path_value = item.get('path')
            if isinstance(path_value, str):
                if path_value in runtime_paths:
                    self.error('DUPLICATE_PATH', at, path_value)
                runtime_paths.add(path_value)
            path = self.path(path_value, at + '.path', self.repo)
            self.hashed(path, item.get('sha256'), at + '.sha256', 'RUNTIME_CHANGED')
        if 'SKILL.md' not in runtime_paths:
            self.error('MISSING_RUNTIME', 'runtime_revision.files', 'must record SKILL.md and every loaded reference')

        output = self.obj(run.get('output'), 'output')
        output_path = self.path(output.get('path'), 'output.path', required=complete or (isinstance(run.get('stage'), str) and run.get('stage') in {'assemble', 'deliver'}))
        output_text = self.read(output_path, 'output.path')
        if complete and not output_text.strip():
            self.error('EMPTY_OUTPUT', 'output.path', 'complete requires nonempty manuscript')
        if complete:
            output_anchors = anchors(output_text)
            for chapter, at in chapter_items:
                if not isinstance(chapter.get('anchor'), str) or chapter.get('anchor') not in output_anchors:
                    self.error('MISSING_OUTPUT_ANCHOR', at + '.anchor', str(chapter.get('anchor')))
            for unit, at in unit_items:
                for target in unit.get('targets', []) if isinstance(unit.get('targets'), list) else []:
                    if isinstance(target, dict) and (not isinstance(target.get('anchor'), str) or target.get('anchor') not in output_anchors):
                        self.error('MISSING_OUTPUT_ANCHOR', at + '.targets', str(target.get('anchor')))

        check_items, _ = self.indexed(run.get('checks'), 'checks')
        current_review = False
        latest_full_review = max((n for n, (item, _) in enumerate(check_items)
                                  if item.get('kind') == 'semantic'
                                  and item.get('scope') == 'full_manuscript'), default=-1)
        for check_index, (item, at) in enumerate(check_items):
            self.enum(item.get('kind'), {'mechanical', 'semantic'}, at + '.kind')
            self.enum(item.get('status'), {'pass', 'fail', 'not_run'}, at + '.status')
            for key in ('scope', 'method', 'date'):
                self.string(item.get(key), at + '.' + key)
            if item.get('status') != 'not_run':
                evidence = self.path(item.get('evidence'), at + '.evidence')
                if evidence is not None and not self.read(evidence, at + '.evidence').strip():
                    self.error('EMPTY_EVIDENCE', at + '.evidence', 'evidence cannot be empty')
            else:
                evidence = None
            if item.get('kind') == 'semantic' and item.get('scope') == 'full_manuscript':
                # Check records are append-only chronological evidence. A later
                # full-manuscript failure/not-run cannot inherit an earlier pass.
                current_review = False
            if item.get('kind') == 'semantic' and item.get('scope') == 'full_manuscript' and item.get('status') == 'pass':
                expected = item.get('output_sha256')
                if check_index == latest_full_review:
                    self.hashed(output_path, expected, at + '.output_sha256', 'STALE_REVIEW')
                    if (evidence is not None and output_path is not None and output_path.is_file()
                            and expected == sha256(output_path)):
                        current_review = True
                elif not isinstance(expected, str) or not HASH.fullmatch(expected):
                    self.error('HASH', at + '.output_sha256', 'historical review requires its original SHA-256')
        if complete and not current_review:
            self.error('MISSING_SEMANTIC_REVIEW', 'checks', 'complete requires full_manuscript semantic pass, existing evidence, matching current output SHA-256')
        resume = self.obj(run.get('resume'), 'resume')
        self.strings(resume.get('completed'), 'resume.completed')
        remaining = self.strings(resume.get('remaining'), 'resume.remaining')
        self.string(resume.get('next_action'), 'resume.next_action')
        if complete and remaining:
            self.error('INCOMPLETE_RESUME', 'resume.remaining', 'complete requires no remaining ranges')
        return self.result()

    def result(self):
        return {'status': 'needs_review' if self.changed else ('fail' if self.errors else 'pass'),
                'scope': 'finite_structural_checks', 'limitation': LIMITATION,
                'errors': self.errors, 'exit_code': 2 if self.changed else (1 if self.errors else 0)}


def validate_run(run_path, repo_root):
    return Checker(run_path, repo_root).check()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path, help='run.json; all run paths resolve relative to this file')
    parser.add_argument('--repo-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json', action='store_true', help='machine-readable result')
    args = parser.parse_args(argv)
    result = validate_run(args.run, args.repo_root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['status']}: {result['limitation']}")
        for error in result['errors']:
            print(f"{error['code']} {error['at']}: {error['message']}")
    return result['exit_code']


if __name__ == '__main__':
    sys.exit(main())
