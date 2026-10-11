import argparse
import json
import git
from colorama import Fore, Style, init
from patterns import find_secrets

init(autoreset=True)

SEVERITY = {
    "AWS Access Key": "HIGH",
    "Private Key Header": "HIGH",
    "GitHub Token": "HIGH",
    "Slack Token": "HIGH",
    "Generic Secret": "MEDIUM",
    "Generic API Key": "MEDIUM",
    "Generic Token": "MEDIUM",
    "Password Assignment": "MEDIUM",
}

SEVERITY_COLOR = {"HIGH": Fore.RED, "MEDIUM": Fore.YELLOW, "LOW": Fore.GREEN}


def scan_repo(repo_path):
    repo = git.Repo(repo_path)
    seen = {}

    commits = list(repo.iter_commits(reverse=True))
    print(Fore.CYAN + f"Scanning {len(commits)} commits in {repo_path} ...\n")

    for commit in commits:
        parent = commit.parents[0] if commit.parents else git.NULL_TREE
        diffs = commit.diff(parent, create_patch=True)

        for d in diffs:
            if d.diff is None:
                continue
            try:
                text = d.diff.decode("utf-8", errors="ignore")
            except Exception:
                continue

            secrets = find_secrets(text)
            for secret_type, matched in secrets:
                key = (d.b_path or d.a_path, secret_type, matched)
                if key not in seen:
                    seen[key] = {
                        "commit": commit.hexsha[:7],
                        "date": commit.committed_datetime.strftime("%Y-%m-%d"),
                        "file": d.b_path or d.a_path,
                        "type": secret_type,
                        "match": matched,
                        "severity": SEVERITY.get(secret_type, "MEDIUM"),
                    }

    return list(seen.values())


def print_report(results):
    if not results:
        print(Fore.GREEN + Style.BRIGHT + "No secrets found in commit history. ✅")
        return

    high = [r for r in results if r["severity"] == "HIGH"]
    medium = [r for r in results if r["severity"] == "MEDIUM"]

    print(Fore.WHITE + Style.BRIGHT + f"Found {len(results)} potential secret(s)")
    print(Fore.RED + f"  HIGH: {len(high)}" + Fore.WHITE + "   " +
          Fore.YELLOW + f"MEDIUM: {len(medium)}")
    print(Fore.CYAN + "-" * 60)

    for r in sorted(results, key=lambda x: x["severity"]):
        color = SEVERITY_COLOR[r["severity"]]
        print(f"\n{color}{Style.BRIGHT}[{r['severity']}] {r['type']}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}File:    {r['file']}")
        print(f"  {Fore.WHITE}Commit:  {r['commit']}  ({r['date']})")
        print(f"  {Fore.WHITE}Match:   {Fore.YELLOW}{r['match']}")

    print(Fore.CYAN + "\n" + "-" * 60)
    print(Fore.WHITE + "Tip: these secrets exist permanently in Git history.")
    print(Fore.WHITE + "Rotate/revoke them, don't just delete the line, delete won't remove history.")


def main():
    parser = argparse.ArgumentParser(
        description="Git Secret Scanner: find secrets hidden in a repo's commit history."
    )
    parser.add_argument("--path", required=True, help="path to the Git repository to scan")
    parser.add_argument("--output", help="save results as JSON to this file")
    args = parser.parse_args()

    results = scan_repo(args.path)
    print()
    print_report(results)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(Fore.CYAN + f"\nSaved results to {args.output}")


if __name__ == "__main__":
    main()
