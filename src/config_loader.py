import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AutomationConfig:
    target: str
    fields: dict[str, str]
    selectors: dict[str, str]
    timeout_ms: int = 10_000
    headless: bool = False


def load_config(path: Path) -> AutomationConfig:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return parse_config(raw)


def parse_config(raw: dict[str, Any]) -> AutomationConfig:
    target = require_string(raw, "target")
    fields = require_string_map(raw, "fields")
    selectors = require_string_map(raw, "selectors")
    timeout_ms = int(raw.get("timeout_ms", 10_000))
    headless = bool(raw.get("headless", False))

    if timeout_ms < 1_000 or timeout_ms > 60_000:
        raise ValueError("timeout_ms must be between 1000 and 60000")

    missing_selectors = sorted(set(fields) - set(selectors))
    if missing_selectors:
        raise ValueError(f"Missing selectors for fields: {', '.join(missing_selectors)}")

    return AutomationConfig(
        target=target,
        fields=fields,
        selectors=selectors,
        timeout_ms=timeout_ms,
        headless=headless,
    )


def require_string(raw: dict[str, Any], key: str) -> str:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value


def require_string_map(raw: dict[str, Any], key: str) -> dict[str, str]:
    value = raw.get(key)
    if not isinstance(value, dict) or not value:
        raise ValueError(f"{key} must be a non-empty object")
    result: dict[str, str] = {}
    for item_key, item_value in value.items():
        if not isinstance(item_key, str) or not isinstance(item_value, str):
            raise ValueError(f"{key} must only contain string keys and values")
        result[item_key] = item_value
    return result
