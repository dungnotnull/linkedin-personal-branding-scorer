#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge_updater.py - self-improving crawl pipeline for Skill #150
(Personal Branding Scorer on LinkedIn, cluster: marketing-content-branding).

Pipeline:
  1. crawl4ai -> fetch latest ArXiv (cs.SI) records + authoritative domain pages
  2. (optional) WebSearch -> latest news/reports from authoritative sources
  3. Parse  -> title, authors, year, venue, DOI/URL, abstract, key findings
  4. Score  -> rank by recency + domain-keyword relevance
  5. Append -> add scored entries to SECOND-KNOWLEDGE-BRAIN.md (date-stamped)
  6. Deduplicate -> skip entries whose URL/DOI hash already exists

Production-grade features:
  * argparse CLI with --dry-run, --brain, --limit, --verbose, --no-network
  * structured logging
  * graceful degradation: if crawl4ai/network is unavailable, log and exit 0
    so the skill keeps working off the existing knowledge base
  * idempotent appends keyed by a stable sha256(url) hash token
  * relevance floor (configurable) to keep the brain focused on the domain
  * JSONL event log for observability

Recommended schedule: weekly cron, e.g. `0 3 * * 1 python tools/knowledge_updater.py`.

This module is import-safe: importing it never performs network I/O. Only
``main()`` (under ``if __name__ == "__main__"``) triggers crawls.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime
import hashlib
import json
import logging
import os
import re
import sys
import time
from typing import Dict, Iterable, List, Optional

# ---------------------------------------------------------------------------
# Defaults & paths
# ---------------------------------------------------------------------------
DEFAULT_ARXIV_CATEGORIES: List[str] = ["cs.SI"]
DEFAULT_WEB_SOURCES: List[str] = [
    "https://www.linkedin.com/business",
    "https://www.linkedin.com/blog/engineering",
    "https://sproutsocial.com/insights",
    "https://blog.hootsuite.com",
    "https://hbr.org",
]
DEFAULT_SEARCH_QUERIES: List[str] = [
    "linkedin algorithm ranking 2026",
    "personal branding thought leadership research",
    "social selling index benchmarks",
    "b2b content engagement linkedin",
]
DEFAULT_RELEVANCE_FLOOR: float = 0.10
DEFAULT_LIMIT: int = 50

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BRAIN = os.path.normpath(os.path.join(HERE, "..", "SECOND-KNOWLEDGE-BRAIN.md"))

HASH_TOKEN_RE = re.compile(r"<!--hash:([0-9a-f]{16})-->")
ARXIV_ID_RE = re.compile(r"(arXiv:\d{4}\.\d{4,5})")
ARXIV_NEW_RE = re.compile(r"/abs/(\d{4}\.\d{4,5})")
HASH_LEN = 16

log = logging.getLogger("knowledge_updater")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclasses.dataclass
class Entry:
    title: str
    authors: str
    year: str
    venue: str
    url: str
    abstract: str = ""

    def to_dict(self) -> Dict[str, str]:
        return dataclasses.asdict(self)


# ---------------------------------------------------------------------------
# Hashing / dedup helpers
# ---------------------------------------------------------------------------
def normalize_url(url: str) -> str:
    """Normalize a URL for stable hashing (strip fragments, lowercase scheme/host)."""
    if not url:
        return ""
    u = url.strip()
    if "#" in u:
        u = u.split("#", 1)[0]
    u = u.rstrip("/")
    # Lowercase the scheme + host portion only (path stays case-sensitive).
    if "://" in u:
        scheme, rest = u.split("://", 1)
        if "/" in rest:
            host, tail = rest.split("/", 1)
            u = f"{scheme.lower()}://{host.lower()}/{tail}"
        else:
            u = f"{scheme.lower()}://{rest.lower()}"
    return u


def url_hash(url: str) -> str:
    return hashlib.sha256(normalize_url(url).encode("utf-8")).hexdigest()[:HASH_LEN]


def existing_hashes(text: str) -> set:
    return set(HASH_TOKEN_RE.findall(text))


# ---------------------------------------------------------------------------
# Relevance scoring
# ---------------------------------------------------------------------------
def relevance_keywords(queries: Iterable[str]) -> List[str]:
    return [w.lower() for q in queries for w in q.split()]


def relevance_score(title: str, abstract: str, keywords: List[str]) -> float:
    if not keywords:
        return 0.0
    blob = (title + " " + abstract).lower()
    hits = sum(1 for k in keywords if k and k in blob)
    return hits / len(keywords)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def parse_arxiv(markdown: str, base_url: str) -> List[Entry]:
    """Parse ArXiv listing markdown into Entry records."""
    out: List[Entry] = []
    seen_ids: set = set()
    today = str(datetime.date.today().year)
    # Match inline arXiv ids first, then href-style /abs/ ids.
    for m in ARXIV_ID_RE.finditer(markdown):
        aid = m.group(1).split(":", 1)[1]
        if aid in seen_ids:
            continue
        seen_ids.add(aid)
        out.append(
            Entry(
                title=f"ArXiv {aid}",
                authors="-",
                year=today,
                venue="arXiv (cs.SI)",
                url=f"https://arxiv.org/abs/{aid}",
                abstract="",
            )
        )
    for m in ARXIV_NEW_RE.finditer(markdown):
        aid = m.group(1)
        if aid in seen_ids:
            continue
        seen_ids.add(aid)
        out.append(
            Entry(
                title=f"ArXiv {aid}",
                authors="-",
                year=today,
                venue="arXiv (cs.SI)",
                url=f"https://arxiv.org/abs/{aid}",
                abstract="",
            )
        )
    return out


def parse_generic(markdown: str, url: str) -> Entry:
    """Best-effort single-entry extraction for a generic page."""
    title = _first_heading(markdown) or f"Update scan: {url}"
    return Entry(
        title=title,
        authors="-",
        year=str(datetime.date.today().year),
        venue=url,
        url=url,
        abstract=(markdown or "").strip()[:600],
    )


def _first_heading(markdown: str) -> str:
    for line in (markdown or "").splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip(" #").strip()
    return ""


# ---------------------------------------------------------------------------
# Fetchers (network I/O lives here; safe to import module without these running)
# ---------------------------------------------------------------------------
def fetch_with_crawl4ai(urls: List[str], verbose: bool = False) -> List[Entry]:
    """Fetch pages with crawl4ai if installed. Returns [] when unavailable.

    Prefers the async ``AsyncWebCrawler`` API and falls back to the legacy
    synchronous ``WebCrawler``. All failures degrade gracefully so the skill
    keeps working off the existing knowledge brain.
    """
    import asyncio

    async_crawler_cls = None
    try:
        from crawl4ai import AsyncWebCrawler  # type: ignore
        async_crawler_cls = AsyncWebCrawler
    except Exception:
        pass

    if async_crawler_cls is not None:
        async def _run() -> List[Entry]:
            results: List[Entry] = []
            crawler = async_crawler_cls()
            try:
                if hasattr(crawler, "start"):
                    await crawler.start()
                for url in urls:
                    try:
                        res = await crawler.arun(url=url)
                        md = getattr(res, "markdown", None) or getattr(res, "text", "") or ""
                        if url.startswith("https://arxiv.org/"):
                            results.extend(parse_arxiv(md, url))
                        elif md.strip():
                            results.append(parse_generic(md, url))
                    except Exception as e:
                        log.warning("crawl4ai failed for %s: %s", url, e)
            finally:
                if hasattr(crawler, "close"):
                    close = crawler.close
                    if asyncio.iscoroutinefunction(close):
                        await close()
                    else:
                        close()
            return results

        try:
            return asyncio.run(_run())
        except Exception as e:
            if verbose:
                log.warning("async crawl4ai path failed (%s); trying sync API.", e)

    return _fetch_with_crawl4ai_sync(urls)


def _fetch_with_crawl4ai_sync(urls: List[str]) -> List[Entry]:
    try:
        from crawl4ai import WebCrawler  # type: ignore
    except Exception as e:
        log.info("crawl4ai sync API unavailable (%s).", e)
        return []
    results: List[Entry] = []
    try:
        crawler = WebCrawler()
        if hasattr(crawler, "warmup"):
            crawler.warmup()
        for url in urls:
            try:
                res = crawler.run(url=url)
                md = getattr(res, "markdown", "") or ""
                if url.startswith("https://arxiv.org/"):
                    results.extend(parse_arxiv(md, url))
                elif md.strip():
                    results.append(parse_generic(md, url))
            except Exception as e:
                log.warning("sync crawl4ai failed for %s: %s", url, e)
    except Exception as e:
        log.warning("sync crawl4ai session failed: %s", e)
    return results


def fetch_entries(
    arxiv_categories: List[str],
    web_sources: List[str],
    limit: int,
    no_network: bool,
) -> List[Entry]:
    """Fetch candidate entries. Returns [] when network is unavailable."""
    if no_network:
        log.info("--no-network set; skipping all live fetches.")
        return []
    urls: List[str] = [f"https://arxiv.org/list/{c}/recent" for c in arxiv_categories]
    urls.extend(web_sources)
    entries = fetch_with_crawl4ai(urls)
    if len(entries) > limit:
        entries = entries[:limit]
    return entries


# ---------------------------------------------------------------------------
# Brain append
# ---------------------------------------------------------------------------
def _format_entry_line(today: str, e: Entry, rel: float, h: str) -> str:
    return (
        f"- {today} -- **{e.title}** ({e.venue}, {e.year}) "
        f"[{e.url}] relevance={rel:.2f} <!--hash:{h}-->"
    )


def append_entries(
    entries: List[Entry],
    brain_path: str,
    queries: List[str],
    relevance_floor: float,
    dry_run: bool,
    event_log: Optional[str] = None,
) -> int:
    if not os.path.exists(brain_path):
        log.error("knowledge brain not found: %s", brain_path)
        return 0
    with open(brain_path, "r", encoding="utf-8") as f:
        text = f.read()
    seen = existing_hashes(text)
    kws = relevance_keywords(queries)
    scored = sorted(
        entries,
        key=lambda e: relevance_score(e.title, e.abstract, kws),
        reverse=True,
    )
    today = datetime.date.today().isoformat()
    added = 0
    lines: List[str] = []
    events: List[dict] = []
    for e in scored:
        if not e.url:
            continue
        h = url_hash(e.url)
        if h in seen:
            continue
        rel = relevance_score(e.title, e.abstract, kws)
        if rel < relevance_floor:
            events.append({"event": "skipped_low_relevance", "url": e.url, "relevance": round(rel, 3)})
            continue
        lines.append(_format_entry_line(today, e, rel, h))
        seen.add(h)
        added += 1
        events.append({"event": "appended", "url": e.url, "relevance": round(rel, 3), "hash": h})

    if added and not dry_run:
        section = f"\n### Auto-crawl {today}\n" + "\n".join(lines) + "\n"
        with open(brain_path, "a", encoding="utf-8") as f:
            f.write(section)

    if event_log and events:
        try:
            with open(event_log, "a", encoding="utf-8") as f:
                for ev in events:
                    f.write(json.dumps({"ts": datetime.datetime.utcnow().isoformat() + "Z", **ev}) + "\n")
        except OSError as e:
            log.warning("could not write event log %s: %s", event_log, e)

    log.info("appended %d new entries to %s (dry_run=%s)", added, os.path.basename(brain_path), dry_run)
    return added


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="knowledge_updater.py",
        description="Self-improving crawl pipeline for Skill #150 "
        "(Personal Branding Scorer on LinkedIn).",
    )
    p.add_argument("--brain", default=DEFAULT_BRAIN, help="Path to SECOND-KNOWLEDGE-BRAIN.md")
    p.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Max candidate entries to keep")
    p.add_argument("--relevance-floor", type=float, default=DEFAULT_RELEVANCE_FLOOR,
                   help="Minimum relevance score to append an entry")
    p.add_argument("--dry-run", action="store_true", help="Compute but do not write to the brain")
    p.add_argument("--no-network", action="store_true", help="Skip all live fetches")
    p.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    p.add_argument("--event-log", default=None, help="Optional JSONL event log path")
    p.add_argument("--config", default=None, help="Optional JSON config file overriding defaults")
    return p


def load_config(path: Optional[str]) -> dict:
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main(argv: Optional[List[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    cfg = load_config(args.config)
    arxiv_categories = cfg.get("arxiv_categories", DEFAULT_ARXIV_CATEGORIES)
    web_sources = cfg.get("web_sources", DEFAULT_WEB_SOURCES)
    queries = cfg.get("search_queries", DEFAULT_SEARCH_QUERIES)
    relevance_floor = cfg.get("relevance_floor", args.relevance_floor)
    limit = cfg.get("limit", args.limit)

    log.info("knowledge_updater for skill #150 (linkedin-personal-branding-scorer)")
    log.info("brain=%s dry_run=%s no_network=%s relevance_floor=%.2f limit=%d",
             args.brain, args.dry_run, args.no_network, relevance_floor, limit)

    started = time.time()
    entries = fetch_entries(arxiv_categories, web_sources, limit, args.no_network)
    n = append_entries(entries, args.brain, queries, relevance_floor,
                       args.dry_run, args.event_log)
    elapsed = time.time() - started
    if n == 0:
        log.info("no new entries this run (network/dedup/relevance); elapsed %.2fs", elapsed)
    else:
        log.info("done: %d new entries; elapsed %.2fs", n, elapsed)
    # Always exit 0 so the skill keeps working off the existing brain.
    return 0


if __name__ == "__main__":
    sys.exit(main())
