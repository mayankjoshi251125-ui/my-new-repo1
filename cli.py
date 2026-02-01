import typer
from app.github_tools import *
from app.readme_generator import generate_readme

app = typer.Typer()


@app.command()
def create_repo(
    name: str,
    description: str = typer.Option("", "--description", "-d", help="Repository description"),
):
    print(create_repository(name, description))


@app.command()
def commit(
    repo_url: str,
    message: str,
    files: list[str] = typer.Option(
        None,
        "--files",
        "-f",
        help="Local files to commit (can be used multiple times)",
    ),
):
    print(commit_and_push(repo_url, message, files))


@app.command()
def create_issue_cli(repo: str, title: str, body: str):
    print(create_issue(repo, title, body))


@app.command()
def create_pr_cli(
    repo: str,
    title: str,
    body: str,
    head: str,
    base: str = typer.Option("main", "--base", "-b", help="Base branch"),
):
    print(create_pull_request(repo, title, body, head, base))


@app.command()
def auto_pr(repo_url: str, title: str, body: str):
    print(auto_create_pr(repo_url, title, body))


@app.command()
def audit(repo: str):
    results = audit_repository(repo)
    print("\n".join(results))


@app.command()
def generate_readme_cli(project: str, features: str):
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(generate_readme(project, features))
    print("README.md generated successfully!")


if __name__ == "__main__":
    app()


