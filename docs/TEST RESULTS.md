# Verification results

Prepared for Hammad Kashif | P24-0631 | BCS-5C.

Verified on 11 October 2026 with Python 3.12, Flask 3.1.2, PyMySQL 1.1.2, MySQL Community Server 8.4.11, Newman and Google Chrome.

## Results

| Check | Result |
| --- | --- |
| MySQL-backed API regression suite | 28 tests passed, 0 failed |
| Exported Postman collection executed with Newman | 13 requests, 37 assertions passed, 0 failed |
| Frontend browser checks | 16 checks passed, 0 browser JavaScript errors |
| Desktop and mobile visual review | Reviewed at 1440 px and 390 px widths; no clipped elements or horizontal overflow |

The database was a real isolated MySQL server, not an in-memory substitute. The test application ran on loopback port 5063 and MySQL on port 3307; these testing ports do not change the supplied default setup (5000 and 3306). All test-created opportunity rows were removed after the checks.

## API coverage

Creation, retrieval of all/one, partial updates, persisted status changes, deletion, missing/deleted IDs, required fields, blank text, text-length limits, integer limits/types, impossible dates, non-YYYY-MM-DD dates, invalid statuses, unexpected fields, malformed JSON, default Open status, safe handling of SQL-like text, atomic rejection of invalid updates, JSON 500 error handling, frontend serving and database health.

## Postman coverage

The exported collection was executed with Newman, the Postman collection runner. It created three records, retrieved all and one, updated a title/position count, closed and verified the stored record, deleted it, received the expected 404, received the expected 400 for missing/invalid data, and cleaned up the other two records. `POSTMAN RESULTS.json` records each request's actual HTTP status and assertion outcomes. The Postman graphical interface/video demonstration is still for the student/friend to perform.

## Frontend coverage

The browser checked empty state, browser required-field validation, create persistence, full details, edit persistence, close/reopen, multiple records, search, status filter, mobile overflow, backend validation messages, deletion, stale-record 404 display, stored HTML escaping and browser errors. `FRONTEND RESULTS.json` lists the checks. The included desktop/mobile screenshots show actual temporary records retrieved from the API during testing; they are preview images, not frontend fixtures or seeded database rows.

## Remaining submission tasks

GitHub publication and the <=60-second recording were intentionally left to the student's friend per the user's instruction. See HANDOFF CHECKLIST.md and DEMONSTRATION GUIDE.md. No GitHub URL or video link has been fabricated.
