from github_api import get_pull_requests, get_pull_request_reviews, get_pull_request_comments
from data_collector import filter_pr, extract_metrics
from utils import read_repositories, save_to_csv
import os
import pandas as pd

OUTPUT_FILE = "pull_requests_metrics.csv"

def append_to_csv(data, filename):
    """Salva dados incrementalmente no CSV."""
    df = pd.DataFrame(data)
    file_exists = os.path.isfile(filename)

    df.to_csv(filename, mode='a', header=not file_exists, index=False)

def main():
    repos = read_repositories("repos.csv")

    for repo in repos:
        print(f"\n=== Coletando PRs de: {repo} ===")
        prs = get_pull_requests(repo)
        print(f"Numero total de PRs coletados: {len(prs)}")

        prs = prs[:100]
        print(f"Processando até 100 PRs deste repositório...")

        repo_data = []

        for pr in prs:
            try:
                print(f"Repo: {repo} - Coletando reviews do PR: {pr['number']}")
                reviews = get_pull_request_reviews(repo, pr["number"])

                print(f"Repo: {repo} - Coletando comentários do PR: {pr['number']}")
                comments = get_pull_request_comments(repo, pr["number"])

                if not filter_pr(pr, reviews):
                    continue

                print(f"Repo: {repo} - Extraindo métricas do PR: {pr['number']}")
                metrics = extract_metrics(pr, reviews, comments)
                metrics["repo"] = repo

                repo_data.append(metrics)

            except Exception as e:
                print(f" Erro ao processar PR {pr['number']} do repo {repo}: {e}")

        if repo_data:
            append_to_csv(repo_data, OUTPUT_FILE)
            print(f"Dados salvos para o repositório {repo} ({len(repo_data)} PRs válidos)")
        else:
            print(f"Nenhum PR válido encontrado para {repo}")

    print(f"Coleta finalizada. Resultados salvos em: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
