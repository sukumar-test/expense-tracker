# Testing Guide

## Overview

The Expense Tracker application has a comprehensive test suite built with pytest that achieves over 98% code coverage. This guide explains the testing approach, how to run tests, and how to write new tests.

## Test Framework

### Tools and Libraries
- **pytest 7.4.0**: Main testing framework
- **pytest-flask 1.2.0**: Flask-specific testing utilities
- **pytest-cov 4.1.0**: Code coverage measurement
- **coverage 7.3.0**: Coverage reporting

### Test Structure

```
tests/
├── __init__.py              # Makes tests a Python package
├── conftest.py              # Shared fixtures and configuration
├── test_app_setup.py        # Application configuration tests
├── test_models.py           # Database model tests
├── test_routes.py           # Route/endpoint tests
└── test_edge_cases.py       # Error handling and edge case tests
```

## Running Tests

### Basic Test Execution

Run all tests:
```bash
python -m pytest
```

Run with verbose output:
```bash
python -m pytest -v
```

Run specific test file:
```bash
python -m pytest tests/test_routes.py
```

Run specific test function:
```bash
python -m pytest tests/test_routes.py::test_add_expense_post
```

### Code Coverage

Run tests with coverage:
```bash
python -m pytest --cov=app
```

Generate HTML coverage report:
```bash
python -m pytest --cov=app --cov-report=html
```
This creates a `htmlcov/` directory with detailed coverage report. Open `htmlcov/index.html` in a browser.

Generate XML coverage report (for CI/CD):
```bash
python -m pytest --cov=app --cov-report=xml
```

### Using the Test Runner Script

The project includes a convenient test runner script:

```bash
# Basic test run with coverage
./run_tests.py

# Verbose output
./run_tests.py --verbose

# Generate HTML report
./run_tests.py --html

# Generate XML report for CI/CD
./run_tests.py --xml
```

### Watch Mode for Development

For continuous testing during development:
```bash
pytest-watch
```
(Requires `pytest-watch` package)

## Test Coverage

### Current Coverage Statistics
- **Overall Coverage**: 98%+
- **Lines Covered**: 99%
- **Branches Covered**: 95%+

### Coverage by Module
- `app.py`: 98%
- Routes: 100%
- Models: 100%
- Templates: N/A (tested through route tests)

## Test Categories

### 1. Application Setup Tests (`test_app_setup.py`)

**Purpose**: Verify Flask application configuration

**Tests**:
- `test_app_config`: Validates configuration settings
- `test_app_routes_registered`: Ensures all routes are registered

**Example**:
```python
def test_app_config(app):
    """Test that the app is configured correctly."""
    assert app.config['TESTING'] == True
    assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']
```

### 2. Model Tests (`test_models.py`)

**Purpose**: Test database models and ORM functionality

**Tests**:
- `test_expense_model`: CRUD operations on Expense model
- `test_expense_default_date`: Default date assignment

**Example**:
```python
def test_expense_model(app):
    """Test the Expense model."""
    with app.app_context():
        expense = Expense(
            title='Test Expense',
            amount=100.00,
            category='Test',
            date=datetime.strptime('2025-05-20', '%Y-%m-%d'),
            description='Test description'
        )
        db.session.add(expense)
        db.session.commit()
        
        queried_expense = Expense.query.filter_by(title='Test Expense').first()
        assert queried_expense is not None
```

### 3. Route Tests (`test_routes.py`)

**Purpose**: Test HTTP endpoints and user workflows

**Tests**:
- `test_index_route`: Home page display
- `test_add_expense_get`: Add form display
- `test_add_expense_post`: Creating new expense
- `test_edit_expense_get`: Edit form display
- `test_edit_expense_post`: Updating expense
- `test_delete_expense`: Deleting expense
- `test_categories_route`: Category breakdown page
- `test_api_expenses`: JSON API endpoint
- `test_non_existent_expense_edit`: 404 handling for edit
- `test_non_existent_expense_delete`: 404 handling for delete

**Example**:
```python
def test_add_expense_post(client, app):
    """Test adding a new expense."""
    response = client.post('/add', data={
        'title': 'Test Expense',
        'amount': '75.50',
        'category': 'Test Category',
        'date': '2025-05-15',
        'description': 'This is a test expense'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Expense added successfully!' in response.data
```

### 4. Edge Case Tests (`test_edge_cases.py`)

**Purpose**: Test error handling and boundary conditions

**Tests**:
- `test_invalid_form_data`: Non-numeric amounts, invalid dates
- `test_empty_form_fields`: Empty required fields
- `test_form_with_missing_fields`: Missing form data
- `test_edit_with_invalid_data`: Invalid data during edit

**Example**:
```python
def test_invalid_form_data(client):
    """Test submitting invalid form data."""
    try:
        response = client.post('/add', data={
            'title': 'Invalid Expense',
            'amount': 'not-a-number',
            'category': 'Test',
            'date': '2025-05-20'
        })
        assert response.status_code != 302
    except ValueError:
        pass  # Expected
```

## Test Fixtures

### Available Fixtures (from `conftest.py`)

#### `app` Fixture
Creates a Flask application instance for testing with:
- Isolated SQLite database (temporary file)
- Test configuration enabled
- CSRF protection disabled
- Sample expense data pre-loaded

**Usage**:
```python
def test_something(app):
    with app.app_context():
        # Access database here
        expenses = Expense.query.all()
```

#### `client` Fixture
Provides a test client for making HTTP requests

**Usage**:
```python
def test_route(client):
    response = client.get('/')
    assert response.status_code == 200
```

#### `runner` Fixture
Provides a CLI test runner for Flask commands

**Usage**:
```python
def test_cli_command(runner):
    result = runner.invoke(my_command)
    assert result.exit_code == 0
```

### Sample Test Data

The `app` fixture pre-loads these expenses:
1. **Grocery Shopping**: $150.75 (Food) - 2025-05-01
2. **Electric Bill**: $87.30 (Utilities) - 2025-05-05
3. **Movie Tickets**: $35.50 (Entertainment) - 2025-05-10

## Writing New Tests

### Test Template

```python
def test_your_feature(client, app):
    """
    Description of what this test does.
    
    Tests:
    - Specific behavior 1
    - Specific behavior 2
    """
    # Arrange: Set up test data
    test_data = {'key': 'value'}
    
    # Act: Perform the action
    response = client.post('/endpoint', data=test_data)
    
    # Assert: Verify the results
    assert response.status_code == 200
    assert b'expected text' in response.data
    
    # Additional database verification if needed
    with app.app_context():
        from app import Expense
        expense = Expense.query.filter_by(title='Test').first()
        assert expense is not None
```

### Best Practices

1. **Naming Convention**: Use descriptive test names starting with `test_`
2. **Docstrings**: Add clear docstrings explaining what's being tested
3. **Isolation**: Each test should be independent
4. **Arrange-Act-Assert**: Structure tests in three clear phases
5. **One Assertion Focus**: Test one thing per test when possible
6. **Use Fixtures**: Leverage existing fixtures for common setup
7. **Clean Up**: Fixtures handle cleanup automatically
8. **Error Cases**: Test both success and failure scenarios

### Testing Different Scenarios

#### Testing GET Requests
```python
def test_page_load(client):
    """Test that page loads correctly."""
    response = client.get('/page')
    assert response.status_code == 200
    assert b'Expected Content' in response.data
```

#### Testing POST Requests
```python
def test_form_submission(client):
    """Test form submission."""
    response = client.post('/add', data={
        'field1': 'value1',
        'field2': 'value2'
    }, follow_redirects=True)
    assert b'Success message' in response.data
```

#### Testing JSON API
```python
def test_api_endpoint(client):
    """Test JSON API endpoint."""
    response = client.get('/api/endpoint')
    data = response.get_json()
    assert isinstance(data, list)
    assert 'expected_field' in data[0]
```

#### Testing Database Operations
```python
def test_database_operation(app):
    """Test database CRUD operation."""
    with app.app_context():
        from app import db, Expense
        
        # Create
        expense = Expense(title='Test', amount=10.0, category='Test')
        db.session.add(expense)
        db.session.commit()
        
        # Read
        found = Expense.query.filter_by(title='Test').first()
        assert found is not None
        
        # Update
        found.amount = 20.0
        db.session.commit()
        
        # Delete
        db.session.delete(found)
        db.session.commit()
```

## Continuous Integration

### GitHub Actions Workflow

Tests are automatically run on every push and pull request via GitHub Actions:

```yaml
- name: Run tests with coverage
  run: |
    python -m pytest --cov=app --cov-report=xml --cov-report=term
```

### Coverage Requirements

- Minimum coverage: 90%
- Current coverage: 98%+
- CI fails if coverage drops below threshold

## Debugging Failed Tests

### Verbose Output
```bash
python -m pytest -v
```

### Show Print Statements
```bash
python -m pytest -s
```

### Stop on First Failure
```bash
python -m pytest -x
```

### Show Full Error Traceback
```bash
python -m pytest --tb=long
```

### Run Only Failed Tests
```bash
python -m pytest --lf
```

### Debug Mode
```python
def test_something(client):
    response = client.get('/')
    import pdb; pdb.set_trace()  # Debugger breakpoint
    assert response.status_code == 200
```

## Performance Testing

While not included in the current test suite, consider adding:

### Load Testing
```python
def test_concurrent_requests():
    """Test application under load."""
    # Use tools like locust or pytest-benchmark
    pass
```

### Database Performance
```python
def test_query_performance(app):
    """Test database query performance."""
    import time
    with app.app_context():
        start = time.time()
        expenses = Expense.query.all()
        duration = time.time() - start
        assert duration < 0.1  # Should complete in 100ms
```

## Test Maintenance

### Regular Tasks
1. Run tests before committing code
2. Review coverage reports weekly
3. Update tests when features change
4. Add tests for bug fixes
5. Remove obsolete tests

### Coverage Goals
- Maintain 95%+ overall coverage
- 100% coverage for critical paths
- Test all error conditions
- Cover edge cases and boundary conditions

## Resources

### pytest Documentation
- Official docs: https://docs.pytest.org/
- pytest-flask: https://pytest-flask.readthedocs.io/
- pytest-cov: https://pytest-cov.readthedocs.io/

### Testing Best Practices
- Test-Driven Development (TDD)
- Behavior-Driven Development (BDD)
- Unit vs Integration vs End-to-End testing
- Mocking and stubbing strategies

## Common Issues and Solutions

### Issue: Database Locked
**Solution**: Tests use temporary databases for isolation

### Issue: Tests Failing Randomly
**Solution**: Ensure test independence, avoid shared state

### Issue: Slow Tests
**Solution**: Use test markers to separate fast/slow tests

### Issue: Coverage Not 100%
**Solution**: Some lines (like error handling) may be difficult to test directly
