# School Test Application

A real-time testing application for schools with student and teacher interfaces.

## 🧪 Testing

[![Backend Tests](https://github.com/A2020GK/school-test/actions/workflows/backend-tests.yml/badge.svg)](https://github.com/A2020GK/school-test/actions/workflows/backend-tests.yml)
[![Frontend Tests](https://github.com/A2020GK/school-test/actions/workflows/frontend-tests.yml/badge.svg)](https://github.com/A2020GK/school-test/actions/workflows/frontend-tests.yml)

### Test Coverage

This application has comprehensive test coverage with **66+ test cases**:

- ✅ **Authentication** - 8 tests
- ✅ **Question Generation** - 24 tests  
- ✅ **Test Manager** - 11 tests
- ✅ **Grade Calculation** - 12 tests
- ✅ **Flask Integration** - 11 tests
- ✅ **Frontend Validation** - JavaScript, HTML, CSS

### Running Tests

#### Quick Start
```bash
./run_tests.sh
```

#### Individual Test Suites
```bash
# Install dependencies
pip install -r requirements.txt

# Run specific tests
python -m unittest test_auth.py -v
python -m unittest test_question.py -v
python -m unittest test_test_manager.py -v
python -m unittest test_routes.py -v
python -m unittest test_integration.py -v

# Run all tests
python -m unittest discover -s . -p "test_*.py" -v
```

#### With Coverage
```bash
pip install coverage
python -m coverage run -m unittest discover -s . -p "test_*.py"
python -m coverage report
python -m coverage html  # Open htmlcov/index.html
```

### Test Documentation

For detailed testing documentation, see:
- **[TESTING.md](TESTING.md)** - Complete testing guide
- **[TEST_SUMMARY.md](TEST_SUMMARY.md)** - Test results and statistics

### Continuous Integration

Tests run automatically via GitHub Actions on:
- Every push to main, develop, or copilot branches
- Every pull request
- Multiple Python versions (3.9, 3.10, 3.11)

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

## 🚀 Usage

### Teacher Interface
Access at: `http://127.0.0.1:5000/teacher`
- Start/stop tests
- Monitor students
- View results

### Student Interface
Access at: `http://<server-ip>:5000`
- Register with name and computer number
- Take tests
- View grades

## 🏗️ Project Structure

```
school-test/
├── app.py                  # Flask application
├── auth.py                 # Authentication module
├── question.py             # Question generation
├── test_manager.py         # Test state management
├── routes.py               # API routes
├── data_manager.py         # Data management
├── static/                 # Frontend files
│   ├── student/           # Student interface
│   └── teacher/           # Teacher interface
├── test_*.py              # Test files (66+ tests)
├── run_tests.sh           # Test runner script
├── TESTING.md             # Testing documentation
├── TEST_SUMMARY.md        # Test summary report
└── .github/workflows/     # CI/CD configuration
    ├── backend-tests.yml
    └── frontend-tests.yml
```

## 🔧 Development

### Prerequisites
- Python 3.9+
- pip
- Node.js 18+ (for frontend validation)

### Setting Up Development Environment
```bash
# Clone the repository
git clone https://github.com/A2020GK/school-test.git
cd school-test

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
./run_tests.sh
```

### Running the Application
```bash
python run.py
```

## 📝 Features

- ✅ Real-time student-teacher communication via WebSocket
- ✅ Two test variants: Powers of 2 and Square Roots
- ✅ Automatic grading system
- ✅ Student registration and management
- ✅ CSV export of results
- ✅ Teacher authentication
- ✅ Comprehensive test coverage

## 🛡️ Testing Infrastructure

### Backend Testing
- Unit tests for all modules
- Integration tests for Flask routes
- Code coverage reporting (78%)
- Automated linting with flake8

### Frontend Testing
- JavaScript syntax validation
- HTML structure validation
- CSS file checks

### CI/CD
- GitHub Actions workflows
- Multi-version testing (Python 3.9, 3.10, 3.11)
- Automated coverage reporting

## 📊 Test Results

Latest test run: **66 tests passed** ✅

```
Coverage Report:
auth.py             100%
test_manager.py     100%
question.py          95%
Overall             78%
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

All contributions must include tests and pass CI checks.

## 📄 License

This project is for educational purposes.

## 👥 Authors

- A2020GK

## 🔗 Links

- [GitHub Repository](https://github.com/A2020GK/school-test)
- [Testing Documentation](TESTING.md)
- [Test Summary](TEST_SUMMARY.md)
