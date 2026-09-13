from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from package_plugin import package
from scan_public import findings


class PublicDistributionTests(unittest.TestCase):
    def test_rejects_secrets_without_needing_real_credentials(self):
        cases = [
            ('github-token', 'gh' + 'p_' + 'A' * 30),
            ('api-key', 'sk' + '-proj-' + 'A' * 30),
            ('aws-access-key', 'AK' + 'IA' + '1' * 16),
            ('email-address', 'person' + '@' + 'private.test'),
            ('machine-path', '/home/' + 'someone/private'),
            ('machine-path', 'C' + ':/Users/' + 'someone'),
        ]
        for rule, value in cases:
            with self.subTest(rule=rule):
                self.assertIn(rule, findings('file.txt', value.encode()))

    def test_public_urls_and_reserved_examples_allowed(self):
        self.assertEqual(findings('README.md', b'https://github.com/owner/repo'), [])
        self.assertEqual(findings('README.md', b'author@example.com'), [])

    def test_local_files_rejected(self):
        self.assertIn('private-file', findings('.env', b''))
        self.assertIn('local-state', findings('learning/topic/progress.md', b''))
        self.assertIn('unexpected-binary', findings('data.bin', bytes([255])))

    def test_package_is_reproducible_and_contains_only_plugin(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            a, b = package(first), package(second)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            with zipfile.ZipFile(a) as archive:
                names = archive.namelist()
                self.assertIn('.codex-plugin/plugin.json', names)
                self.assertIn('LICENSE', names)
                self.assertIn('assets/icon.svg', names)
                self.assertFalse(any(n.startswith(('.git/', 'tests/', 'scripts/')) for n in names))
                self.assertIsNone(archive.testzip())


if __name__ == '__main__':
    unittest.main()
