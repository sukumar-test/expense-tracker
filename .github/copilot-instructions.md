## AI Coding Agent Instructions: Expense Tracker

### Project Overview
- Flask web app for personal expense tracking
- Uses SQLAlchemy (SQLite), Bootstrap 5, Chart.js
- Main entry: `app.py` (routes, models, logic)
- Static assets: `static/` (CSS, JS), templates: `templates/`

### Architecture & Data Flow
- Expenses stored in SQLite (`expenses.db` auto-created)
- Core model: `Expense` (see `app.py`)
- Routes: `/`, `/add`, `/edit/<id>`, `/delete/<id>`, `/categories`, `/api/expenses`
- Category breakdown and charts in `categories.html` (uses Chart.js)
- JS (`static/js/script.js`) sets default dates, tooltips, and delete confirmations

### Developer Workflows
- **Setup:**
	- Create venv: `python -m venv venv`
	- Activate: `source venv/bin/activate`
	- Install: `pip install -r requirements.txt`
	- Run: `./run.sh` (preferred) or `python app.py`
- **Testing:**
	- Run all tests: `./run_tests.py` or `python -m pytest`
	- Coverage: `./run_tests.py --html` or `python -m pytest --cov=app --cov-report=html`
	- Test config/fixtures: `tests/conftest.py` (isolated DB, sample data)
- **CI/CD:**
	- GitHub Actions (`.github/workflows/cicd.yml`) runs tests, lint, builds, deploys to Azure
	- Required secrets: `AZURE_CREDENTIALS`, `AZURE_WEBAPP_NAME`, `AZURE_RESOURCE_GROUP`
- **Azure Deploy:**
	- Manual: `./azure_deploy.sh` (creates ZIP, updates requirements, sets up startup)
	- Python version: 3.10+

### Project-Specific Patterns & Conventions
- All routes and models in `app.py` (single-file app)
- Use Flask's `flash` for user messages
- Use WTForms for form validation (see templates)
- Tests use fixtures for DB/client setup (`conftest.py`)
- Place new tests in `tests/`, name by feature (e.g., `test_routes.py`)
- Follow PEP 8, write docstrings, keep functions focused
- Use descriptive test names, leverage fixtures

### Integration Points
- Frontend: Bootstrap, Chart.js, custom JS
- Backend: Flask, SQLAlchemy
- API: `/api/expenses` returns JSON for frontend/chart use
- Deployment: Azure Web App (via GitHub Actions or manual script)

### Examples
- Add expense: POST `/add` (form in `add.html`)
- Edit expense: GET/POST `/edit/<id>`
- Delete expense: GET `/delete/<id>` (JS confirmation)
- Category chart: `/categories` (template + Chart.js)
- API: GET `/api/expenses` (returns JSON)

### Key Files/Directories
- `app.py`: main logic, routes, models
- `run.sh`, `run_tests.py`, `azure_deploy.sh`: setup, test, deploy scripts
- `requirements.txt`: dependencies
- `static/`, `templates/`: assets and UI
- `tests/`: pytest suite, fixtures

---
For unclear conventions or missing details, check `README.md` and `CONTRIBUTING.md`.
