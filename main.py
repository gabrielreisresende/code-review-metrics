from github_api import get_pull_requests, get_pull_request_reviews, get_pull_request_comments
from data_collector import filter_pr, extract_metrics
from utils import read_repositories, save_to_csv

def main():
    repos = read_repositories("repos.csv")
    all_data = []

    for repo in repos:
        print(f"Coletando PRs de: {repo}")
        prs = get_pull_requests(repo)
        print(f"Numero de PRs coletados: {len(prs)}")

        for pr in prs:
            
            print(f"Repo: {repo} - Coletando reviews do PR: {pr['number']}")
            reviews = get_pull_request_reviews(repo, pr["number"])
            
            print(f"Repo: {repo} - Coletando comentarios do PR: {pr['number']}")
            comments = get_pull_request_comments(repo, pr["number"])

            if not filter_pr(pr, reviews):
                continue

            print(f"Repo: {repo} - Extraindo métricas do PR: {pr['number']}")
            metrics = extract_metrics(pr, reviews, comments)
            
            metrics["repo"] = repo
            all_data.append(metrics)

    save_to_csv(all_data, "pull_requests_metrics.csv")
    print(f"Coleta finalizada. Total de PRs válidos: {len(all_data)}")

if __name__ == "__main__":
    main()
