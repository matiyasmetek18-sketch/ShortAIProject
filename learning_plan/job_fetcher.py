from __future__ import annotations

import json
import re
from typing import Iterable, List, Optional

from .models import JobPosting
from .utils import clean_text, decode_duckduckgo_url, make_search_url, slugify_company


class JobSearchError(Exception):
    """Raised when the job posting cannot be found or parsed."""


class JobFetcher:
    USER_AGENT = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        try:
            import requests
        except ImportError as exc:
            raise JobSearchError(
                'Live job fetching requires the "requests" package. Run `pip install -r requirements.txt` '
                "or use --job-file with a saved description."
            ) from exc
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.USER_AGENT})

    def fetch(self, company: str, role: str, job_url: Optional[str] = None) -> JobPosting:
        company_summary = self._fetch_company_summary(company)
        if job_url:
            posting = self._extract_job_posting(job_url, company, role)
            posting.company_summary = company_summary
            return posting

        candidates = self._search_job_links(company, role)
        for candidate in candidates:
            try:
                posting = self._extract_job_posting(candidate, company, role)
            except Exception:
                continue
            if self._matches_target(posting, company, role):
                posting.company_summary = company_summary
                return posting

        raise JobSearchError(
            f'No public job posting found for "{company}" and role "{role}". '
            "Try a more specific title or provide --job-url / --job-file."
        )

    def _search_job_links(self, company: str, role: str) -> List[str]:
        queries = [
            f'"{company}" "{role}" software jobs',
            f'site:boards.greenhouse.io "{company}" "{role}"',
            f'site:jobs.lever.co "{company}" "{role}"',
            f'site:ashbyhq.com "{company}" "{role}"',
        ]
        results: List[str] = []
        for query in queries:
            soup = self._get_soup(make_search_url(query))
            for tag in soup.select(".result__title a, .result__url, a.result__a"):
                href = tag.get("href")
                if not href:
                    continue
                url = decode_duckduckgo_url(href)
                if url.startswith("http") and url not in results:
                    results.append(url)
            if results:
                break
        return results[:8]

    def _fetch_company_summary(self, company: str) -> Optional[str]:
        soup = self._get_soup(make_search_url(f"{company} software company"))
        for tag in soup.select(".result__title a, a.result__a"):
            href = tag.get("href")
            if not href:
                continue
            url = decode_duckduckgo_url(href)
            if any(blocked in url for blocked in ("linkedin.com", "wikipedia.org")):
                continue
            try:
                page = self._get_soup(url)
            except Exception:
                continue
            description = page.find("meta", attrs={"name": "description"})
            if description and description.get("content"):
                return clean_text(description["content"])
        return None

    def _extract_job_posting(self, url: str, company: str, role: str) -> JobPosting:
        soup = self._get_soup(url)
        posting = self._parse_json_ld(soup, url, company, role)
        if posting:
            return posting

        if "boards.greenhouse.io" in url:
            posting = self._parse_greenhouse_html(soup, url, company, role)
            if posting:
                return posting
        if "jobs.lever.co" in url:
            posting = self._parse_lever_html(soup, url, company, role)
            if posting:
                return posting

        title = clean_text(soup.title.text if soup.title else role)
        body = clean_text(" ".join(node.get_text(" ", strip=True) for node in soup.select("main, article, section")))
        if len(body) < 300:
            body = clean_text(soup.get_text(" ", strip=True))
        if not body:
            raise JobSearchError(f"Unable to parse job posting at {url}")

        return JobPosting(
            company=company,
            role=role,
            title=title,
            url=url,
            description=body,
            source="html",
        )

    def _parse_json_ld(
        self, soup, url: str, company: str, role: str
    ) -> Optional[JobPosting]:
        for script in soup.select('script[type="application/ld+json"]'):
            raw = script.string or script.get_text()
            if not raw:
                continue
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue
            for item in self._iterate_json_ld(data):
                if str(item.get("@type", "")).lower() != "jobposting":
                    continue
                description = clean_text(item.get("description", ""))
                if not description:
                    continue
                org = item.get("hiringOrganization", {}) or {}
                location = item.get("jobLocation", {}) or {}
                locality = location.get("address", {}).get("addressLocality")
                return JobPosting(
                    company=org.get("name") or company,
                    role=role,
                    title=item.get("title") or role,
                    url=item.get("url") or url,
                    description=description,
                    source="json-ld",
                    location=locality,
                )
        return None

    def _parse_greenhouse_html(
        self, soup, url: str, company: str, role: str
    ) -> Optional[JobPosting]:
        title = clean_text(soup.select_one("h1.app-title").get_text(" ", strip=True)) if soup.select_one("h1.app-title") else None
        body_node = soup.select_one("#content, .content, .section-wrapper")
        if body_node:
            return JobPosting(
                company=company,
                role=role,
                title=title or role,
                url=url,
                description=clean_text(body_node.get_text(" ", strip=True)),
                source="greenhouse-html",
            )
        return None

    def _parse_lever_html(
        self, soup, url: str, company: str, role: str
    ) -> Optional[JobPosting]:
        title = clean_text(soup.select_one(".posting-headline h2").get_text(" ", strip=True)) if soup.select_one(".posting-headline h2") else None
        body_nodes = soup.select(".section-wrapper, .posting-requirements, .posting-categories")
        if body_nodes:
            combined = " ".join(node.get_text(" ", strip=True) for node in body_nodes)
            return JobPosting(
                company=company,
                role=role,
                title=title or role,
                url=url,
                description=clean_text(combined),
                source="lever-html",
            )
        return None

    def _matches_target(self, posting: JobPosting, company: str, role: str) -> bool:
        text = f"{posting.title} {posting.description[:500]}".lower()
        company_ok = company.lower() in text or slugify_company(company) in slugify_company(posting.url or "")
        role_words = [word for word in re.split(r"\W+", role.lower()) if len(word) > 2]
        role_hits = sum(1 for word in role_words if word in text)
        return company_ok and role_hits >= max(1, len(role_words) // 2)

    def _iterate_json_ld(self, data: object) -> Iterable[dict]:
        if isinstance(data, dict):
            if "@graph" in data and isinstance(data["@graph"], list):
                for item in data["@graph"]:
                    if isinstance(item, dict):
                        yield item
            else:
                yield data
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    yield item

    def _get_soup(self, url: str):
        try:
            from bs4 import BeautifulSoup
        except ImportError as exc:
            raise JobSearchError(
                'Live job fetching requires the "beautifulsoup4" package. Run `pip install -r requirements.txt`.'
            ) from exc
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
