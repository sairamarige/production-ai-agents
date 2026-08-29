# Logging

## Production thinking: what should NOT be logged

Reviewing `main.py`, here's what must never end up in `app.log`:

- ❌ The `AI_API_KEY` / any provider API key
- ❌ Passwords or password hashes
- ❌ Access tokens, refresh tokens, session cookies, JWTs
- ❌ Secrets from `.env` (DB credentials, webhook secrets, etc.)
- ❌ Full raw user input if it could contain personal data (names, emails,
  addresses, health info) — that's why `/ask` logs the *length* of the
  question instead of the question text itself
- ❌ Full AI response content if it could contain sensitive user data
- ❌ Credit card numbers or any payment details
- ❌ Anything that would let someone impersonate a user or the app itself
  if the log file leaked

**Rule of thumb:** log *that* something happened and *how big/what kind* it
was, not the sensitive payload itself. If you need the payload for
debugging, mask it (e.g. `sk-***abcd`) or log it only at `DEBUG` level in a
local dev environment — never in production.

## Interview Questions — Answers

**1. What is logging?**
Recording events that happen while a program runs — startup, requests,
errors, shutdowns — to a destination like the console or a file, so you
have a record of what the application did.

**2. Why is logging better than `print()`?**
`print()` always writes to stdout with no severity, no timestamp, and no
way to turn it off. Logging gives you severity levels, timestamps, the
source module, configurable output destinations (console, file, remote log
service), and you can filter or disable it without touching code.

**3. What are the different logging levels?**
DEBUG < INFO < WARNING < ERROR < CRITICAL (increasing severity).

**4. What is `logging.getLogger(__name__)`?**
Creates/returns a logger named after the current module. This means log
messages are tagged with exactly which file produced them, and it lets you
configure different modules' loggers independently.

**5. What does `basicConfig()` do?**
Configures the root logger in one call — sets the minimum level, the
message format, and the handlers (console, file, etc.) that all loggers
will use unless they're configured differently.

**6. What is `logger.exception()`?**
A shortcut for `logger.error()` that must be called from inside an
`except` block — it automatically attaches the full traceback to the log
message, which is essential for debugging.

**7. How do you save logs to a file?**
Add a `logging.FileHandler("app.log")` to your handlers list in
`basicConfig()` (or attach it to a specific logger).

**8. What information should never be logged?**
API keys, passwords, tokens, secrets, and any sensitive personal or
payment data. See Task 7 above.

**9. Why is logging important for deployed APIs?**
Once an app is running in production you can't attach a debugger. Logs are
often the only way to see what happened — which requests came in, what
failed, and why — so you can diagnose issues after the fact.

**10. Difference between DEBUG, INFO, WARNING, ERROR?**
- `DEBUG`: fine-grained internal details, useful only to developers.
- `INFO`: normal events confirming things are working as expected.
- `WARNING`: something unexpected happened, but the app can continue.
- `ERROR`: an operation failed and something didn't work as intended.
(`CRITICAL` is one step above ERROR — the app itself may not be able to
keep running.)

## Files

| File               | Purpose                                                        |
|--------------------|-----------------------------------------------------------------|
| `main.py`          | FastAPI app (`/ask`, `/ws`) with full logging added             |
| `logging_demo.py`  | Task 1/2/4 — all levels, custom format, exception logging       |
| `app.log`          | Generated log file (Task 5) — created after you run the app     |
| `requirements.txt` | Dependencies                                                    |
| `Dockerfile`        | Container build for deployment                                 |
| `.env.example`     | Template for secrets — copy to `.env`, never commit `.env`      |
| `.gitignore`       | Keeps `.env`, `__pycache__/`, `*.pyc` out of git                 |

Run locally:

```bash
pip install -r requirements.txt
python3 logging_demo.py          # Tasks 1, 2, 4 — writes to app.log
uvicorn main:app --reload        # Tasks 3, 6 — app + request + websocket logging
```