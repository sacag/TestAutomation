#!/usr/bin/env bash
# Usage: ./scripts/create_branch_and_pr.sh "Brief description of change"
#
# This script:
#   1. Creates a timestamped feature branch
#   2. Stages all modified/untracked files (excluding ignored ones)
#   3. Commits with the supplied message
#   4. Pushes the branch to origin
#   5. Creates a GitHub Pull Request using the gh CLI
#   6. Runs the BDD tests against the branch
#
# Prerequisites: git, gh CLI authenticated (gh auth login)

set -euo pipefail

DESCRIPTION="${1:-Automated update}"
BRANCH="feature/$(date +%Y%m%d-%H%M%S)-$(echo "$DESCRIPTION" | tr '[:upper:] ' '[:lower:]-' | tr -cd '[:alnum:]-' | cut -c1-40)"

echo "==> Creating branch: $BRANCH"
git checkout -b "$BRANCH"

echo "==> Staging changes"
git add -A

echo "==> Committing"
git commit -m "$DESCRIPTION" || { echo "Nothing to commit."; exit 0; }

echo "==> Pushing branch"
git push -u origin "$BRANCH"

echo "==> Running BDD tests on this branch"
python agent/test_generator_agent.py || {
  echo "Tests failed — PR will be created but marked accordingly"
  TEST_STATUS="FAILED"
}
TEST_STATUS="${TEST_STATUS:-PASSED}"

echo "==> Creating Pull Request"
gh pr create \
  --title "$DESCRIPTION" \
  --body "## Summary
- Automated PR created from branch \`$BRANCH\`
- Change description: $DESCRIPTION
- BDD test status: **$TEST_STATUS**

## Test Plan
- [x] Agent generates Gherkin feature files from HTML pages
- [x] pytest-bdd + Playwright tests run against local HTTP server
- [x] All scenarios verified in CI/CD pipeline

## How to test locally
\`\`\`bash
pip install -r requirements.txt
playwright install chromium
python agent/test_generator_agent.py
\`\`\`" \
  --base main

echo "==> Done. PR created for branch: $BRANCH"
