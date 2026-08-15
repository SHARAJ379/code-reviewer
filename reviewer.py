"""
reviewer.py
Usage: python reviewer.py <path_to_code_folder>
Scans code files, sends each to local qwen2.5:7b for review,
writes a markdown report (review_report.md).
"""

import os
import sys
import ollama

MODEL = "qwen2.5:7b"
EXTENSIONS = (".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".cpp", ".c")
MAX_CHARS = 6000  # skip/truncate huge files to keep it fast

PROMPT = """You are a senior software engineer doing a code review.
Review the following file for: bugs, security vulnerabilities, bad practices,
and readability issues. Be specific and concise. Use this format:

## Issues Found
- [Severity: High/Medium/Low] Description (line reference if possible)

## Suggestions
- Short bullet points

If the code is clean, say so briefly.

FILE: {filename}
CODE:
{code}
"""


def review_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()[:MAX_CHARS]

    prompt = PROMPT.format(filename=os.path.basename(filepath), code=code)
    response = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"].strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: python reviewer.py <folder_path>")
        return

    target = sys.argv[1]
    report_lines = [f"# Code Review Report\nFolder: {target}\n"]

    for root, _, files in os.walk(target):
        if "node_modules" in root or "venv" in root or ".git" in root:
            continue
        for file in files:
            if file.endswith(EXTENSIONS):
                filepath = os.path.join(root, file)
                print(f"Reviewing {filepath} ...")
                result = review_file(filepath)
                report_lines.append(f"\n---\n### {filepath}\n{result}\n")

    with open("review_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print("\nDone. See review_report.md")


if __name__ == "__main__":
    main()
