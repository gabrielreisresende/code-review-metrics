import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

BASE_URL = "https://api.github.com"

def get_paginated(url, params=None):
    """Faz requisições paginadas à API do GitHub."""
    results = []
    page = 1
    while True:
        if params is None:
            params = {}
        params.update({"per_page": 100, "page": page})
        resp = requests.get(url, headers=HEADERS, params=params)
        if resp.status_code != 200:
            print(f"Erro na requisição: {resp.status_code} - {resp.text}")
            break
        data = resp.json()
        if not data:
            break
        results.extend(data)
        page += 1
    return results


def get_pull_requests(repo_full_name):
    """Obtém PRs com status merged ou closed de um repositório."""
    url = f"{BASE_URL}/repos/{repo_full_name}/pulls"
    params = {"state": "all", "sort": "created", "direction": "desc"}
    return get_paginated(url, params)


def get_pull_request_reviews(repo_full_name, pr_number):
    """Obtém as revisões de um PR."""
    url = f"{BASE_URL}/repos/{repo_full_name}/pulls/{pr_number}/reviews"
    return get_paginated(url)


def get_pull_request_comments(repo_full_name, pr_number):
    """Obtém comentários de um PR (conversas de revisão)."""
    url = f"{BASE_URL}/repos/{repo_full_name}/issues/{pr_number}/comments"
    return get_paginated(url)
