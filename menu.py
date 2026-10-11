
import os
import json
from pathlib import Path
from colorama import Fore, Style, init
import pyfiglet
import tkinter as tk
from tkinter import filedialog
import git
from scanner import scan_repo, print_report

init(autoreset=True)


def clear():
    os.system("clear")


def banner():
    clear()
    print(Fore.CYAN + pyfiglet.figlet_format("SecretScan", font="slant"))
    print(Fore.CYAN + "=" * 60)
    print(Fore.WHITE + " Git Secret Scanner" + Fore.GREEN + "  v1.0")
    print(Fore.WHITE + " Author : " + Fore.YELLOW + "nikhileshk0375-hash")
    print(Fore.WHITE + " Github : " + Fore.YELLOW + "github.com/nikhileshk0375-hash/git-secret-scanner")
    print(Fore.CYAN + "=" * 60 + "\n")


def menu():
    print(Fore.GREEN + " [1] " + Fore.WHITE + "Scan a repository")
    print(Fore.GREEN + " [2] " + Fore.WHITE + "Scan and save results as JSON")
    print(Fore.GREEN + " [0] " + Fore.WHITE + "Exit")
    print(Fore.CYAN + "-" * 60)


def pick_folder():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    root.update()
    folder = filedialog.askdirectory(
        title="Select a Git repository folder",
        initialdir=str(Path.home())  # starts at /home/shoonya instead of current folder
    )
    root.destroy()
    print(Fore.WHITE + f"(You selected: {folder})")  # debug line so we can see what was picked
    return folder

def is_git_repo(path):
    try:
        git.Repo(path)
        return True
    except Exception:
        return False


def get_repo_path():
    print(Fore.CYAN + "\nOpening folder picker... (check your taskbar if it doesn't appear)")
    path = pick_folder()
    return path


def scan_only():
    path = get_repo_path()
    if not path:
        print(Fore.YELLOW + "No folder selected.")
        return
    if not is_git_repo(path):
        print(Fore.RED + f"Not a Git repository: {path}")
        print(Fore.WHITE + "(This folder has no .git history, so there's nothing to scan.)")
        return
    try:
        results = scan_repo(path)
        print()
        print_report(results)
    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def scan_and_save():
    path = get_repo_path()
    if not path:
        print(Fore.YELLOW + "No folder selected.")
        return
    if not is_git_repo(path):
        print(Fore.RED + f"Not a Git repository: {path}")
        print(Fore.WHITE + "(This folder has no .git history, so there's nothing to scan.)")
        return
    out_name = input(Fore.CYAN + "Output filename [results.json]: " + Fore.WHITE).strip()
    out_name = out_name if out_name else "results.json"
    try:
        results = scan_repo(path)
        print()
        print_report(results)
        with open(out_name, "w") as f:
            json.dump(results, f, indent=2)
        print(Fore.CYAN + f"\nSaved results to {out_name}")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def main():
    actions = {"1": scan_only, "2": scan_and_save}
    while True:
        banner()
        menu()
        choice = input(Fore.CYAN + " Select an option: " + Fore.WHITE).strip()
        if choice == "0":
            print(Fore.CYAN + "\nGoodbye!\n")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print(Fore.RED + "Invalid option.")
        input(Fore.CYAN + "\nPress Enter to continue...")


main()
