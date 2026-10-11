#!/usr/bin/env python3
from pathlib import Path
import os
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class PrivatePreservedRepositoryTests(unittest.TestCase):
    def test_passwords_never_native_argv(self):
        text = (ROOT / 'stack.config/kopia/init-kopia.sh').read_text()
        self.assertNotIn('--password', text)
        self.assertNotIn('--server-password', text)
        self.assertIn('export KOPIA_PASSWORD KOPIA_SERVER_PASSWORD', text)
        runtime = (ROOT / 'stack.runtime.yaml').read_text()
        self.assertIn('--config -', runtime)
        self.assertNotIn(' -u ', runtime)

    def test_existing_repository_policy_is_not_startup_scratch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mock = root / 'kopia'
            receipt = root / 'receipt'
            mock.write_text('''#!/bin/sh
set -eu
case "$*" in
 "repository status") exit 0 ;;
 "policy "*) exit 77 ;;
 "server start "*)
  test "$KOPIA_PASSWORD" = public-source-fixture
  test "$KOPIA_SERVER_PASSWORD" = public-source-fixture
  printf 'native-env-no-policy' > "$UNIT_RECEIPT"
  exit 0 ;;
 *) exit 78 ;;
esac
''')
            mock.chmod(0o700)
            env = dict(os.environ, PATH=f'{root}:{os.environ["PATH"]}', KOPIA_PASSWORD='public-source-fixture', KOPIA_REPO_PATH=str(root / 'repo'), UNIT_RECEIPT=str(receipt))
            result = subprocess.run(['sh', str(ROOT / 'stack.config/kopia/init-kopia.sh')], env=env, capture_output=True)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(receipt.read_text(), 'native-env-no-policy')

if __name__ == '__main__':
    unittest.main()
