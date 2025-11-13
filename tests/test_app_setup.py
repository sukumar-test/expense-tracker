"""Tests for application setup and configuration.

This module contains test cases that verify the Flask application is
configured correctly with proper settings and all required routes are registered.
"""

import os


def test_app_config(app):
    """Test that the Flask app is configured correctly.
    
    Verifies that all configuration settings are properly set, including
    database configuration, testing mode, and secret key.
    
    Args:
        app (Flask): The Flask application fixture.
    """
    assert app.config['TESTING'] == True
    assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False
    assert app.secret_key == 'expense_tracker_secret_key'
    
def test_app_routes_registered(app):
    """Test that all necessary routes are registered.
    
    Verifies that all expected application routes are properly registered
    with the Flask app, including view routes and API endpoints.
    
    Args:
        app (Flask): The Flask application fixture.
    """
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    
    # Check that all expected routes are registered
    assert '/' in routes
    assert '/add' in routes
    assert '/edit/<int:id>' in routes
    assert '/delete/<int:id>' in routes
    assert '/categories' in routes
    assert '/api/expenses' in routes
