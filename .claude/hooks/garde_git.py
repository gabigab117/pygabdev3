#!/usr/bin/env python3
"""PreToolUse hook: refuse the git commands that destroy uncommitted work or rewrite main.

Claude Code passes the Bash call as JSON on stdin. Exit code 2 blocks the call and
shows stderr to Claude. A command this script cannot read is let through: Bash itself
would refuse a command that does not parse.

A `deny` permission rule would not do: it matches the command's text, so
`git -C back checkout -- x` escapes `Bash(git checkout *)`.

Runs on the macOS system Python (3.9): no syntax newer than that.
"""

import json
import re
import shlex
import sys

OPERATOR_CHARS = ";&|()`\n"
SHELLS = {"sh", "bash", "zsh"}
# Global git options whose value is the next word (`git -C back status`).
GIT_OPTIONS_WITH_VALUE = {
    "-C",
    "-c",
    "--git-dir",
    "--work-tree",
    "--namespace",
    "--exec-path",
    "--config-env",
}
HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
MAX_NESTING = 3

PREFIX = "Garde-fou du projet : "
SUFFIX = " Si l'opération est vraiment voulue, Gabriel la lance lui-même."
FROM_COPY = (
    "Pour annuler une modification volontaire, restaure le fichier depuis sa copie du "
    "scratchpad ; pour lire une autre version, `git show <révision>:<chemin>`."
)
CHECKOUT = (
    "`git checkout` est refusé : il écrase des fichiers modifiés sans prévenir, ce qui a "
    "déjà effacé un travail non commité. Pour changer de branche : `git switch`. "
    + FROM_COPY
)
RESTORE = (
    "`git restore` sur les fichiers de travail est refusé : il efface leurs modifications "
    "non commitées. `git restore --staged` (retirer de l'index) reste permis. "
    + FROM_COPY
)
RESET = (
    "`git reset --hard` est refusé : il efface toutes les modifications non commitées. "
    "`git reset` sans `--hard` garde les fichiers de travail."
)
CLEAN = (
    "`git clean -f` est refusé : il supprime les fichiers non suivis, donc le travail neuf "
    "pas encore commité. `git clean -n` montre ce qui serait supprimé."
)
SWITCH = "`git switch` forcé est refusé : il jette les modifications non commitées."
STASH = "`git stash drop` et `git stash clear` sont refusés : le travail mis de côté serait perdu."
PUSH = (
    "Le force-push est refusé : l'historique de `main` est linéaire, et le distant sert de "
    "sauvegarde."
)


def without_heredocs_and_comments(command):
    """Drop here-document bodies and comment lines, which are text, not commands."""
    kept = []
    delimiter = None
    for line in command.split("\n"):
        if delimiter is not None:
            if line.strip() == delimiter:
                delimiter = None
            continue
        if line.lstrip().startswith("#"):
            continue
        kept.append(line)
        match = HEREDOC.search(line)
        if match:
            delimiter = match.group(2)
    return "\n".join(kept)


def simple_commands(text):
    """Split shell text into simple commands, each a list of words.

    Newlines outside quotes separate commands; inside quotes they stay in the word, so a
    multi-line commit message is never read as commands.
    """
    lexer = shlex.shlex(text, posix=True, punctuation_chars=OPERATOR_CHARS)
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
    words = []
    for token in lexer:
        if token and all(char in OPERATOR_CHARS for char in token):
            if words:
                yield words
            words = []
        else:
            words.append(token)
    if words:
        yield words


def commands_of(command):
    """The simple commands of a Bash call, line by line when the whole does not parse."""
    text = without_heredocs_and_comments(command.replace("\\\n", " "))
    try:
        return list(simple_commands(text))
    except ValueError:
        commands = []
        for line in text.split("\n"):
            try:
                commands.extend(simple_commands(line))
            except ValueError:
                continue
        return commands


def nested_scripts(words):
    """The script of `bash -c '…'`, or the text of `eval …`."""
    for start, word in enumerate(words):
        name = word.rsplit("/", 1)[-1]
        if name == "eval":
            return [" ".join(words[start + 1 :])]
        if name in SHELLS:
            for index in range(start + 1, len(words) - 1):
                option = words[index]
                if (
                    option.startswith("-")
                    and not option.startswith("--")
                    and "c" in option
                ):
                    return [words[index + 1]]
            return []
    return []


def git_subcommand(words):
    """The words from git's subcommand on, global options skipped, or None without git."""
    for index, word in enumerate(words):
        if word == "git" or word.endswith("/git"):
            rest = words[index + 1 :]
            position = 0
            while position < len(rest) and rest[position].startswith("-"):
                position += 2 if rest[position] in GIT_OPTIONS_WITH_VALUE else 1
            return rest[position:]
    return None


def refusal(words):
    """The reason to refuse this git subcommand, or None."""
    if not words:
        return None
    subcommand, args = words[0], words[1:]
    if "--" in args:
        args = args[: args.index("--")]  # what follows are paths
    longs = {arg.split("=", 1)[0] for arg in args if arg.startswith("--")}
    shorts = "".join(
        arg[1:] for arg in args if arg.startswith("-") and not arg.startswith("--")
    )
    plain = [arg for arg in args if not arg.startswith("-")]

    if subcommand == "checkout":
        return CHECKOUT
    if subcommand == "restore":
        staged = "--staged" in longs or "S" in shorts
        worktree = "--worktree" in longs or "W" in shorts
        if worktree or not staged:
            return RESTORE
    if subcommand == "reset" and "--hard" in longs:
        return RESET
    if subcommand == "clean":
        forced = "--force" in longs or "f" in shorts
        dry_run = "--dry-run" in longs or "n" in shorts
        if forced and not dry_run:
            return CLEAN
    if subcommand == "switch" and (
        longs & {"--force", "--discard-changes"} or "f" in shorts
    ):
        return SWITCH
    if subcommand == "stash" and plain[:1] in (["drop"], ["clear"]):
        return STASH
    if subcommand == "push":
        forced = (
            longs & {"--force", "--force-with-lease", "--force-if-includes"}
            or "f" in shorts
        )
        if forced or any(arg.startswith("+") for arg in plain):
            return PUSH
    return None


def check(command, depth=0):
    """The reason to refuse a Bash call, or None."""
    if depth > MAX_NESTING:
        return None
    for words in commands_of(command):
        for script in nested_scripts(words):
            reason = check(script, depth + 1)
            if reason:
                return reason
        reason = refusal(git_subcommand(words))
        if reason:
            return reason
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    tool_input = payload.get("tool_input") if isinstance(payload, dict) else None
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str):
        return 0
    reason = check(command)
    if reason:
        print(PREFIX + reason + SUFFIX, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
