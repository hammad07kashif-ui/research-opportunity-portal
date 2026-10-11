# Research Opportunity Portal

**Student:** Hammad Kashif  
**Roll number:** P24-0631  
**Class:** BCS-5C  
**Course:** Computer Networks (CN), Fall 2026  
**Assignment:** 01 - University Research Opportunity Portal

## Submission status

The frontend, backend, database schema and Postman collection are included. GitHub publication and the one-minute demonstration video are to be completed by the student/friend, as requested. This project is not yet the final instructor submission until those two items are added.

**GitHub repository link:** https://github.com/hammad07kashif-ui/research-opportunity-portal  
**Demonstration video/link:** Not recorded yet. Add `docs/demonstration.mp4` or replace this line with the real video link.

## What the application does

Faculty can post, view, edit, close/reopen and delete research opportunities. The page includes a search box, status filter, full details dialog, database-backed counts, field validation and success/error messages. It starts with an empty database. No opportunity data is hard-coded in the frontend. All frontend operations use the REST API, and all API CRUD operations use MySQL.

## Stack and prerequisites

- Python 3.11 or newer.
- MySQL 8.0 or newer, running locally (MySQL 8.4 recommended).
- A modern browser.
- Postman for the required API demonstration. Node.js is optional for the collection runner.

Flask serves both the REST API and the static frontend at the same address, so there is no separate frontend build or CORS configuration.

## Setup on Windows (PowerShell)

Open a terminal inside this project folder.

1. Create a Python environment and install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

2. Start MySQL. Open MySQL Workbench, connect as your administrative user, and execute the entire `database/schema.sql` file. Alternatively open the MySQL command-line client, log in with `mysql -u root -p`, and run `SOURCE C:/full/path/to/project/database/schema.sql;` (use the actual path with forward slashes).

3. Create an application user in MySQL Workbench/the MySQL client. Replace the password below with your own local password. Do not put it into the README or publish it.

```sql
CREATE USER 'research_portal'@'127.0.0.1' IDENTIFIED BY 'YOUR_LOCAL_PASSWORD';
GRANT SELECT, INSERT, UPDATE, DELETE ON research_portal.* TO 'research_portal'@'127.0.0.1';
```

4. Edit `.env` locally:

```text
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=research_portal
DB_PASSWORD=your actual local password
DB_NAME=research_portal
PORT=5000
```

If using another MySQL account, set DB_USER and DB_PASSWORD to that account. If your MySQL port differs, change DB_PORT. The supplied `.env.example` has no real password. `.env` is excluded by `.gitignore`.

5. Run the application:

```powershell
.\.venv\Scripts\python.exe backend/app.py
```

Open **http://127.0.0.1:5000**. Keep the terminal running. The frontend is served automatically. Stop the server with Ctrl+C.

### Linux/macOS equivalent

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
# Execute database/schema.sql in MySQL, create the user, and edit .env as above.
.venv/bin/python backend/app.py
```

## REST API

| Method | Endpoint | Success | Purpose |
| --- | --- | --- | --- |
| POST | `/api/opportunities` | 201 | Create an opportunity |
| GET | `/api/opportunities` | 200 | Retrieve all opportunities |
| GET | `/api/opportunities/:id` | 200 | Retrieve complete details |
| PUT | `/api/opportunities/:id` | 200 | Update fields or status |
| DELETE | `/api/opportunities/:id` | 200 | Delete an opportunity |
| GET | `/api/health` | 200 | Verify the server and MySQL connection |

Requests and responses use JSON. Lists return `{ "data": [...] }`; a single record returns `{ "data": { ... } }`. Creation/update also return a `message`. The database generates unique IDs, created_at and updated_at. POST returns a Location header for the new record.

Example POST body:

```json
{
  "title": "Machine learning for crop health",
  "description": "Analyze crop imagery and train classification models with the faculty team.",
  "research_area": "Artificial Intelligence",
  "faculty_name": "Dr. Ayesha Khan",
  "department": "Computer Science",
  "required_skills": "Python, machine learning, data analysis",
  "available_positions": 2,
  "application_deadline": "2027-01-31",
  "status": "Open"
}
```

PUT accepts full objects or partial updates. For closing a record, send `{ "status": "Closed" }` to its PUT endpoint.

### Validation and errors

- All eight descriptive/date/position fields are required when creating. Text is trimmed and must be non-empty, with length limits matching the schema (description limited to 10000 characters).
- available_positions must be an integer from 1 to 10000 (booleans, fractions and numeric strings are rejected).
- application_deadline must be a real calendar date in `YYYY-MM-DD` format. Past dates are permitted for maintaining historical records; status is managed explicitly.
- status must be `Open` or `Closed`; omitted status on creation defaults to Open.
- Invalid/missing values, malformed JSON and unknown fields return **400** with field errors. Failed updates do not overwrite valid stored values.
- Missing/deleted IDs and unknown API routes return **404**.
- Unexpected/database failures return **500** with a safe error message; details stay in the server log.
- SQL queries use bound parameters. The frontend escapes stored text before rendering it.

## Postman demonstration and testing

Import `postman/Research Portal.postman_collection.json` into Postman. Its `baseUrl` is `http://127.0.0.1:5000`; change it if you use another port. Run the requests in the numbered order, preferably with Collection Runner. The collection stores created IDs automatically, so there is no manual ID editing.

It creates three opportunities, lists them, gets one, updates it, closes it, deletes it, requests the deleted ID (404), and sends invalid data (400). Each request includes response assertions. Run the final cleanup requests to remove the two remaining demonstration records. The runner only deletes records whose IDs it created during that run.

Optional command-line run (this executes the same exported Postman collection):

```powershell
npx newman run "postman/Research Portal.postman_collection.json"
```

### Automated API regression tests

Tests require the MySQL configuration from `.env`; use a dedicated testing database if you prefer. Tests create their own rows and remove only those rows. Install pytest and run:

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest tests -q
```

See `docs/TEST RESULTS.md` for the actual checks performed on the supplied project.

## Project files

```text
backend/app.py                         Flask API and MySQL access
frontend/index.html                    Page and CRUD dialogs
frontend/style.css                     Responsive styling
frontend/app.js                        REST API calls and UI behavior
database/schema.sql                    Database and table setup
postman/Research Portal.postman_collection.json
requirements.txt                       Application dependencies
.env.example                           Safe configuration template
tests/test_api.py                      MySQL-backed regression tests
docs/DEMONSTRATION GUIDE.md             A <=60-second recording plan
docs/HANDOFF CHECKLIST.md               GitHub and submission steps
docs/TEST RESULTS.md                    Verification evidence
README.md                              Setup and usage instructions
```

## Git history and GitHub handoff

The handoff ZIP contains `development-history.bundle` with real local development commits. Follow `docs/HANDOFF CHECKLIST.md` to clone the bundle and publish those commits to your own GitHub repository. No repository has been created or pushed by the assistant. Add the actual repository URL to this README after publication and ensure the instructor has access.

## Troubleshooting

- **500/database error:** Confirm MySQL is running, execute the schema, and check `.env` host, port, username, password and permissions. `/api/health` also tests the connection.
- **Port already in use:** Set PORT=5001 in `.env`, restart and use http://127.0.0.1:5001. Change the Postman baseUrl accordingly.
- **No records:** This is normal for a new database. Use Post opportunity or run the collection.
- **Python packages missing:** Run pip with the same `.venv` Python used to start the server.
- **Postman 404:** Run the create requests first. The intentionally deleted-record request should return 404.

This is a local coursework application. The brief does not require user accounts or authentication. It binds to loopback by default; it is intended for the assignment demonstration.

## References

- Flask quickstart: https://flask.palletsprojects.com/en/stable/quickstart/
- Flask error handling: https://flask.palletsprojects.com/en/stable/errorhandling/
- PyMySQL connection documentation: https://pymysql.readthedocs.io/en/latest/modules/connections.html
- MySQL portable installation: https://dev.mysql.com/doc/refman/8.4/en/windows-install-archive.html
