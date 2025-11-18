"""Test suite for application setup and configuration.

This module validates the Flask application's initialization, configuration
settings, and route registration to ensure the app is properly configured
for the expense tracker functionality.
"""
import os

def test_app_config(app):
    """Test Flask application configuration settings.

    This test validates that the application is configured with the correct
    settings for testing, database connection, and session management.

    Args:
        app: Flask application fixture.

    Asserts:
        - TESTING mode is enabled (set to True)
        - SQLALCHEMY_DATABASE_URI contains 'sqlite' (using SQLite database)
        - SQLALCHEMY_TRACK_MODIFICATIONS is disabled (set to False)
        - Secret key is properly set for session management

    Note:
        These configuration settings are critical for the application's
        security and proper database operation in test mode.
    """
    assert app.config['TESTING'] == True
    assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False
    assert app.secret_key == 'expense_tracker_secret_key'
    
def test_app_routes_registered(app):
    """Test that all necessary application routes are registered.

    This test validates the route registration to ensure all expected
    endpoints for the expense tracker are available in the URL map.

    Args:
        app: Flask application fixture.

    Asserts:
        - Index route ('/') is registered
        - Add expense route ('/add') is registered
        - Edit expense route ('/edit/<int:id>') is registered
        - Delete expense route ('/delete/<int:id>') is registered
        - Categories summary route ('/categories') is registered
        - API expenses endpoint ('/api/expenses') is registered

    Note:
        Route registration is essential for the application's functionality.
        Missing routes would prevent users from accessing key features.
    """
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    
    # Check that all expected routes are registered
    assert '/' in routes
    assert '/add' in routes
    assert '/edit/<int:id>' in routes
    assert '/delete/<int:id>' in routes
    assert '/categories' in routes
    assert '/api/expenses' in routes
