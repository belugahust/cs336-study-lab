import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import github_sync
import study


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'workspace'
        self.root.mkdir()
        course = study.load_course(study.ROOT)
        (self.root / 'course.json').write_text(json.dumps(course), encoding='utf-8')
        for lesson in course['lectures']:
            p = self.root / lesson['note']
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('# Test note\n', encoding='utf-8')

    def tearDown(self):
        self.tmp.cleanup()

    def call(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return study.main(list(args), root=self.root)

    def test_repeat_sessions_accumulate_without_finishing_practice(self):
        self.assertEqual(self.call('record', '--lecture', '1', '--minutes', '25', '--summary', 'BPE', '--watched'), 0)
        self.assertEqual(self.call('record', '--lecture', '1', '--minutes', '15', '--summary', 'merge rule'), 0)
        state = study.states(study.load_course(self.root), study.read_events(self.root))[1]
        self.assertEqual(state['minutes'], 40)
        self.assertEqual(state['sessions'], 2)
        self.assertTrue(state['watched'])
        self.assertFalse(state['practice'])
        self.assertEqual(self.call('render', '--check'), 0)

    def test_invalid_session_does_not_write_data(self):
        self.assertEqual(self.call('record', '--lecture', '99', '--minutes', '10', '--summary', 'invalid'), 1)
        self.assertEqual(self.call('record', '--lecture', '1', '--minutes', '10', '--summary', ' '), 1)
        self.assertEqual(study.read_events(self.root), [])

    def test_failed_push_keeps_one_local_record(self):
        self.assertEqual(self.call('record', '--lecture', '2', '--minutes', '20', '--summary', 'shape', '--push'), 1)
        self.assertEqual(len(study.read_events(self.root)), 1)
        self.assertEqual(self.call('render', '--check'), 0)

    def test_experiment_metrics_and_html_escaping(self):
        self.assertEqual(self.call('experiment', '--assignment', '1', '--name', 'small', '--metric', 'val_loss=1.5', '--seed', '42', '--device', 'CPU'), 0)
        event = study.read_events(self.root)[0]
        self.assertEqual(event['metrics'], {'val_loss': 1.5})
        self.assertEqual(event['seed'], 42)
        self.assertEqual(self.call('experiment', '--assignment', '1', '--name', 'bad', '--metric', 'loss=nan'), 1)
        self.assertEqual(len(study.read_events(self.root)), 1)
        note = self.root / 'lectures/01/notes.md'
        note.write_text('<script>alert(1)</script>', encoding='utf-8')
        self.assertEqual(self.call('render'), 0)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', (self.root / 'index.html').read_text(encoding='utf-8'))

    def test_corrupt_event_stops_append(self):
        path = self.root / 'records/sessions.jsonl'
        path.parent.mkdir()
        path.write_text('{broken\n', encoding='utf-8')
        self.assertEqual(self.call('record', '--lecture', '1', '--minutes', '10', '--summary', 'x'), 1)
        self.assertEqual(path.read_text(encoding='utf-8'), '{broken\n')

    def test_stale_generated_files_are_detected(self):
        self.assertEqual(self.call('render'), 0)
        (self.root / 'index.html').write_text('stale', encoding='utf-8')
        self.assertEqual(self.call('render', '--check'), 1)

    @unittest.skipUnless(shutil.which('git'), 'git required')
    def test_sync_to_local_remote_and_retry_with_no_changes(self):
        remote = Path(self.tmp.name) / 'remote.git'
        subprocess.run(['git', 'init', '--bare', str(remote)], check=True, capture_output=True)
        for args in [('init', '-b', 'main'), ('config', 'user.name', 'Test'), ('config', 'user.email', 'test@example.invalid'), ('remote', 'add', 'origin', str(remote))]:
            study.git(self.root, *args)
        self.assertEqual(self.call('record', '--lecture', '1', '--minutes', '10', '--summary', 'test', '--push'), 0)
        self.assertEqual(self.call('sync'), 0)
        local = study.git(self.root, 'rev-parse', 'HEAD').stdout.strip()
        published = subprocess.run(['git', '--git-dir', str(remote), 'rev-parse', 'refs/heads/main'], check=True, text=True, capture_output=True).stdout.strip()
        self.assertEqual(local, published)


class ApiSafetyTests(unittest.TestCase):
    def test_rejects_non_github_and_credential_urls(self):
        for remote in ('https://example.com/u/r.git', 'https://secret@github.com/u/r.git'):
            with patch('github_sync.run', return_value=remote), self.assertRaises(ValueError):
                github_sync.GitHub(Path('.'))

    def test_remote_newer_is_never_overwritten(self):
        class FakeGitHub:
            def __init__(self, root):
                pass

            def repo_request(self, method, path, body=None, allow_404=False):
                if method != 'GET':
                    raise AssertionError('Must not write remote')
                return {'object': {'sha': 'remote-sha'}}

        with patch('github_sync.GitHub', FakeGitHub), patch('github_sync.run', return_value='local-sha'), patch('github_sync.subprocess.run', return_value=subprocess.CompletedProcess([], 1)), self.assertRaisesRegex(ValueError, '不会覆盖远端'):
            github_sync.sync_api(Path('.'), 'main')


if __name__ == '__main__':
    unittest.main()
