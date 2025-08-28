import importlib
import pytest

def test_dag_imports():
    # Skip this test if Airflow is not installed (common in isolated QA venv)
    try:
        # Check if airflow is available
        importlib.import_module("airflow")
    except ImportError:
        pytest.skip("Airflow not installed in QA venv; skipping DAG import test")
    
    # Validate the DAG module imports without raising
    m = importlib.import_module("airflow.dags.dbt_orchastrator")
    dags = [v for v in vars(m).values() if getattr(v, "dag_id", None)]
    dag_ids = {d.dag_id for d in dags}
    assert "weather_dbt_orchestrator" in dag_ids
