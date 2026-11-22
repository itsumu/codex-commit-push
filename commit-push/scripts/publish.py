"""Commit the reviewed index and push just the selected branch."""
import os
import subprocess
import sys


def git(*args, capture=False):
    return subprocess.run(["git", *args], check=True, text=True,
                          stdout=subprocess.PIPE if capture else None).stdout


def value(*args):
    return git(*args, capture=True).strip()


def stop(message):
    raise SystemExit(message)


def main(branch, head, tree, remote, dest, message):
    ref = "refs/heads/" + branch
    dst = "refs/heads/" + dest
    if value("symbolic-ref", "HEAD") != ref:
        stop("Branch changed; review again.")
    git("check-ref-format", dst)
    if remote.startswith("-") or remote not in value("remote").splitlines():
        stop("Expected a named Git remote.")
    if len(value("remote", "get-url", "--push", "--all", remote).splitlines()) != 1:
        stop("Multiple push URLs; resolve destination first.")
    mirror = subprocess.run(["git", "config", "--bool", "--get", "remote."+remote+".mirror"],
                            capture_output=True, text=True)
    if mirror.returncode not in (0, 1) or mirror.stdout.strip() == "true":
        stop("Refusing mirror or invalid remote configuration.")
    for marker in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-apply", "rebase-merge", "sequencer"):
        if os.path.exists(value("rev-parse", "--git-path", marker)):
            stop("Finish the ongoing Git operation first.")
    current = subprocess.run(["git", "rev-parse", "--verify", "-q", "HEAD"], capture_output=True, text=True)
    if (current.stdout.strip() or "unborn") != head or value("write-tree") != tree:
        stop("HEAD or staged content changed; review again.")
    if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode != 1:
        stop("No reviewed changes to commit.")
    git("commit", "--file", message)
    sha = value("rev-parse", "HEAD")
    if value("rev-parse", "HEAD^{tree}") != tree or value("symbolic-ref", "HEAD") != ref:
        stop("Commit created, but branch or content changed during commit; not pushed: "+sha)
    setup = not value("for-each-ref", "--format=%(upstream)", ref)
    print("Created commit "+sha+"; pushing to "+remote+"/"+dest, flush=True)
    git("push", "--no-follow-tags", "--recurse-submodules=no", "--", remote, sha+":"+dst)
    if setup:
        result = subprocess.run(["git", "branch", "--set-upstream-to="+remote+"/"+dest, "--", branch])
        if result.returncode:
            print("Push succeeded, but tracking was not set.", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 7:
        stop("Usage: publish.py LOCAL_BRANCH HEAD TREE REMOTE DEST_BRANCH MESSAGE_FILE")
    try:
        main(*sys.argv[1:])
    except subprocess.CalledProcessError as error:
        sys.exit(error.returncode)
