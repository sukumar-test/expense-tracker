#!/usr/bin/env python3
"""Test runner script for the Expense Tracker application.

This script provides a command-line interface for running the test suite
with various options for coverage reporting. It uses pytest as the testing
framework and pytest-cov for code coverage analysis.

The script supports:
- Running all tests with coverage reporting
- Generating HTML coverage reports for detailed analysis
- Generating XML coverage reports for CI/CD integration
- Verbose output mode for detailed test information

Usage:
    Basic usage (terminal coverage report)::
    
        $ python run_tests.py
        
    With HTML coverage report::
    
        $ python run_tests.py --html
        
    With XML coverage report for CI/CD::
    
        $ python run_tests.py --xml
        
    With verbose output::
    
        $ python run_tests.py --verbose

Exit Codes:
    0: All tests passed
    Non-zero: Tests failed or encountered errors
"""
import pytest
import os
import sys
import argparse

def main():
    """Main function to run tests with coverage.
    
    Parses command-line arguments and executes pytest with appropriate
    coverage options. Displays success message if all tests pass.
    
    Returns:
        int: Exit code from pytest (0 for success, non-zero for failure).
        
    Command-line Arguments:
        --html: Generate HTML coverage report in htmlcov/ directory.
        --xml: Generate XML coverage report as coverage.xml (for CI/CD).
        --verbose, -v: Enable verbose test output.
        
    Examples:
        >>> # Run tests with HTML and XML reports
        >>> sys.argv = ['run_tests.py', '--html', '--xml']
        >>> exit_code = main()
        >>> assert exit_code == 0  # All tests passed
    """
    parser = argparse.ArgumentParser(description="Run tests for Expense Tracker with coverage.")
    parser.add_argument("--html", action="store_true", help="Generate HTML coverage report")
    parser.add_argument("--xml", action="store_true", help="Generate XML coverage report for CI/CD")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    # Add the parent directory to sys.path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # Build pytest arguments
    pytest_args = []
    
    if args.verbose:
        pytest_args.append("-v")
    
    # Always run with coverage
    pytest_args.append("--cov=app")
    pytest_args.append("--cov-report=term")
    
    # Add HTML coverage report if requested
    if args.html:
        pytest_args.append("--cov-report=html")
        print("HTML coverage report will be generated in htmlcov/ directory")
        
    # Add XML coverage report if requested (useful for CI/CD)
    if args.xml:
        pytest_args.append("--cov-report=xml")
        print("XML coverage report will be generated as coverage.xml")
    
    # Add the tests directory
    pytest_args.append("tests/")
    
    # Run pytest with constructed arguments
    exit_code = pytest.main(pytest_args)
    
    # Display coverage information
    if exit_code == 0:
        print("\n✅ All tests passed!")
        
    # Exit with pytest's exit code
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
