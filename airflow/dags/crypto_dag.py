from datetime import datetime, timezone

from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from get_crypto_prices import get_crypto_prices
from lib.db import insert_prices_and_log_run
from lib.ddl import CREATE_TABLES_SQL

from airflow import DAG


def load_prices_task(ti, **context):
    data = ti.xcom_pull(task_ids="fetch_prices")
    insert_prices_and_log_run(
        data=data,
        dag_id=context["dag"].dag_id,
        run_id=context["run_id"],
        postgres_conn_id="postgres_default",
        source="coingecko",
        currency="usd",
    )


with DAG(
    dag_id="crypto_price_etl",
    start_date=datetime(2026, 1, 8, tzinfo=timezone.utc),
    schedule="@hourly",
    catchup=False,
    tags=["crypto"],
) as dag:

    create_tables = SQLExecuteQueryOperator(
        task_id="create_tables",
        conn_id="postgres_default",
        sql=CREATE_TABLES_SQL,
    )

    fetch_prices = PythonOperator(
        task_id="fetch_prices",
        python_callable=get_crypto_prices,
    )

    load_prices = PythonOperator(
        task_id="load_prices",
        python_callable=load_prices_task,
    )

    create_tables >> fetch_prices >> load_prices
