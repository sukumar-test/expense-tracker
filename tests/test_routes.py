"""Tests for route handlers in the expense tracker application.

This module contains test cases that verify the correct behavior of all
Flask routes, including GET and POST requests, redirects, and response validation.
"""

from datetime import datetime
import json


def test_index_route(client):
    """Test the index route that displays all expenses.
    
    Verifies that the homepage loads correctly and contains expected content.
    
    Args:
        client (FlaskClient): The test client fixture.
    """
    response = client.get('/')
    assert response.status_code == 200
    # Test if the page loads - look for key elements that should be there
    assert b'Expenses' in response.data
    
def test_add_expense_get(client):
    """Test the GET request to the add expense page.
    
    Verifies that the add expense form page loads correctly with
    the expected form elements.
    
    Args:
        client (FlaskClient): The test client fixture.
    """
    response = client.get('/add')
    assert response.status_code == 200
    assert b'Add New Expense' in response.data
    assert b'<form' in response.data
    
def test_add_expense_post(client, app):
    """Test adding a new expense via POST request.
    
    Verifies that a new expense can be created through the form submission,
    is saved to the database, and displays the success message.
    
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
    
    Verifies that the edit expense form loads with pre-populated data
    from an existing expense.
    
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
    
    Verifies that an expense can be updated with new data through
    form submission and the changes are persisted to the database.
    
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
    
    Verifies that an expense can be deleted and is removed from the database,
    with appropriate success message displayed.
    
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
    
    Verifies that the category summary page loads and displays
    expense categories with aggregated data.
    
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
    
    Verifies that the API endpoint returns a valid JSON array of expenses
    with all required fields present in each expense object.
    
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
    
    Verifies that attempting to edit a non-existent expense returns
    a 404 Not Found error.
    
    Args:
        client (FlaskClient): The test client fixture.
    """
    response = client.get('/edit/999')
    assert response.status_code == 404

def test_non_existent_expense_delete(client):
    """Test deleting a non-existent expense.
    
    Verifies that attempting to delete a non-existent expense returns
    a 404 Not Found error.
    
    Args:
        client (FlaskClient): The test client fixture.
    """
    response = client.get('/delete/999')
    assert response.status_code == 404
