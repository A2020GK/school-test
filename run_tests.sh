#!/bin/bash
# Test runner script for the school-test application

set -e  # Exit on error

echo "=========================================="
echo "Running Backend Tests for School Test App"
echo "=========================================="
echo ""

# Check if virtual environment exists, if not, create it
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "=========================================="
echo "Running Unit Tests"
echo "=========================================="
echo ""

# Run authentication tests
echo "Testing Authentication Module..."
python -m unittest test_auth.py -v
echo ""

# Run question tests
echo "Testing Question Generation Module..."
python -m unittest test_question.py -v
echo ""

# Run test manager tests
echo "Testing Test Manager Module..."
python -m unittest test_test_manager.py -v
echo ""

# Run routes tests
echo "Testing Routes Module..."
python -m unittest test_routes.py -v
echo ""

echo "=========================================="
echo "Running Integration Tests"
echo "=========================================="
echo ""

# Run integration tests
echo "Testing Flask Routes..."
python -m unittest test_integration.py -v
echo ""

echo "=========================================="
echo "All Tests Passed Successfully! ✓"
echo "=========================================="

# Run all tests with coverage if coverage is installed
if command -v coverage &> /dev/null; then
    echo ""
    echo "=========================================="
    echo "Running Coverage Report"
    echo "=========================================="
    coverage run -m unittest discover -s . -p "test_*.py"
    coverage report
    coverage html
    echo "HTML coverage report generated in htmlcov/"
fi
