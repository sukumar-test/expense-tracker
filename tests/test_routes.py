"""Test suite for HTTP routes in the expense tracker application.

This module contains comprehensive tests for all web routes and API endpoints,
including page rendering, form submissions, data validation, CRUD operations,
and error handling for non-existent resources.
"""
from datetime import datetime
import json

def test_index_route(client):
    """Test the index route displays the expenses page correctly.

    This test validates that the home page loads successfully and contains
    the expected content for displaying expenses.

    Args:
        client: Flask test client fixture for making HTTP requests.

    Asserts:
        - Returns HTTP 200 (OK) status code
        - Response contains 'Expenses' text, indicating the page loaded
    """
    response = client.get('/')
    assert response.status_code == 200
    # Test if the page loads - look for key elements that should be there
    assert b'Expenses' in response.data
    
def test_add_expense_get(client):
    """Test GET request to the add expense page.

    This test validates that the add expense form page loads correctly
    and contains the necessary form elements for user input.

    Args:
        client: Flask test client fixture for making HTTP requests.

    Asserts:
        - Returns HTTP 200 (OK) status code
        - Response contains 'Add New Expense' header text
        - Response contains '<form' tag, indicating the form is present
    """
    response = client.get('/add')
    assert response.status_code == 200
    assert b'Add New Expense' in response.data
    assert b'<form' in response.data
    
def test_add_expense_post(client, app):
    """Test POST request to add a new expense.

    This test validates the complete workflow of submitting a new expense
    through the web form, including form processing, database persistence,
    success message display, and data validation.

    Args:
        client: Flask test client fixture for making HTTP requests.
        app: Flask application fixture with application context.

    Asserts:
        - Returns HTTP 200 (OK) after following redirect
        - Success message 'Expense added successfully!' is displayed
        - All expense details (title, amount, category) are visible on page
        - Expense is correctly persisted to the database with all fields

    Note:
        The test follows redirects to verify the success message and
        confirms database state to ensure data integrity.
    """
    response = client.post('/add', data={
        'title': 'Test Expense',
        'amount': '75.50',
        'category': 'Test Category',
        'date': '2025-05-15',
        'description': 'This is a test expense'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Expense added successfully!' in response.data
    assert b'Test Expense' in response.data
    assert b'$75.50' in response.data
    assert b'Test Category' in response.data
    
    # Verify expense was added to database
    with app.app_context():
        from app import Expense
        expense = Expense.query.filter_by(title='Test Expense').first()
        assert expense is not None
        assert expense.amount == 75.50
        assert expense.category == 'Test Category'
        assert expense.description == 'This is a test expense'
        
def test_edit_expense_get(client):
    """Test GET request to the edit expense page.

    This test validates that the edit form page loads correctly with
    pre-populated data from an existing expense record.

    Args:
        client: Flask test client fixture for making HTTP requests.

    Asserts:
        - Returns HTTP 200 (OK) status code
        - Response contains 'Edit Expense' header text
        - Form is pre-populated with existing expense data (title and amount)

    Note:
        This test assumes expense with ID 1 ('Grocery Shopping') exists
        from the test fixtures.
    """
    # Get the first expense (id=1)
    response = client.get('/edit/1')
    assert response.status_code == 200
    assert b'Edit Expense' in response.data
    assert b'Grocery Shopping' in response.data
    assert b'150.75' in response.data
    
def test_edit_expense_post(client, app):
    """Test POST request to update an existing expense.

    This test validates the complete workflow of editing an expense through
    the web form, including form submission, database update, success message
    display, and verification of changes.

    Args:
        client: Flask test client fixture for making HTTP requests.
        app: Flask application fixture with application context.

    Asserts:
        - Returns HTTP 200 (OK) after following redirect
        - Success message 'Expense updated successfully!' is displayed
        - Updated expense title is visible on the page
        - Database record is updated with all new field values

    Note:
        This test modifies expense with ID 1 and verifies changes are
        persisted correctly in the database.
    """
    response = client.post('/edit/1', data={
        'title': 'Updated Grocery Shopping',
        'amount': '160.25',
        'category': 'Food',
        'date': '2025-05-01',
        'description': 'Updated grocery description'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Expense updated successfully!' in response.data
    assert b'Updated Grocery Shopping' in response.data
    
    # Verify expense was updated in database
    with app.app_context():
        from app import Expense
        expense = Expense.query.filter_by(id=1).first()
        assert expense.title == 'Updated Grocery Shopping'
        assert expense.amount == 160.25
        assert expense.description == 'Updated grocery description'
        
def test_delete_expense(client, app):
    """Test deleting an expense through the delete route.

    This test validates the complete delete workflow, including the HTTP
    request handling, success message display, and database record removal.

    Args:
        client: Flask test client fixture for making HTTP requests.
        app: Flask application fixture with application context.

    Asserts:
        - Returns HTTP 200 (OK) after following redirect
        - Success message 'Expense deleted successfully!' is displayed
        - Expense record is removed from the database (query returns None)

    Note:
        This test deletes expense with ID 2 and confirms it no longer
        exists in the database after deletion.
    """
    response = client.get('/delete/2', follow_redirects=True)
    assert response.status_code == 200
    assert b'Expense deleted successfully!' in response.data
    
    # Verify expense was deleted from database
    with app.app_context():
        from app import Expense
        expense = Expense.query.filter_by(id=2).first()
        assert expense is None
        
def test_categories_route(client):
    """Test the categories summary page displays correctly.

    This test validates that the categories page loads successfully and
    displays expense data grouped by category.

    Args:
        client: Flask test client fixture for making HTTP requests.

    Asserts:
        - Returns HTTP 200 (OK) status code
        - Response contains category-related header text
        - Response displays at least two category names (Food, Entertainment)

    Note:
        The test uses flexible assertions for header text to accommodate
        different page title variations.
    """
    response = client.get('/categories')
    assert response.status_code == 200
    assert b'Expense Categories' in response.data or b'Categories' in response.data
    assert b'Food' in response.data
    assert b'Entertainment' in response.data

def test_api_expenses(client):
    """Test the API endpoint returns expense data in JSON format.

    This test validates that the expenses API endpoint correctly returns
    all expenses as JSON data with the proper structure and required fields.

    Args:
        client: Flask test client fixture for making HTTP requests.

    Asserts:
        - Returns HTTP 200 (OK) status code
        - Response is valid JSON that parses to a list
        - At least one expense contains the expected title
        - All expenses include required fields (id, title, amount, category,
          date, description)

    Note:
        This API endpoint is used for programmatic access to expense data
        and must maintain consistent field names and types.
    """
    response = client.get('/api/expenses')
    assert response.status_code == 200
    
    # Check that response is JSON
    data = response.get_json()
    assert isinstance(data, list)
    
    # Check the first expense data
    assert data[0]['title'] == 'Grocery Shopping' or data[2]['title'] == 'Grocery Shopping'
    
    # Make sure all expenses have the required fields
    for expense in data:
        assert 'id' in expense
        assert 'title' in expense
        assert 'amount' in expense
        assert 'category' in expense
        assert 'date' in expense
        assert 'description' in expense

def test_non_existent_expense_edit(client):
    """Test error handling when attempting to edit a non-existent expense.

    This test validates that the application properly handles requests to
    edit expenses that don't exist in the database.

    Args:
        client: Flask test client fixture for making HTTP requests.

    Asserts:
        - Returns HTTP 404 (Not Found) status code

    Note:
        Proper 404 error handling prevents confusion and provides clear
        feedback when users attempt to access non-existent resources.
    """
    response = client.get('/edit/999')
    assert response.status_code == 404

def test_non_existent_expense_delete(client):
    """Test error handling when attempting to delete a non-existent expense.

    This test validates that the application properly handles delete requests
    for expenses that don't exist in the database.

    Args:
        client: Flask test client fixture for making HTTP requests.

    Asserts:
        - Returns HTTP 404 (Not Found) status code

    Note:
        Proper 404 error handling is essential for data integrity and
        prevents potential issues with concurrent deletions.
    """
    response = client.get('/delete/999')
    assert response.status_code == 404
