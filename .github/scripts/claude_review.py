#!/usr/bin/env python3
"""Claude PR Review Script for GitHub Actions."""

import argparse
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


def main():
    parser = argparse.ArgumentParser(description="Claude PR Review")
    parser.add_argument("--title", required=True, help="PR title")
    parser.add_argument("--body", default="", help="PR description")
    parser.add_argument("--diff", required=True, help="Git diff")
    parser.add_argument("--files", required=True, help="Changed files")
    args = parser.parse_args()

    prompt = f"""You are a code reviewer. Please review this Pull Request and provide constructive feedback.

## PR Title
{args.title}

## PR Description
{args.body if args.body else "No description provided"}

## Changed Files
{args.files}

## Diff
```diff
{args.diff[:50000]}
```

## Review Guidelines
Please review the code for:
1. **Code Quality**: Readability, maintainability, best practices
2. **Bugs**: Potential bugs or edge cases
3. **Security**: Security vulnerabilities
4. **Performance**: Performance issues
5. **Documentation**: Missing or unclear documentation

## Response Format
Please respond in the following format:

### Summary
Brief summary of the changes.

### Good Points
- List of positive aspects

### Suggestions
- List of improvement suggestions (if any)

### Overall
Your overall assessment (Approve / Request Changes / Comment)

---
Reviewed by Claude
"""

    review = call_claude_api(prompt)
    print(review)


if __name__ == "__main__":
    main()
