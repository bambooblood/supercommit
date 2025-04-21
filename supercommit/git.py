import typer
from git import GitCommandError, Repo


def get_repo(path: str):
    return Repo(path)


def get_current_branch(repo):
    return repo.active_branch.name


def stage_changes(repo):
    repo.git.add("--all")


def has_changes(repo):
    return repo.is_dirty(untracked_files=True)


def show_changes(repo):
    status = repo.git.status()
    typer.echo("📄 Status:\n")
    typer.echo(status)


def show_diff(repo):
    diff = repo.git.diff("HEAD")
    typer.echo("🔀 Diff with last commit:\n")
    typer.echo(diff)


def get_diff(repo):
    # TODO: Handle potential unexistent ref. Example, first commit
    return repo.git.diff("HEAD")


def commit_changes(repo, message):
    repo.index.commit(message)


def push_branch(repo, branch):
    try:
        repo.git.push("--set-upstream", "origin", branch)
        typer.echo(f"🚀 Pushed branch {branch} to origin.")
    except GitCommandError as e:
        typer.echo(f"⚠️ Push failed: {e}", err=True)
