from datetime import datetime, timezone

def parse_datetime(dt_str):
    return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

def filter_pr(pr, reviews):
    """Aplica filtros:
    - Status merged ou closed
    - Pelo menos uma revisão
    - Tempo entre criação e fechamento >= 1 hora
    """
    

    if len(reviews) < 1:
        return False

    created_at = parse_datetime(pr["created_at"])
    closed_at = parse_datetime(pr["closed_at"]) if pr["closed_at"] else None
    if not closed_at:
        return False

    delta = closed_at - created_at
    if delta.total_seconds() < 3600:  # menos de 1 hora
        return False

    return True


def extract_metrics(pr, reviews, comments):
    """Extrai as métricas definidas."""
    additions = pr.get("additions", 0)
    deletions = pr.get("deletions", 0)
    changed_files = pr.get("changed_files", 0)

    created_at = parse_datetime(pr["created_at"])
    closed_at = parse_datetime(pr["closed_at"]) if pr["closed_at"] else created_at
    analysis_time_hours = (closed_at - created_at).total_seconds() / 3600

    description_length = len(pr.get("body") or "")

    participants = set()
    for r in reviews:
        if r["user"]:
            participants.add(r["user"]["login"])
    for c in comments:
        if c["user"]:
            participants.add(c["user"]["login"])

    total_comments = len(reviews) + len(comments)

    return {
        "pr_number": pr["number"],
        "state": "merged" if pr.get("merged_at") else "closed",
        "additions": additions,
        "deletions": deletions,
        "changed_files": changed_files,
        "analysis_time_hours": analysis_time_hours,
        "description_length": description_length,
        "participants_count": len(participants),
        "comments_count": total_comments
    }
