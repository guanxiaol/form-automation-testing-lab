from pathlib import Path
from uuid import uuid4

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

from config_loader import AutomationConfig
from models import AutomationResult, ErrorCategory, StepResult


class FormAutomationRunner:
    def __init__(self, project_root: Path):
        self.project_root = project_root

    async def run(self, config: AutomationConfig) -> AutomationResult:
        result = AutomationResult(task_id=str(uuid4()))
        result.mark_running()

        try:
            target_uri = self._resolve_target(config.target)
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=config.headless)
                page = await browser.new_page()
                page.set_default_timeout(config.timeout_ms)

                await self._run_step(result, "navigate", lambda: page.goto(target_uri))

                for field_name, value in config.fields.items():
                    selector = config.selectors[field_name]
                    await self._run_step(
                        result,
                        f"fill_{field_name}",
                        lambda selector=selector, value=value: page.fill(selector, value),
                    )

                terms_selector = config.selectors.get("terms")
                if terms_selector:
                    await self._run_step(result, "check_terms", lambda: page.check(terms_selector))

                submit_selector = config.selectors.get("submit")
                if submit_selector:
                    await self._run_step(result, "submit", lambda: page.click(submit_selector))

                await page.wait_for_timeout(800)
                await browser.close()

            result.mark_succeeded()
        except Exception as exc:
            if not result.finished_at:
                result.mark_failed()
            result.metadata["failure"] = type(exc).__name__

        return result

    async def _run_step(self, result: AutomationResult, name: str, action):
        step = StepResult.start(name)
        result.steps.append(step)
        try:
            await action()
            step.succeed()
        except PlaywrightTimeoutError as exc:
            step.fail(ErrorCategory.SELECTOR, str(exc).splitlines()[0])
            result.mark_failed()
            raise
        except Exception as exc:
            step.fail(ErrorCategory.UNKNOWN, str(exc).splitlines()[0])
            result.mark_failed()
            raise

    def _resolve_target(self, target: str) -> str:
        if target.startswith("http://") or target.startswith("https://"):
            return target

        target_path = Path(target)
        if not target_path.is_absolute():
            target_path = self.project_root / target_path

        if not target_path.exists():
            raise FileNotFoundError(f"Demo target not found: {target_path}")

        return target_path.as_uri()
