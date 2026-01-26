# --------- Install ---------
!pip install -q google-genai requests

# --------- Imports ---------
import os
import requests
from typing import List, Dict
from google import genai
from google.colab import userdata

# --------- Secrets ---------
# Gemini API Key (required)
os.environ["GEMINI_API_KEY"] = userdata.get("GEMINI_API_KEY")

# GitHub token (optional, avoids rate limits)
GITHUB_TOKEN = userdata.get("GITHUB_TOKEN")

if not os.environ["GEMINI_API_KEY"]:
    raise RuntimeError("GEMINI_API_KEY not found in Colab Secrets")

# --------- Config ---------
GITHUB_API = "https://api.github.com"

# --------- Errors ---------
class GitHubRepoError(Exception):
    pass

# --------- GitHub Client ---------
def github_headers(raw: bool = False):
    headers = {}
    if raw:
        headers["Accept"] = "application/vnd.github.v3.raw"
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


def fetch_readme(owner: str, repo: str) -> str:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/readme"
    r = requests.get(url, headers=github_headers(raw=True), timeout=10)

    if r.status_code == 404:
        raise GitHubRepoError("README.md not found")
    if r.status_code != 200:
        raise GitHubRepoError(f"README fetch failed ({r.status_code})")

    return r.text


def fetch_repo_tree(owner: str, repo: str) -> List[str]:
    for branch in ("main", "master"):
        url = f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        r = requests.get(url, headers=github_headers(), timeout=10)
        if r.status_code == 200:
            return [item["path"] for item in r.json().get("tree", [])]

    raise GitHubRepoError("Repo tree fetch failed (no main/master branch)")


# --------- Repo Analyzer ---------
IMPORTANT_FILES = (
    "README.md",
    "requirements.txt",
    "pyproject.toml",
    "setup.py",
    "Dockerfile",
)

IMPORTANT_DIRS = (
    "src", "app", "api", "backend",
    "frontend", "tests", "docs"
)

def identify_key_elements(paths: List[str]) -> Dict:
    key_files, key_dirs = [], set()

    for p in paths:
        if p.endswith(IMPORTANT_FILES):
            key_files.append(p)
        for d in IMPORTANT_DIRS:
            if p.startswith(f"{d}/"):
                key_dirs.add(d)

    return {
        "key_files": sorted(key_files),
        "key_directories": sorted(key_dirs),
    }

# --------- Gemini Client ---------
def generate_guided_tour(
    readme: str,
    tree: List[str],
    highlights: Dict
) -> str:

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    prompt = f"""
You are a senior software engineer onboarding a new developer.

Create a **Guided Developer Tour**.

Include:
1. What the project is
2. What problem it solves
3. Who it is for
4. Architecture overview
5. Key files & directories
6. First steps for contributors

README:
{readme}

Repository structure (sample):
{tree[:200]}

Key elements:
{highlights}
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# --------- Pipeline ---------
def run_pipeline(owner: str, repo: str) -> str:
    print("Fetching README...")
    readme = fetch_readme(owner, repo)

    print("Fetching repo structure...")
    tree = fetch_repo_tree(owner, repo)

    print("Identifying key components...")
    highlights = identify_key_elements(tree)

    print("Generating guided tour...")
    return generate_guided_tour(readme, tree, highlights)

# --------- Run ---------
repo_input = input("Enter GitHub repo (owner/repo): ").strip()

try:
    if "/" not in repo_input:
        raise ValueError("Format must be owner/repo")

    owner, repo = repo_input.split("/", 1)
    tour = run_pipeline(owner, repo)

    print("\n" + "=" * 60)
    print("📘 GUIDED DEVELOPER TOUR")
    print("=" * 60 + "\n")
    print(tour)

except GitHubRepoError as e:
    print(f"GitHub error: {e}")
except Exception as e:
    print(f"Error: {e}")
