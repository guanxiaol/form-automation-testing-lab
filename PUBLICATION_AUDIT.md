# Publication Audit

This repository was created as a sanitized public version. The original private working directory contained runtime data and automation code that is not appropriate for public release.

## Excluded from publication

- `accounts.txt` — contains generated account records
- `accounts.json` — contains generated account credentials
- `register_results.txt` — contains run outputs
- `emails.txt` — contains email-related runtime data
- `logs/` — contains runtime logs
- `browser_profiles/` — contains browser profile/cache state
- `venv/` — local Python virtual environment
- `__pycache__/` — Python bytecode cache
- `*.plist` / LaunchAgent configuration — local auto-start configuration
- Original bulk registration dashboard and continuous-run implementation
- Temporary email API client and OTP polling implementation

## Public version scope

The public version only includes:

- A local demo form
- A single-run Playwright automation example
- A sample non-sensitive configuration file
- Security and publication guidance

## Verification checklist before GitHub push

Run these commands before publishing:

```bash
git status --short
grep -R "@" . --exclude-dir=.git --exclude="README.md" --exclude="SECURITY.md" --exclude="PUBLICATION_AUDIT.md"
grep -R "password\|token\|cookie\|local absolute path" . --exclude-dir=.git
```

Expected result: only example placeholders should appear.
