from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from tools._shared import err


def verify(claim: str = "", sources: list[dict[str, str]] | None = None) -> dict[str, Any]:
    """Compare agent-reviewed evidence; stance labels are supplied, not inferred."""
    try:
        if not isinstance(claim, str) or not claim.strip():
            raise ValueError("claim must be a non-empty string")
        if not isinstance(sources, list):
            raise ValueError("sources must be a list of cited evidence")
        domains = set()
        stances = set()
        for source in sources:
            if not isinstance(source, dict):
                raise ValueError("Each source must be an object")
            url, quote, stance = (source.get(key) for key in ("url", "quote", "stance"))
            if not isinstance(url, str):
                raise ValueError("Each source needs an HTTP(S) URL")
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https") or not parsed.hostname:
                raise ValueError("Each source needs an HTTP(S) URL")
            if not isinstance(quote, str) or not quote.strip():
                raise ValueError("Each source needs a non-empty evidence quote")
            if stance not in ("supports", "contradicts", "unclear"):
                raise ValueError("stance must be supports, contradicts, or unclear")
            domains.add(parsed.hostname.removeprefix("www."))
            stances.add(stance)
        # ponytail: distinct hosts only approximate independence; check publisher ownership manually.
        if {"supports", "contradicts"} <= stances:
            status = "conflicting"
        elif len(domains) < 2 or "unclear" in stances or not stances:
            status = "insufficient_evidence"
        elif stances == {"supports"}:
            status = "corroborated"
        else:
            status = "contradicted"
        return {"tool": "verify", "claim": claim.strip(), "status": status,
                "source_count": len(domains), "sources": sources}
    except Exception as exc:
        return err("verify", exc)
