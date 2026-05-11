#!/usr/bin/env python3
"""
Test Generation Agent for Microsoft Web Pages.

Workflow:
  1. Parse each HTML page in pages/ and extract testable elements
     (title, headings, internal links, external links, key text).
  2. Produce BDD Gherkin .feature files in features/.
  3. Optionally run pytest to execute those feature files.

Usage:
  python agent/test_generator_agent.py              # generate + run
  python agent/test_generator_agent.py --generate   # generate only
  python agent/test_generator_agent.py --run        # run only (features must exist)
"""

import argparse
import re as _re
import subprocess
import sys
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent
PAGES_DIR = BASE_DIR / "pages"
FEATURES_DIR = BASE_DIR / "features"


# ---------------------------------------------------------------------------
# HTML analysis
# ---------------------------------------------------------------------------

def _text(tag):
    return tag.get_text(strip=True)


def analyze_page(filepath: Path) -> dict:
    soup = BeautifulSoup(filepath.read_text(encoding="utf-8"), "html.parser")
    return {
        "title": soup.title.string.strip() if soup.title else "",
        "h1": [_text(h) for h in soup.find_all("h1")],
        "h2": [_text(h) for h in soup.find_all("h2")],
        "external_links": [
            {"text": _text(a), "href": a.get("href", ""), "target": a.get("target", "")}
            for a in soup.find_all("a", attrs={"target": "_blank"})
        ],
        "internal_links": [
            {"text": _text(a), "href": a.get("href", "")}
            for a in soup.find_all("a")
            if a.get("target") != "_blank"
        ],
        "key_texts": [
            _re.sub(r"\s+", " ", p.get_text(separator=" ", strip=True))
            for p in soup.find_all("p")
            if len(p.get_text(strip=True)) > 30
        ][:4],
    }


# ---------------------------------------------------------------------------
# Feature file generation
# ---------------------------------------------------------------------------

def _indent(text: str, spaces: int = 4) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else "" for line in text.splitlines())


def generate_feature(page_name: str, data: dict, background_step: str, nav_target: str, nav_step: str) -> str:
    """Build a complete Gherkin feature string from the analysed page data."""
    lines = [
        f"Feature: Microsoft {page_name} Page",
        f"  As a visitor to the Microsoft information site",
        f"  I want to view the {page_name} page",
        f"  So that I can find accurate information about Microsoft",
        "",
        "  Background:",
        f"    Given {background_step}",
        "",
    ]

    # --- title ---
    if data["title"]:
        lines += [
            "  Scenario: Page loads with the correct title",
            f'    Then the page title should be "{data["title"]}"',
            "",
        ]

    # --- h1 ---
    for h1 in data["h1"]:
        lines += [
            "  Scenario: Page displays the main heading",
            f'    Then I should see the heading "{h1}"',
            "",
        ]

    # --- h2 section headings ---
    for h2 in data["h2"]:
        safe = h2.replace('"', "'")
        lines += [
            f'  Scenario: Section "{safe}" is present',
            f'    Then I should see the heading "{safe}"',
            "",
        ]

    # --- key body text ---
    for snippet in data["key_texts"][:2]:
        # Use first ~60 chars as a reliable anchor
        anchor = snippet[:60].replace('"', "'")
        lines += [
            "  Scenario: Page contains expected body text",
            f'    Then the page body should contain "{anchor}"',
            "",
        ]

    # --- external links open in new tab ---
    if data["external_links"]:
        lines += ["  Scenario: External links open in a new browser tab"]
        first = True
        for link in data["external_links"]:
            safe = link["text"].replace('"', "'")
            keyword = "Then" if first else "And"
            lines += [
                f'    {keyword} the link "{safe}" should be present',
                f'    And the link "{safe}" should open in a new tab',
            ]
            first = False
        lines += [""]

    # --- navigation ---
    nav_links = [l for l in data["internal_links"] if nav_target in l["href"].lower()]
    if nav_links:
        nav_text = nav_links[0]["text"].replace('"', "'")
        lines += [
            "  Scenario: Navigation link is present and functional",
            f'    When I click the link "{nav_text}"',
            f"    Then {nav_step}",
            "",
        ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def generate_features():
    print("=" * 60)
    print("Test Generation Agent — Analysing pages")
    print("=" * 60)

    FEATURES_DIR.mkdir(exist_ok=True)

    pages = {
        "index.html": {
            "name": "Overview",
            "background_step": "I am on the Microsoft Overview page",
            "nav_target": "history",
            "nav_step": "I should be on the History page",
            "output": "microsoft_overview.feature",
        },
        "history.html": {
            "name": "History",
            "background_step": "I am on the Microsoft History page",
            "nav_target": "index",
            "nav_step": "I should be on the Overview page",
            "output": "microsoft_history.feature",
        },
    }

    for filename, cfg in pages.items():
        path = PAGES_DIR / filename
        if not path.exists():
            print(f"ERROR: {path} not found — skipping")
            continue

        data = analyze_page(path)
        print(f"\n{filename}:")
        print(f"  Title       : {data['title']}")
        print(f"  H1          : {data['h1']}")
        print(f"  H2 sections : {len(data['h2'])}")
        print(f"  Ext links   : {len(data['external_links'])}")
        print(f"  Int links   : {len(data['internal_links'])}")

        feature_text = generate_feature(
            page_name=cfg["name"],
            data=data,
            background_step=cfg["background_step"],
            nav_target=cfg["nav_target"],
            nav_step=cfg["nav_step"],
        )

        out_path = FEATURES_DIR / cfg["output"]
        out_path.write_text(feature_text, encoding="utf-8")
        print(f"  -> Generated : {out_path.relative_to(BASE_DIR)}")

    print("\nFeature generation complete.")


def run_tests():
    print("\n" + "=" * 60)
    print("Test Generation Agent — Running BDD tests")
    print("=" * 60 + "\n")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short",
         f"--html=reports/test-report.html", "--self-contained-html"],
        cwd=BASE_DIR,
    )

    print("\n" + "=" * 60)
    if result.returncode == 0:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED — see output above")
    print("=" * 60)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Generate BDD Gherkin test cases for Microsoft pages and run them."
    )
    parser.add_argument("--generate", action="store_true", help="Only generate feature files")
    parser.add_argument("--run", action="store_true", help="Only run existing tests")
    args = parser.parse_args()

    if args.generate:
        generate_features()
    elif args.run:
        sys.exit(run_tests())
    else:
        generate_features()
        sys.exit(run_tests())


if __name__ == "__main__":
    main()
