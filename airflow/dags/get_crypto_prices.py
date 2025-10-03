import requests 

import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="crypto_prices_dag",
    start_date=datetime.datetime(2025, 2, 3),
    schedule="@daily",
):
    EmptyOperator(task_id="task")