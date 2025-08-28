# QA Test Suite

This folder contains an isolated test framework for the weather data engineering pipeline using pytest, testcontainers, and mocks.

## Quick Start

```bash
# Create isolated QA venv
python3 -m venv .qa-venv
source .qa-venv/bin/activate

# Install QA dependencies
pip install -r qa/requirements.txt

# Run all tests
pytest -c qa/pytest.ini --ignore=postgres/
```

## Test Coverage

### test_ingestion.py
- Mocks WeatherStack API responses
- Validates `fetch_data()` function from `api_request/api_request.py`
- Ensures proper JSON parsing and data extraction

### test_dag_import.py
- Validates Airflow DAG imports without syntax errors
- Checks for expected `dag_id` presence
- **Note**: Skipped when Airflow not installed (common in isolated QA venv)

### conftest.py
- Provides Postgres Testcontainers fixture for database tests
- Sets up project path for imports
- Creates ephemeral test database per session

## Running Individual Tests

```bash
# Run only ingestion tests
pytest -c qa/pytest.ini qa/tests/test_ingestion.py -v

# Run with coverage
pytest -c qa/pytest.ini --cov=api_request --cov-report=term-missing
```

## CI/CD Integration

The `.github/workflows/qa.yml` workflow runs these tests on every push/PR to validate:
1. Code imports without errors
2. API parsing logic works correctly  
3. Basic data validation passes

## Notes

- Tests use isolated dependencies to avoid conflicts with runtime stack
- Testcontainers requires Docker to be running
- DAG import tests need Airflow installed (Python 3.11 recommended)
- Database tests use ephemeral containers (no data persistence needed)
