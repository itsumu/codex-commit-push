# codex-commit-push

[简体中文](README.md) | **English**

Use Codex to write a commit message from your Git diff, commit the reviewed changes, and push the current branch. The tool runs the Codex CLI and Git on your machine. It does not host your repository or require a separate GitHub token.

## Installation

On macOS or Linux, you need Git, Python 3, and a signed-in Codex CLI. Pushes use your existing Git credentials.

```sh
git clone https://github.com/itsumu/codex-commit-push.git
cd codex-commit-push
sh install.sh
```

The installer copies the skill to `${CODEX_HOME:-$HOME/.codex}/skills/commit-push` and adds a global Git alias. It will not overwrite a skill or alias with the same name but different contents.

## Usage

From the repository you want to commit to, run:

```sh
git codex-push
```

You can also enter `$commit-push` in a Codex chat. Both ask Codex to **commit and push**, not just preview a message. If you have staged changes, only those changes are included by default. Otherwise, Codex reviews the working tree and selects relevant changes. It does not create empty commits. To target a specific repository, use `git -C <path-to-repo> codex-push`.

Codex shows the proposed message, the changes to include, and the destination remote and branch. Before committing, the helper checks that HEAD, the branch, and the reviewed staging area still match. It respects Git hooks and signing settings and never force-pushes. If the push is rejected, the commit stays local. Always check what will be included: Codex can miss sensitive data or misinterpret a change.

## Tests

Run the tests from this tool's repository. They push only to a temporary local bare repository:

```sh
python3 -m unittest discover -s tests
```

## Uninstall

From this tool's repository, run:

```sh
sh install.sh --uninstall
```

The uninstaller removes only the skill files and alias that match this version. It does not delete repositories or undo commits.
