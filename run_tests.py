#!/usr/bin/env python3
"""
A simple test script to run all tests with coverage and generate reports.
"""
import pytest
import os
import sys
import argparse

def main():
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
