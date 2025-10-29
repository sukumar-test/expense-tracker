"""Test suite for HTTP routes in the Expense Tracker application.

This module contains tests for all HTTP endpoints in the Flask application,
including:
- Index page display
- Adding new expenses (GET and POST)
- Editing expenses (GET and POST)
- Deleting expenses
- Category summary page
- API endpoints
- Error handling for non-existent resources

All tests use pytest fixtures defined in conftest.py for database setup
and test client creation.
"""
from datetime import datetime
import json

def test_index_route(client):
    """Test the index route displays expenses correctly.
    
    Verifies that:
    - The index page loads successfully (200 status code)
    - The page contains expected content indicating expenses are displayed
    
    Args:
        client (FlaskClient): The test client fixture.
    """
    response = client.get('/')
    assert response.status_code == 200
    # Test if the page loads - look for key elements that should be there
    assert b'Expenses' in response.data
    
def test_add_expense_get(client):
    """Test the GET request to the add expense page.
    
    Verifies that:
    - The add expense form loads successfully (200 status code)
    - The page contains the expected form title
    - The page contains a form element
    
    Args:
        client (FlaskClient): The test client fixture.
    """
    response = client.get('/add')
    assert response.status_code == 200
    assert b'Add New Expense' in response.data
    assert b'<form' in response.data
    
def test_add_expense_post(client, app):
    """Test adding a new expense via POST request.
    
    Verifies that:
    - Submitting the add expense form succeeds with redirect
    - Success flash message is displayed
    - Expense data appears on the index page
    - Expense is correctly saved to the database with all fields
    
    Args:
        client (FlaskClient): The test client fixture.
        app (Flask): The Flask application fixture.
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
    """Test the GET request to edit an expense.
    
    Verifies that:
    - The edit expense form loads successfully (200 status code)
    - The page contains the expected form title
    - The form is pre-filled with existing expense data
    
    Args:
        client (FlaskClient): The test client fixture.
    """
    # Get the first expense (id=1)
    response = client.get('/edit/1')
    assert response.status_code == 200
    assert b'Edit Expense' in response.data
    assert b'Grocery Shopping' in response.data
    assert b'150.75' in response.data
    
def test_edit_expense_post(client, app):
    """Test editing an expense via POST request.
    
    Verifies that:
    - Submitting the edit expense form succeeds with redirect
    - Success flash message is displayed
    - Updated expense data appears on the index page
    - All expense fields are correctly updated in the database
    
    Args:
        client (FlaskClient): The test client fixture.
        app (Flask): The Flask application fixture.
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
    """Test deleting an expense.
    
    Verifies that:
    - Accessing the delete route succeeds with redirect
    - Success flash message is displayed
    - The expense is removed from the database
    
    Args:
        client (FlaskClient): The test client fixture.
        app (Flask): The Flask application fixture.
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
    """Test the categories summary page.
    
    Verifies that:
    - The categories page loads successfully (200 status code)
    - The page contains expected heading text
    - Category names from sample data are displayed
    
    Args:
        client (FlaskClient): The test client fixture.
    """
    response = client.get('/categories')
    assert response.status_code == 200
    assert b'Expense Categories' in response.data or b'Categories' in response.data
    assert b'Food' in response.data
    assert b'Entertainment' in response.data

def test_api_expenses(client):
    """Test the API endpoint for retrieving expenses in JSON format.
    
    Verifies that:
    - The API endpoint returns a successful response
    - Response content type is JSON
    - Response contains a list of expenses
    - Sample expense data is present in the response
    - All required fields are present in each expense object
    
    Args:
        client (FlaskClient): The test client fixture.
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
    """Test accessing a non-existent expense for editing.
    
    Verifies that attempting to edit an expense that doesn't exist
    returns a 404 error.
    
    Args:
        client (FlaskClient): The test client fixture.
    """
    response = client.get('/edit/999')
    assert response.status_code == 404

def test_non_existent_expense_delete(client):
    """Test deleting a non-existent expense.
    
    Verifies that attempting to delete an expense that doesn't exist
    returns a 404 error.
    
    Args:
        client (FlaskClient): The test client fixture.
    """
    response = client.get('/delete/999')
    assert response.status_code == 404
