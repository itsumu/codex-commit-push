import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1] / "commit-push/scripts/publish.py"


class PublishTest(unittest.TestCase):
    def test_review_guard_and_first_push(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "work"
            repo.mkdir()
            env = dict(os.environ, HOME=tmp, GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="Test",
                       GIT_AUTHOR_EMAIL="test@example.invalid", GIT_COMMITTER_NAME="Test",
                       GIT_COMMITTER_EMAIL="test@example.invalid")

            def run(*args, check=True):
                return subprocess.run(args, cwd=repo, env=env, text=True,
                                      capture_output=True, check=check)

            remote = root / "remote.git"
            run("git", "init", "--bare", str(remote))
            run("git", "init", "-b", "main")
            run("git", "remote", "add", "origin", str(remote))
            (repo / "sample").write_text("reviewed\n")
            run("git", "add", "sample")
            tree = run("git", "write-tree").stdout.strip()
            (repo / "sample").write_text("unstaged\n")
            msg = root / "message"
            msg.write_text("Add reviewed sample\n")

            def publish(snapshot, check=True):
                return run(sys.executable, str(HELPER), "main", "unborn",
                           snapshot, "origin", "main", str(msg), check=check)

            self.assertNotEqual(publish("stale", check=False).returncode, 0)
            self.assertNotEqual(run("git", "rev-parse", "--verify", "HEAD", check=False).returncode, 0)
            publish(tree)
            self.assertEqual(run("git", "--git-dir", str(remote), "show", "main:sample").stdout, "reviewed\n")
            self.assertEqual((repo / "sample").read_text(), "unstaged\n")
            self.assertEqual(run("git", "rev-parse", "--abbrev-ref", "@{u}").stdout.strip(), "origin/main")
