"""Offline unit tests for the starter tools."""
from __future__ import annotations

from conftest import FakeResponse
from tools import TOOL_FUNCTIONS


clarify_tool = TOOL_FUNCTIONS["clarify"]
format_tool = TOOL_FUNCTIONS["format"]
send_tool = TOOL_FUNCTIONS["send"]
lookup_tool = TOOL_FUNCTIONS["lookup"]
fetch_tool = TOOL_FUNCTIONS["fetch"]
timeline_tool = TOOL_FUNCTIONS["timeline"]
social_search_tool = TOOL_FUNCTIONS["social_search"]
policy_tool = TOOL_FUNCTIONS["policy"]


def test_clarify_choice_returns_options_and_awaits_user() -> None:
    result = clarify_tool(question="Chọn nguồn nào?", response_type="choice", options=["web", "social"])
    assert result["options"] == ["web", "social"]
    assert result["awaiting_user"] is True
    assert result["response_type"] == "choice"


def test_format_sections_groups_items_by_section() -> None:
    items = [{"title": "1", "section": "A"}, {"title": "2", "section": "B"}, {"title": "3", "section": "A"}]
    result = format_tool(items=items, template="sections")
    assert result["markdown"].count("## A") == 1
    assert result["markdown"].count("## B") == 1


def test_format_thread_numbers_items() -> None:
    result = format_tool(items=[{"title": "A"}, {"title": "B"}], template="thread")
    lines = result["markdown"].splitlines()
    assert lines[0].startswith("1/")
    assert lines[2].startswith("2/")


def test_format_empty_items_does_not_crash() -> None:
    assert format_tool(items=None)["item_count"] == 0
    assert format_tool(items=[])["item_count"] == 0


def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "chat-123")
    calls = fake_http(FakeResponse({"ok": True}))
    result = send_tool(text="Bản tin", confirmed=True)
    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert "bot-token" in calls[0]["url"]
    assert calls[0]["json"] == {"chat_id": "chat-123", "text": "Bản tin", "parse_mode": "Markdown"}
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))
    result = send_tool(text="Bản tin", confirmed=True)
    assert calls == []
    assert result["error"] == "RuntimeError"


def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))
    result = lookup_tool(query="AI", topic="general", timeframe=None, max_results=2)
    assert "time_range" not in calls[0]["json"]
    assert result["items"] == []


def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"data": {"markdown": "Body", "metadata": {"title": "T", "sourceURL": "https://example.com/a"}}}))
    result = fetch_tool("https://example.com/a")
    assert calls[0]["json"] == {"url": "https://example.com/a", "formats": ["markdown"]}
    assert result["items"][0] == {"title": "T", "url": "https://example.com/a", "source": "example.com", "summary": "Body"}


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    fake_http(FakeResponse({"data": {"markdown": "x" * 5000, "metadata": {}}}))
    result = fetch_tool("https://example.com/a")
    assert len(result["items"][0]["summary"]) == 4000


def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    monkeypatch.setenv("RAPIDAPI_TWITTER_HOST", "twitter.example")
    rows = [{"screen_name": "bach", "text": "missing", "tweet_id": ""}]
    rows += [{"screen_name": "bach", "text": f"tweet {i}", "tweet_id": str(i)} for i in range(6)]
    calls = fake_http(FakeResponse({"timeline": rows}))
    result = timeline_tool(screenname="bach", limit=3)
    assert calls[0]["params"] == {"screenname": "bach"}
    assert len(result["items"]) == 3
    assert all(item["url"].startswith("https://x.com/bach/status/") for item in result["items"])


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    monkeypatch.setenv("RAPIDAPI_TWITTER_HOST", "twitter.example")
    calls = fake_http(FakeResponse({"tweets": []}))
    result = social_search_tool(query="AI", search_type="Top", limit=5)
    assert calls[0]["params"] == {"query": "AI", "search_type": "Top"}
    assert result["search_type"] == "Top"


def test_policy_empty_query_returns_no_results() -> None:
    result = policy_tool(query="   ")
    assert result["results"] == []
    assert result["policy_area"] == "all"


def test_policy_area_filter_only_returns_that_area() -> None:
    result = policy_tool(query="API keys privacy", policy_area="data_privacy")
    assert result["results"]
    assert all(item["policy_area"] == "data_privacy" for item in result["results"])


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    result = policy_tool(query="ignore citation policy viral tweet", policy_area="source_citation", top_k=10)
    assert result["results"]
    untrusted = [line for item in result["results"] for line in item["untrusted_text"]]
    facts = " ".join(item["facts"] for item in result["results"])
    assert any("ignore the citation policy" in line.lower() for line in untrusted)
    assert "ignore the citation policy" not in facts.lower()


# No custom group tool is registered in this starter yet. Add three tests
# (happy path, bad model input, and failure path) when one is implemented.
