#!/usr/bin/env python3
"""Claude PR Review Script - Optimized for low cost."""

import os
import urllib.request
import urllib.error
import json


def call_claude_api(prompt: str) -> str:
    """Call Claude API with Haiku model for cost efficiency."""
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
        "model": "claude-3-5-haiku-20241022",  # Haiku: ~12x cheaper than Sonnet
        "max_tokens": 1024,  # Reduced from 4096
        "messages": [{"role": "user", "content": prompt}],
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        return f"API Error: {e.code} - {e.read().decode('utf-8')}"
    except Exception as e:
        return f"Error: {str(e)}"


def read_file(path: str, max_chars: int = 10000) -> str:
    """Read file contents with character limit."""
    try:
        with open(path, "r") as f:
            content = f.read()
            if len(content) > max_chars:
                return content[:max_chars] + "\n...(truncated)"
            return content
    except FileNotFoundError:
        return ""


def main():
    title = os.environ.get("PR_TITLE", "")
    body = os.environ.get("PR_BODY", "")[:500]  # Limit body
    diff = read_file("/tmp/pr_diff.txt", 10000)  # Reduced from 50000
    files = read_file("/tmp/changed_files.txt", 500)

    prompt = f"""PRをレビューして簡潔にフィードバックしてください。

## PR: {title}
{body}

## 変更ファイル
{files}

## Diff
```
{diff}
```

以下の形式で回答（日本語、簡潔に）:

### 概要
1-2文で変更内容を要約

### 良い点
- 箇条書き

### 改善提案
- 箇条書き（なければ「特になし」）

### 判定
Approve / Request Changes / Comment

---
🤖 Claude Haiku Review
"""

    print(call_claude_api(prompt))


if __name__ == "__main__":
    main()
