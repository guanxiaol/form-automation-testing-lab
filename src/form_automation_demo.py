import argparse
import asyncio
import json
from pathlib import Path

from config_loader import load_config
from runner import FormAutomationRunner


PROJECT_ROOT = Path(__file__).resolve().parents[1]


async def fill_demo_form(config_path: Path) -> None:
    config = load_config(config_path)
    runner = FormAutomationRunner(PROJECT_ROOT)
    result = await runner.run(config)
    print(json.dumps(result.to_safe_dict(), ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Authorized local registration form automation demo")
    parser.add_argument("--config", default="examples/sample_config.json", help="Path to demo config JSON")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    asyncio.run(fill_demo_form(config_path))


if __name__ == "__main__":
    main()
