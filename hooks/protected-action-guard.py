"""Emit a Codex PreToolUse deny candidate for protected shell actions.

This hook never grants authorization, mutates commands, or executes the action.
It intentionally fails open for malformed input so governance reasoning remains
with the existing HLH Skills and human authorization gates.
"""
import json
import re
import shlex
import sys

SUPPORTED_TOOLS = {"bash", "powershell", "shell"}


def protected_command(command: str) -> bool:
    """Classify only simple, confidently recognized command forms."""
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        return False
    if not tokens:
        return False
    lowered = [token.lower() for token in tokens]
    executable = lowered[0].rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    if executable == "git":
        index = 1
        while index < len(lowered) and lowered[index] in {"-c", "--git-dir", "--work-tree"}:
            index += 2
        return index < len(lowered) and (
            lowered[index] in {"commit", "push", "tag"}
            or lowered[index:index + 2] == ["reset", "--hard"]
        )
    if executable == "rm":
        options = set(lowered[1:])
        return "-r" in options and "-f" in options or "-rf" in options or "-fr" in options
    if executable == "remove-item":
        options = set(lowered[1:])
        return "-recurse" in options and "-force" in options
    if executable == "drop" and len(lowered) > 1:
        return lowered[1] in {"database", "table"}
    return executable in {"kubectl", "terraform"} and len(lowered) > 1 and lowered[1] in {"apply", "destroy"}


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        tool_name = payload.get("tool_name", "")
        command = payload.get("tool_input", {}).get("command", "")
    except (json.JSONDecodeError, AttributeError, TypeError):
        print("{}")
        return 0
    if not isinstance(tool_name, str) or tool_name.lower() not in SUPPORTED_TOOLS:
        print("{}")
        return 0
    if not isinstance(command, str) or not protected_command(command):
        print("{}")
        return 0
    result = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "HLH protected-action candidate: explicit human authorization "
                "and the applicable governance gate are required."
            ),
        }
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
