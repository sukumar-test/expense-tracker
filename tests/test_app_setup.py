"""
Test file for testing the application setup and configuration.
"""
import os

def test_app_config(app):
    """Test that the app is configured correctly."""
    assert app.config['TESTING'] == True
    assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False
    assert app.secret_key == 'expense_tracker_secret_key'
    
def test_app_routes_registered(app):
    """Test that all necessary routes are registered."""
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    
    # Check that all expected routes are registered
    assert '/' in routes
    assert '/add' in routes
    assert '/edit/<int:id>' in routes
    assert '/delete/<int:id>' in routes
    assert '/categories' in routes
    assert '/api/expenses' in routes
