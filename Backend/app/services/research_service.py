"""
Web Research Service.

Performs real-time internet research using Tavily API.
Includes retry logic with exponential backoff for reliability.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from tavily import TavilyClient
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.utils.logger import get_logger
from app.utils.validators import sanitize_text

logger = get_logger(__name__)


@dataclass
class ResearchResult:
    """Single web research result."""
    title: str
    url: str
    content: str
    score: float = 0.0


@dataclass
class ResearchContext:
    """Aggregated research context from multiple sources."""
    query: str
    results: List[ResearchResult] = field(default_factory=list)
    summary: str = ""


class ResearchService:
    """
    Web research service using Tavily API.

    Generates multiple search queries from the topic,
    retrieves results, deduplicates, and compiles a
    unified research context for AI content generation.
    """

    def __init__(self, api_key: str, max_results: int = 5) -> None:
        self._client = TavilyClient(api_key=api_key)
        self._max_results = max_results
        logger.info("ResearchService initialized | max_results=%d", max_results)

    def _generate_queries(self, topic: str, academic_level: str) -> List[str]:
        """Generate diverse search queries for comprehensive coverage."""
        return [
            f"{topic} overview and introduction",
            f"{topic} recent research and developments 2025 2026",
            f"{topic} applications and real-world use cases",
            f"{topic} advantages disadvantages and challenges",
            f"{topic} future trends and scope {academic_level} level",
        ]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        reraise=True,
    )
    def _search_single(self, query: str) -> List[ResearchResult]:
        """
        Perform a single Tavily search with retry logic.

        Args:
            query: Search query string.

        Returns:
            List[ResearchResult]: Parsed search results.
        """
        try:
            response = self._client.search(
                query=query,
                max_results=self._max_results,
                search_depth="advanced",
                include_answer=True,
            )

            results = []
            for item in response.get("results", []):
                content = sanitize_text(item.get("content", ""))
                if content and len(content) > 50:
                    results.append(ResearchResult(
                        title=item.get("title", "Unknown"),
                        url=item.get("url", ""),
                        content=content,
                        score=item.get("score", 0.0),
                    ))

            logger.info("Search OK | query='%s' | results=%d", query[:60], len(results))
            return results

        except Exception as e:
            logger.error("Search failed | query='%s' | error=%s", query[:60], str(e))
            raise

    def research_topic(self, topic: str, academic_level: str) -> ResearchContext:
        """
        Perform comprehensive multi-query research on a topic.

        Args:
            topic: Assignment topic.
            academic_level: Academic level for depth adjustment.

        Returns:
            ResearchContext: Compiled research with summary.
        """
        logger.info("Starting research | topic='%s' | level=%s", topic, academic_level)

        queries = self._generate_queries(topic, academic_level)
        all_results: List[ResearchResult] = []
        seen_urls: set = set()

        for query in queries:
            try:
                results = self._search_single(query)
                for result in results:
                    if result.url not in seen_urls:
                        seen_urls.add(result.url)
                        all_results.append(result)
            except Exception:
                logger.warning("Skipping failed query | query='%s'", query[:60])
                continue

        # Sort by relevance
        all_results.sort(key=lambda r: r.score, reverse=True)

        # Build summary from top results
        summary_parts = [r.content for r in all_results[:10] if r.content]
        summary = "\n\n".join(summary_parts)

        context = ResearchContext(
            query=topic,
            results=all_results,
            summary=summary[:8000],  # Cap summary length for token limits
        )

        logger.info(
            "Research completed | topic='%s' | total_results=%d | summary_len=%d",
            topic, len(all_results), len(context.summary),
        )
        return context