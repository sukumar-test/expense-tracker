# Developer Documentation

This document provides information for developers working on the Expense Tracker application.

## Project Overview

Expense Tracker is a Flask-based web application that allows users to track personal expenses. It uses SQLAlchemy with SQLite for data storage and Bootstrap for the frontend.

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - macOS/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `./run.sh` or `python app.py`

## Project Structure

```
expense-tracker/
├── app.py                 # Main application file
├── expenses.db            # SQLite database (created on first run)
├── requirements.txt       # Project dependencies
├── run.sh                 # Script to run the application
├── run_tests.py           # Script to run tests with coverage
├── azure_deploy.sh        # Script to prepare deployment package
├── pytest.ini             # Pytest configuration
├── .github/               # GitHub Actions workflows
│   └── workflows/
│       └── cicd.yml       # CI/CD pipeline configuration
├── static/                # Static files
│   ├── css/
│   │   └── styles.css     # Custom CSS
│   └── js/
│       └── script.js      # Custom JavaScript
├── templates/             # HTML templates
│   ├── add.html           # Add expense page
│   ├── base.html          # Base template (layout)
│   ├── categories.html    # Category visualization page
│   ├── edit.html          # Edit expense page
│   └── index.html         # Home page
└── tests/                 # Test files
    ├── __init__.py
    ├── conftest.py        # Test configuration and fixtures
    ├── test_app_setup.py  # Tests for app configuration
    ├── test_edge_cases.py # Tests for error handling
    ├── test_models.py     # Tests for database models
    └── test_routes.py     # Tests for application routes
```

## Testing

The application has a comprehensive test suite using pytest that covers all major functionality.

### Running Tests

You can run tests using the provided `run_tests.py` script:

```bash
# Run tests with basic coverage report
./run_tests.py

# Run tests with verbose output
./run_tests.py --verbose

# Generate HTML coverage report
./run_tests.py --html

# Generate XML coverage report for CI/CD
./run_tests.py --xml
```

Alternatively, you can run tests directly with pytest:

```bash
# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=app

# Run specific test files
python -m pytest tests/test_routes.py
```

### Writing Tests

When adding new features, please write corresponding tests. Follow these guidelines:

1. Place tests in the appropriate file based on what you're testing
2. Use descriptive test names that explain what's being tested
3. Keep tests small and focused on a single functionality
4. Use fixtures from conftest.py for database and client setup

## Continuous Integration and Deployment

The project uses GitHub Actions for CI/CD with automatic deployment to Azure.

### CI/CD Pipeline

The workflow defined in `.github/workflows/cicd.yml` performs:

1. Running all tests with coverage reporting
2. Linting the code with flake8
3. Building a deployment package
4. Deploying to Azure (on push to main/master)
5. Setting up the database in Azure
6. Performing post-deployment validation

### Deployment to Azure

To deploy manually to Azure:

1. Run the Azure deployment script: `./azure_deploy.sh`
2. Follow the instructions provided by the script

### Required GitHub Secrets for CI/CD

To enable automatic deployment via GitHub Actions, set up these repository secrets:

- `AZURE_CREDENTIALS`: JSON credentials for Azure authentication
- `AZURE_WEBAPP_NAME`: The name of your Azure Web App
- `AZURE_RESOURCE_GROUP`: The name of your Azure resource group

## Contributing

1. Create a feature branch from main
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Create a pull request

## Coding Standards

- Follow PEP 8 style guidelines
- Write docstrings for functions and classes
- Keep functions small and focused
- Use meaningful variable and function names
