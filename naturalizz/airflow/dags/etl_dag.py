from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from ..tasks import retrieve_taxon_data

schedule_interval = "@daily"
start_date = days_ago(1)
with DAG(
    dag_id="taxon_data_pipeline",
    schedule_interval=schedule_interval,
    start_date=start_date,
    catchup=True,
    # max_active_runs=1,
) as dag:
    etl = PythonOperator(
        task_id="extract_taxon_data",
        python_callable=retrieve_taxon_data,
    )
