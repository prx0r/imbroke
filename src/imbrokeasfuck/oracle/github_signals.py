"""GitHub early-signal detection for opportunity discovery."""
from __future__ import annotations
import httpx
from typing import Any
from .opportunity import (
    Opportunity, GITHUB_EARLY_SIGNAL_REPOS, GITHUB_EARLY_SIGNAL_KEYWORDS,
    classify_reward, estimate_qdw_fit,
)

TIMEOUT = httpx.Timeout(15.0)


async def scan_github_repo(owner: str, repo: str) -> list[dict[str, Any]]:
    """Scan a GitHub repo for early-signal keywords in recent activity."""
    signals = []
    headers = {"Accept": "application/vnd.github.v3+json"}

    async with httpx.AsyncClient(timeout=TIMEOUT, headers=headers) as c:
        # Check recent commits for signal keywords
        try:
            r = await c.get(f"https://api.github.com/repos/{owner}/{repo}/commits", params={"per_page": 30})
            if r.status_code == 200:
                for commit in r.json()[:30]:
                    msg = commit.get("commit", {}).get("message", "").lower()
                    for kw in GITHUB_EARLY_SIGNAL_KEYWORDS:
                        if kw in msg:
                            signals.append({
                                "type": "commit",
                                "repo": f"{owner}/{repo}",
                                "message": commit.get("commit", {}).get("message", "")[:200],
                                "url": commit.get("html_url", ""),
                                "date": commit.get("commit", {}).get("author", {}).get("date", ""),
                                "keyword": kw,
                            })
                            break
        except Exception:
            pass

        # Check recent releases
        try:
            r = await c.get(f"https://api.github.com/repos/{owner}/{repo}/releases", params={"per_page": 5})
            if r.status_code == 200:
                for release in r.json()[:5]:
                    name = (release.get("name", "") + " " + release.get("body", "")).lower()
                    for kw in GITHUB_EARLY_SIGNAL_KEYWORDS:
                        if kw in name:
                            signals.append({
                                "type": "release",
                                "repo": f"{owner}/{repo}",
                                "name": release.get("name", ""),
                                "url": release.get("html_url", ""),
                                "date": release.get("published_at", ""),
                                "keyword": kw,
                            })
                            break
        except Exception:
            pass

        # Check recent issues with bounty/RFP keywords
        try:
            r = await c.get(f"https://api.github.com/repos/{owner}/{repo}/issues", params={
                "state": "open", "per_page": 20, "sort": "created", "direction": "desc",
            })
            if r.status_code == 200:
                for issue in r.json()[:20]:
                    title = issue.get("title", "").lower()
                    labels = [l.get("name", "").lower() for l in issue.get("labels", [])]
                    text = f"{title} {' '.join(labels)}"
                    for kw in ["bounty", "rfp", "reward", "grant", "help wanted", "funded"]:
                        if kw in text:
                            signals.append({
                                "type": "issue",
                                "repo": f"{owner}/{repo}",
                                "title": issue.get("title", ""),
                                "url": issue.get("html_url", ""),
                                "date": issue.get("created_at", ""),
                                "labels": labels,
                                "keyword": kw,
                            })
                            break
        except Exception:
            pass

        # Check README for signal keywords
        try:
            r = await c.get(f"https://api.github.com/repos/{owner}/{repo}/readme")
            if r.status_code == 200:
                import base64
                content = base64.b64decode(r.json().get("content", "")).decode("utf-8", errors="ignore").lower()
                for kw in GITHUB_EARLY_SIGNAL_KEYWORDS:
                    if kw in content:
                        signals.append({
                            "type": "readme",
                            "repo": f"{owner}/{repo}",
                            "url": f"https://github.com/{owner}/{repo}",
                            "keyword": kw,
                        })
                        break
        except Exception:
            pass

    return signals


async def scan_all_github_signals() -> list[dict[str, Any]]:
    """Scan all tracked repos for early signals."""
    import asyncio
    tasks = []
    for repo in GITHUB_EARLY_SIGNAL_REPOS:
        owner, name = repo.split("/")
        tasks.append(scan_github_repo(owner, name))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    all_signals = []
    for r in results:
        if isinstance(r, list):
            all_signals.extend(r)
    return all_signals


def signal_to_opportunity(signal: dict[str, Any]) -> Opportunity:
    """Convert a GitHub signal to an Opportunity."""
    repo = signal.get("repo", "")
    keyword = signal.get("keyword", "")
    msg = signal.get("message", "") or signal.get("title", "") or signal.get("name", "")

    kind = "builder_program"
    if keyword in ("bounty", "rfp", "reward", "funded"):
        kind = "bounty"
    elif keyword in ("hackathon", "contest"):
        kind = "hackathon"
    elif keyword in ("grant", "funding"):
        kind = "grant"
    elif keyword in ("testnet", "incentive"):
        kind = "testnet"
    elif keyword in ("miner", "challenge"):
        kind = "subnet"

    title = f"{repo}: {msg[:80]}"
    rating = classify_reward(kind, title, msg)
    fit = estimate_qdw_fit(title, msg, kind)

    return Opportunity(
        kind=kind,
        title=title,
        sponsor=repo.split("/")[0],
        discovered_at=signal.get("date", ""),
        reward_type="token_emission" if kind == "subnet" else "cash",
        reward_confidence=0.5,
        source="github",
        source_url=signal.get("url", f"https://github.com/{repo}"),
        source_data=signal,
        rating=rating,
        reuse_score=fit,
        recommendation="INVESTIGATE" if rating in ("A", "B") and fit > 0.6 else "MONITOR",
    )
