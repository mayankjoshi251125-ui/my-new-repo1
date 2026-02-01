from github import Github
from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from app.config import GITHUB_TOKEN

github = Github(GITHUB_TOKEN)


def create_repository(name, description=""):
    try:
        user = github.get_user()
        repo = user.create_repo(
            name=name,
            description=description,
            private=False,
            auto_init=True
        )
        return repo.clone_url
    except Exception as e:
        return f"GitHub Error: {str(e)}"


import tempfile
import shutil
from git import Repo
import os
from dotenv import load_dotenv
import os

load_dotenv()

def commit_and_push(repo_url: str, message: str, files: list[str] | None = None):
    import tempfile
    import shutil
    import os
    from git import Repo
    from dotenv import load_dotenv

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN not found")

    # Normalize URL
    repo_url = repo_url.replace(" ", "_")
    if not repo_url.endswith(".git"):
        repo_url += ".git"

    auth_repo_url = repo_url.replace("https://", f"https://{token}@")

    temp_dir = tempfile.mkdtemp()

    try:
        repo = Repo.clone_from(auth_repo_url, temp_dir)

        # ensure push uses token
        repo.remote("origin").set_url(auth_repo_url)

        # COPY FILES INTO TEMP REPO
        if files:
            for path in files:
                if not os.path.exists(path):
                    raise FileNotFoundError(f"File not found: {path}")

                dest = os.path.join(temp_dir, os.path.basename(path))
                shutil.copy(path, dest)

        repo.git.add(A=True)
        repo.index.commit(message)
        repo.remote(name="origin").push()

        return "Commit & push successful!"

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)





def create_issue(repo_name, title, body):
    try:
        repo = github.get_repo(repo_name)
        issue = repo.create_issue(title=title, body=body)
        return issue.html_url
    except Exception as e:
        return f"GitHub Error: {str(e)}"


def create_pull_request(repo: str, title: str, body: str, head: str, base: str = "main"):
    """
    repo: owner/repo
    head: branch name (example: feature/readme)
    base: target branch (default: main)
    """

    from github import Github
    import os

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN not found")

    g = Github(token)
    repository = g.get_repo(repo)

    owner = repo.split("/")[0]

    full_head = f"{owner}:{head}"

    pr = repository.create_pull(
        title=title,
        body=body,
        head=full_head,
        base=base
    )

    return pr.html_url




def audit_repository(repo_name):
    findings = []
    try:
        repo = github.get_repo(repo_name)

        try:
            repo.get_readme()
        except:
            findings.append("Missing README.md")

        try:
            repo.get_contents(".github/workflows")
        except:
            findings.append("Missing CI/CD workflows")

        try:
            repo.get_contents(".gitignore")
        except:
            findings.append("Missing .gitignore")

        return findings or ["Repository follows best practices."]

    except Exception as e:
        return [f"Audit Error: {str(e)}"]

def auto_create_pr(repo_url: str, title: str, body: str, branch: str = "feature/auto-pr", base: str = "main"):
    import tempfile
    import shutil
    from git import Repo
    import os
    from dotenv import load_dotenv
    from github import Github

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise ValueError("GITHUB_TOKEN not found")

    owner_repo = repo_url.replace("https://github.com/", "").replace(".git", "")
    owner = owner_repo.split("/")[0]

    auth_repo_url = repo_url.replace("https://", f"https://{token}@")

    temp_dir = tempfile.mkdtemp()

    try:
        repo = Repo.clone_from(auth_repo_url, temp_dir)

        repo.git.checkout("-b", branch)

        readme_path = os.path.join(temp_dir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# Auto Generated README\n\nCreated using AI automation.")

        repo.git.add(A=True)
        repo.index.commit(title)
        repo.remote(name="origin").push(branch)

        g = Github(token)
        gh_repo = g.get_repo(owner_repo)

        pr = gh_repo.create_pull(
            title=title,
            body=body,
            head=f"{owner}:{branch}",
            base=base
        )

        return pr.html_url

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


