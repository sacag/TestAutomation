"""
Root conftest.py — shared fixtures and all BDD step definitions.

Starts a local HTTP server so Playwright can load pages/index.html
and pages/history.html via http://localhost rather than file://.
"""

import http.server
import os
import re
import threading
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, parsers, then, when

PAGES_DIR = Path(__file__).parent / "pages"
SERVER_PORT = 8765


# ---------------------------------------------------------------------------
# HTTP server (session-scoped — starts once, shared across all tests)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def server_url():
    class _Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(PAGES_DIR), **kwargs)

        def log_message(self, fmt, *args):
            pass  # silence request logs

    server = http.server.HTTPServer(("localhost", SERVER_PORT), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://localhost:{SERVER_PORT}"
    server.shutdown()


# ---------------------------------------------------------------------------
# Given steps — navigation
# ---------------------------------------------------------------------------

@given("I am on the Microsoft Overview page")
def navigate_to_overview(page: Page, server_url: str):
    page.goto(f"{server_url}/index.html")
    page.wait_for_load_state("domcontentloaded")


@given("I am on the Microsoft History page")
def navigate_to_history(page: Page, server_url: str):
    page.goto(f"{server_url}/history.html")
    page.wait_for_load_state("domcontentloaded")


# ---------------------------------------------------------------------------
# Then steps — assertions
# ---------------------------------------------------------------------------

@then(parsers.parse('the page title should be "{title}"'))
def assert_page_title(page: Page, title: str):
    expect(page).to_have_title(title)


@then(parsers.parse('I should see the heading "{heading}"'))
def assert_heading_visible(page: Page, heading: str):
    locator = page.locator("h1, h2, h3").filter(has_text=heading)
    expect(locator.first).to_be_visible()


@then(parsers.parse('the page body should contain "{text}"'))
def assert_body_text(page: Page, text: str):
    # to_contain_text normalizes whitespace in both the element and the expected string
    expect(page.locator("body")).to_contain_text(text, ignore_case=True)


@then(parsers.parse('I should see text "{text}"'))
def assert_text_visible(page: Page, text: str):
    locator = page.get_by_text(text, exact=False)
    expect(locator.first).to_be_visible()


@then(parsers.parse('the link "{link_text}" should be present'))
def assert_link_present(page: Page, link_text: str):
    locator = page.get_by_role("link", name=link_text)
    expect(locator.first).to_be_visible()


@then(parsers.parse('the link "{link_text}" should open a reachable page in a new tab'))
def assert_link_reachable_new_tab(page: Page, link_text: str):
    link = page.get_by_role("link", name=link_text).first
    href = link.get_attribute("href")
    target = link.get_attribute("target")

    # 1. Verify target=_blank so the browser will open a new tab
    assert target == "_blank", (
        f"Link '{link_text}' must have target='_blank', got '{target}'"
    )

    # 2. Make an HTTP request to the href and confirm the URL is actually reachable
    response = page.request.get(href, timeout=30000)
    assert response.ok, (
        f"Link '{link_text}' ({href}) returned HTTP {response.status} — URL not reachable"
    )

    # 3. Click the link and capture the new tab that opens
    with page.context.expect_page() as new_page_info:
        link.click()
    new_tab = new_page_info.value
    new_tab.wait_for_load_state("domcontentloaded", timeout=30000)

    # 4. Confirm the new tab navigated to a real URL (not a browser error page)
    assert new_tab.url.startswith("http"), (
        f"Link '{link_text}' opened unexpected URL in new tab: {new_tab.url}"
    )
    assert not new_tab.url.startswith("chrome-error://"), (
        f"Link '{link_text}' ({href}) failed to load in new tab: {new_tab.url}"
    )
    new_tab.close()


@then("I should be on the History page")
def assert_on_history_page(page: Page):
    expect(page).to_have_url(re.compile(r"history\.html"))


@then("I should be on the Overview page")
def assert_on_overview_page(page: Page):
    expect(page).to_have_url(re.compile(r"index\.html"))


# ---------------------------------------------------------------------------
# When steps — interactions
# ---------------------------------------------------------------------------

@when(parsers.parse('I click the link "{link_text}"'))
def click_link(page: Page, link_text: str):
    page.get_by_role("link", name=link_text).first.click()
    page.wait_for_load_state("domcontentloaded")
