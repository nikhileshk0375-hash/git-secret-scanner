import re

PATTERNS = {
    "AWS Access Key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Generic API Key": re.compile(r"(?i)api[_-]?key[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,45}"),
    "Generic Secret": re.compile(r"(?i)secret[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,45}"),
    "Password Assignment": re.compile(r"(?i)password[\"']?\s*[:=]\s*[\"'][^\"'\s]{6,}[\"']"),
    "GitHub Token": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "Private Key Header": re.compile(r"-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----"),
    "Slack Token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    "Generic Token": re.compile(r"(?i)token[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,45}"),
}

PLACEHOLDER_WORDS = ["your_key_here", "xxxx", "placeholder", "example",
                      "changeme", "use_env", "replace_me", "todo", "env_variable"]


def is_placeholder(value):
    lowered = value.lower()
    return any(word in lowered for word in PLACEHOLDER_WORDS)


def find_secrets(text):
    """Search text for any known secret pattern. Returns a list of (type, matched_text)."""
    found = []
    for name, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            value = match.group()
            if is_placeholder(value):
                continue
            found.append((name, value))
    return found
