import argparse
import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright


PROJECT_ROOT = Path(__file__).resolve().parents[1]


async def fill_demo_form(config_path: Path) -> None:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    target = config["target"]
    fields = config.get("fields", {})
    selectors = config.get("selectors", {})

    target_path = Path(target)
    if not target_path.is_absolute():
        target_path = PROJECT_ROOT / target_path

    if not target_path.exists():
        raise FileNotFoundError(f"Demo target not found: {target_path}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(target_path.as_uri())

        for field_name, value in fields.items():
            selector = selectors.get(field_name)
            if not selector:
                continue
            await page.fill(selector, value)
            print(f"filled {field_name}")

        terms_selector = selectors.get("terms")
        if terms_selector:
            await page.check(terms_selector)
            print("checked terms")

        submit_selector = selectors.get("submit")
        if submit_selector:
            await page.click(submit_selector)
            print("submitted form")

        await page.wait_for_timeout(1200)
        await browser.close()


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
