#!/usr/bin/env python3
"""Claude PR Review Script."""

import os
import urllib.request
import urllib.error
import json


def call_claude_api(prompt: str) -> str:
    """Call Claude API."""
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
        "max_tokens": 2048,
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


def read_file(path: str, max_chars: int = 15000) -> str:
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
    body = os.environ.get("PR_BODY", "")[:1000]
    diff = read_file("/tmp/pr_diff.txt", 15000)
    files = read_file("/tmp/changed_files.txt", 500)

    prompt = f"""あなたは厳格なコードレビュアーです。このPRを批判的にレビューしてください。

## PR: {title}
{body}

## 変更ファイル
{files}

## Diff
```
{diff}
```

## レビュー観点（必ず全てチェック）
1. **バグ**: ロジックエラー、off-by-oneエラー、エッジケースの未処理
2. **セキュリティ**: コマンドインジェクション、入力検証の欠如
3. **例外処理**: 空リスト、null、ゼロ除算などの未処理
4. **副作用**: 引数の意図しない変更
5. **パフォーマンス**: 非効率なアルゴリズム

## 回答形式（日本語）

### 概要
変更内容を1-2文で要約

### 検出された問題
問題がある場合は具体的に指摘:
- 🔴 **重大**: [問題の説明と修正案]
- 🟡 **警告**: [問題の説明と修正案]
- 🔵 **提案**: [改善案]

問題がなければ「問題なし」

### 判定
- **Approve**: 問題なし
- **Request Changes**: 重大な問題あり（マージ前に修正必須）
- **Comment**: 軽微な問題あり

---
🤖 Claude Sonnet Review
"""

    print(call_claude_api(prompt))


if __name__ == "__main__":
    main()
