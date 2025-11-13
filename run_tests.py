#!/usr/bin/env python3
"""Test runner script for the expense tracker application.

This script provides a command-line interface for running tests with coverage
reporting. It supports multiple output formats including terminal, HTML, and XML.

Usage:
    python run_tests.py              # Run tests with terminal coverage report
    python run_tests.py --html       # Generate HTML coverage report
    python run_tests.py --xml        # Generate XML coverage report for CI/CD
    python run_tests.py --verbose    # Run with verbose output

Examples:
    python run_tests.py --html --verbose
    python run_tests.py --xml
"""

import pytest
import os
import sys
import argparse


def main():
    """Run the test suite with coverage reporting.
    
    Parses command-line arguments and executes pytest with appropriate
    configuration for coverage reporting.
    
    Returns:
        int: Exit code from pytest (0 for success, non-zero for failures).
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
