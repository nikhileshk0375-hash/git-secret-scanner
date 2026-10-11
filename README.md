# Git Secret Scanner

A tool that scans a Git repository's full commit history for accidentally committed secrets: API keys, passwords, tokens, and private keys, even if they were later deleted in a newer commit.

## Why this matters
Deleting a secret and committing the fix does NOT remove it from Git history. The old commit still exists, and anyone with access to the repository (including the public, for public repos) can retrieve it. This tool finds those leaks before an attacker does.

## Features
- Scans every commit in a repo's history, not just the current files
- Detects AWS keys, GitHub tokens, Slack tokens, private keys, generic API keys/secrets/passwords
- Rates each finding as HIGH or MEDIUM severity
- Filters out common placeholder/example text to reduce false positives
- Deduplicates findings to the earliest commit where each secret appeared
- Two interfaces: a colorful terminal menu with a file picker, and a plain CLI
- Exports results as JSON

## Installation
```bash
git clone https://github.com/nikhileshk0375-hash/git-secret-scanner.git
cd git-secret-scanner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

**Main tool (recommended):** terminal menu with a folder picker.
```bash
python3 menu.py


**Plain CLI:**
```bash
python3 scanner.py --path /path/to/repo
python3 scanner.py --path /path/to/repo --output results.json


## Ethical use
This tool is meant for scanning your own repositories, or repositories you have permission to scan. Public GitHub repository history is already publicly visible, so scanning public repos for awareness is standard security practice. Using any secrets found to access systems without authorization is illegal, and is not the purpose of this tool.

## Limitations
- Regex-based detection can produce false positives and false negatives
- Does not scan binary files
- Does not automatically rotate or revoke found secrets, that's a manual step for the repository owner

## Built with
Python, GitPython, colorama, pyfiglet, Tkinter
