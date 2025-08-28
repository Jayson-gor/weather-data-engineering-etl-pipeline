import importlib

def test_dag_imports():
    # Validate the DAG module imports without raising
    m = importlib.import_module("airflow.dags.dbt_orchastrator")
    dags = [v for v in vars(m).values() if getattr(v, "dag_id", None)]
    dag_ids = {d.dag_id for d in dags}
    assert "weather_dbt_orchestrator" in dag_ids
