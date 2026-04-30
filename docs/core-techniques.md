# Core Techniques for Authorized Form Automation Testing

This document explains the core engineering techniques behind a safe registration-form automation system for authorized testing environments.

The goal is to document reusable testing patterns without publishing production-targeted mass account creation logic, real mailbox integrations, credential storage, platform-specific bypasses, or third-party abuse workflows.

## 1. Scope and threat model

### Intended use

This project is designed for:

- QA validation of owned registration flows
- Regression testing for signup forms in staging environments
- Demonstrating Playwright-based browser automation
- Teaching selector mapping, task orchestration, retry strategy, and safe publication hygiene

### Explicitly excluded

This public version does not include:

- Real third-party registration targets
- Temporary mailbox API integration
- Production one-time-code collection
- Continuous account creation loops
- Credential export pipelines
- Anti-abuse evasion logic
- Stored browser sessions from real users

This boundary is intentional: the same automation primitives that are useful for QA can become harmful if packaged as a ready-to-run account creation tool for third-party platforms.

## 2. High-level architecture

A safe automation test system can be separated into five layers:

```text
Configuration Layer
  ↓
Task Orchestration Layer
  ↓
Browser Automation Layer
  ↓
Verification/Test-Double Layer
  ↓
Reporting Layer
```

### Configuration layer

The configuration layer defines what the automation should interact with. It should avoid hardcoding selectors and test data in the automation engine.

Recommended fields:

- `target`: local file, staging URL, or authorized test endpoint
- `selectors`: mapping from semantic field names to CSS selectors
- `fields`: non-sensitive fixture values
- `timeouts`: per-step timeout settings
- `browser`: headed/headless choice for debugging

Benefits:

- The same engine can test different forms
- Selector changes are isolated to config files
- Sensitive production URLs can be kept out of public code
- Reviewers can inspect test intent without reading browser logic

Example from this repository:

```json
{
  "target": "examples/demo_form.html",
  "fields": {
    "first_name": "Demo",
    "last_name": "User",
    "email": "demo.user@example.test",
    "password": "ExamplePassword123!"
  },
  "selectors": {
    "first_name": "#first-name",
    "last_name": "#last-name",
    "email": "#email",
    "password": "#password",
    "terms": "#terms",
    "submit": "#submit"
  }
}
```

## 3. Browser automation layer

Playwright is used because it provides:

- Reliable element locators
- Browser-context isolation
- Async APIs for orchestration
- Headed mode for debugging
- Trace and screenshot support when needed

The core loop is intentionally simple:

1. Load configuration
2. Open the authorized target
3. Fill configured fields
4. Check required consent controls
5. Submit the form
6. Report success or failure

A minimal implementation is easier to audit than a large framework. The public demo keeps the implementation small so the safety boundary is clear.

## 4. Selector strategy

Selectors should be stable, explicit, and semantic.

Recommended selector priority:

1. Test IDs, such as `[data-testid="signup-email"]`
2. Accessible roles and labels
3. Stable IDs
4. Stable names
5. CSS structure only as a last resort

Avoid selectors that depend on:

- Visual layout
- Randomized class names
- Deep DOM nesting
- Text that changes by locale

A configuration-driven selector map makes it easy to review what the automation touches.

## 5. Task orchestration design

For authorized QA, task orchestration should favor safety and observability over throughput.

Recommended model:

```text
Single test task
  → one browser context
  → one fixture identity
  → one result object
```

The task runner should track:

- `task_id`
- `status`: pending, running, succeeded, failed
- `started_at`
- `finished_at`
- `step_name`
- `error_message`

For public or shared examples, avoid including production-scale concurrency controls. If concurrency is needed in a private QA environment, keep it bounded and documented with explicit authorization.

## 6. Verification handling in safe test environments

Many registration forms include email or one-time-code verification. In a responsible test architecture, this should be handled through controlled test doubles rather than public mailbox scraping.

Safe options:

- Use a staging-only verification bypass flag controlled by the backend
- Use a local fake mailbox service in the test environment
- Use deterministic test codes issued only in non-production
- Mock the verification step in component or integration tests
- Seed verified test users directly in the test database

Unsafe for public release:

- Publishing real mailbox provider integrations
- Publishing token/cookie based mailbox access logic
- Publishing code that waits for production verification messages
- Publishing bulk account output files

The important engineering principle is to test the registration state machine without depending on real third-party inbox infrastructure.

## 7. Error handling and retry strategy

Good automation handles failure explicitly.

Recommended categories:

- Navigation timeout
- Missing selector
- Validation error
- Network failure
- Unexpected page state
- Test fixture conflict

Retry should be conservative:

- Retry transient navigation or network failures
- Do not retry validation failures blindly
- Add exponential backoff for test infrastructure endpoints
- Record the exact failed step
- Preserve screenshots or traces only when they do not contain sensitive data

A safe result object might contain:

```json
{
  "status": "failed",
  "step": "fill_email",
  "error": "Selector #email was not visible within timeout"
}
```

It should not contain real credentials, cookies, or tokens.

## 8. Data handling and logging

Public test automation should use fixture data only.

Recommended practices:

- Use `.example`, `.test`, or clearly fake domains
- Do not persist generated credentials
- Do not log passwords
- Do not commit screenshots containing personal information
- Keep `.env`, local logs, and browser state ignored by Git
- Keep publication audit notes in the repository

This repository uses `.gitignore` rules for runtime data and includes `PUBLICATION_AUDIT.md` to document what was intentionally excluded.

## 9. Local demo flow

The demo flow in this repository uses a local HTML page:

```text
examples/demo_form.html
```

The automation script:

```text
src/form_automation_demo.py
```

It reads:

```text
examples/sample_config.json
```

Then it fills the local form and submits it. This demonstrates the automation mechanics while avoiding dependency on any third-party service.

## 10. Extending this project safely

Safe extensions:

- Add Playwright trace support for the local demo
- Add structured result JSON for test runs
- Add a local fake verification service
- Add unit tests for config validation
- Add CI that runs against the local demo page
- Add screenshots of only the local demo form

Extensions that should stay private and authorized:

- Staging credentials
- Internal service endpoints
- Organization-specific selectors
- Real verification infrastructure
- Production-like load testing

Do not publish anything that turns the project into a ready-to-run account creation tool against third-party services.

## 11. Review checklist before publication

Before pushing updates to a public repository, check:

- No real account records
- No passwords, cookies, tokens, API keys, or session data
- No local absolute paths
- No real mailbox integration
- No production target URLs
- No runtime logs or browser profiles
- No generated credential exports
- No screenshots with personal information

Suggested command pattern:

```bash
git status --short
git ls-files
grep -R "token\|cookie\|secret\|password" . --exclude-dir=.git
```

Review any matches manually. Example fixture values may contain the word `password`, but no real secret should be present.

## 12. Engineering summary

The key reusable techniques are:

- Keep automation generic and configuration-driven
- Use stable selectors and semantic field names
- Isolate browser contexts per test
- Track task state and failure steps explicitly
- Use controlled test doubles for verification flows
- Prefer safety, auditability, and authorization over throughput
- Treat publication hygiene as part of the engineering design

This makes the project useful for learning and QA while avoiding the risks of publishing operational abuse tooling.
