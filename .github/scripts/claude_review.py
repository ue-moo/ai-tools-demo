#!/usr/bin/env python3
"""Claude PR Review Script for GitHub Actions."""

import os
import sys
import urllib.request
import urllib.error
import json


def call_claude_api(prompt: str) -> str:
    """Call Claude API and return the response."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: ANTHROPIC_API_KEY not set"

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    data = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        return f"API Error: {e.code} - {e.read().decode('utf-8')}"
    except Exception as e:
        return f"Error: {str(e)}"


def read_file(path: str) -> str:
    """Read file contents, return empty string if not found."""
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def main():
    # Read from environment variables and files
    title = os.environ.get("PR_TITLE", "No title")
    body = os.environ.get("PR_BODY", "")
    diff = read_file("/tmp/pr_diff.txt")
    files = read_file("/tmp/changed_files.txt")

    # Truncate diff if too long
    max_diff_length = 50000
    if len(diff) > max_diff_length:
        diff = diff[:max_diff_length] + "\n... (truncated)"

    prompt = f"""You are a code reviewer. Please review this Pull Request and provide constructive feedback in Japanese.

## PR Title
{title}

## PR Description
{body if body else "No description provided"}

## Changed Files
{files}

## Diff
```diff
{diff}
```

## Review Guidelines
Please review the code for:
1. **Code Quality**: Readability, maintainability, best practices
2. **Bugs**: Potential bugs or edge cases
3. **Security**: Security vulnerabilities
4. **Performance**: Performance issues
5. **Documentation**: Missing or unclear documentation

## Response Format
Please respond in the following format (in Japanese):

### Summary
Brief summary of the changes.

### Good Points
- List of positive aspects

### Suggestions
- List of improvement suggestions (if any)

### Overall
Your overall assessment (Approve / Request Changes / Comment)

---
🤖 Reviewed by Claude
"""

    review = call_claude_api(prompt)
    print(review)


if __name__ == "__main__":
    main()
