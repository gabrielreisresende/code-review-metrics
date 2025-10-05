import requests
import csv
from dotenv import load_dotenv
import os

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def fetch_popular_repos(language="Java", total=200):
    """Busca os repositórios mais populares por estrelas"""
    repos = []
    per_page = 100
    pages = (total // per_page) + (1 if total % per_page else 0)

    for page in range(1, pages + 1):
        query = f"language:{language}" if language else ""
        url = (
            f"https://api.github.com/search/repositories"
            f"?q={query}&sort=stars&order=desc&per_page={per_page}&page={page}"
        )
        print(f"🔸 Buscando página {page} de repositórios...")
        resp = requests.get(url, headers=HEADERS)

        if resp.status_code != 200:
            print(f"Erro ao buscar repositórios: {resp.status_code} - {resp.text}")
            break

        data = resp.json()
        items = data.get("items", [])
        repos.extend(items)

        if len(items) == 0:
            break

    return repos[:total]

def save_repos_to_csv(repos, filename="repos.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["full_name"])  # cabeçalho
        for repo in repos:
            writer.writerow([repo["full_name"]])
    print(f"Arquivo {filename} criado com {len(repos)} repositórios.")

def main():
    print("Gerando lista de repositórios mais populares...")
    repos = fetch_popular_repos(total=200)
    save_repos_to_csv(repos)

if __name__ == "__main__":
    main()
