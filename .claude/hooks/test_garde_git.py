"""Tests of the git guard hook. Run from the repository root:

/usr/bin/python3 -m unittest discover -s .claude/hooks -p "test_*.py"
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).with_name("garde_git.py")

BLOCKED = [
    "git checkout -- app/models.py",
    "git -C back checkout .",
    "cd back && git checkout main",
    "git restore app/models.py",
    "git restore --staged --worktree app/models.py",
    "git -C front reset --hard HEAD~1",
    "git clean -fd",
    "git -c color.ui=never clean -xdf",
    "git switch --discard-changes main",
    "git stash drop",
    "git push --force origin main",
    "git push -f",
    "git push --force-with-lease=main origin main",
    "git push origin +main",
    "bash -c 'git checkout -- x'",
    'sh -lc "cd back && git reset --hard"',
    "eval git checkout -- x",
    "git status\ngit checkout -- x",
    "git push \\\n  --force origin main",
    "echo $(git checkout -- x)",
    "echo `git checkout -- x`",
    "/usr/bin/git reset --hard",
    "find . -name '*.py' -exec git checkout -- {} \\;",
]

ALLOWED = [
    "git status",
    "git -C back diff --stat",
    "git log --oneline -5",
    "git restore --staged app/models.py",
    "git reset HEAD~1",
    "git clean -n",
    "git switch main",
    "git stash",
    "git push origin main",
    "git commit -m 'docs: le hook refuse git checkout -- et git reset --hard'",
    "git commit -m \"$(cat <<'EOF'\ndocs: git checkout -- x est refusé\n\ngit reset --hard aussi\nEOF\n)\"",
    "git commit -F - <<'EOF'\ngit checkout -- x est refusé\nEOF",
    'gh pr create --body "Résumé\n- git reset --hard est bloqué"',
    "grep -rn 'git checkout' .",
    "# git checkout -- x\nls",
    "uv run pytest --cov",
    "ls git",
]


def run(payload):
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
        check=False,
    )


def run_command(command):
    return run(json.dumps({"tool_name": "Bash", "tool_input": {"command": command}}))


class GitGuardTest(unittest.TestCase):
    def test_blocks_commands_that_lose_work(self):
        for command in BLOCKED:
            with self.subTest(command=command):
                result = run_command(command)
                self.assertEqual(result.returncode, 2)
                self.assertIn("Garde-fou", result.stderr)

    def test_lets_other_commands_through(self):
        for command in ALLOWED:
            with self.subTest(command=command):
                result = run_command(command)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_lets_unreadable_input_through(self):
        for payload in [
            "not json",
            "[]",
            json.dumps({"tool_name": "Read", "tool_input": {}}),
        ]:
            with self.subTest(payload=payload):
                self.assertEqual(run(payload).returncode, 0)


if __name__ == "__main__":
    unittest.main()
