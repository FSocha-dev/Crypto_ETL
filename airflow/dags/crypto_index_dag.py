from datetime import datetime, timezone
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator      
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sensors.external_task import ExternalTaskSensor

from lib.ddl_index import CREATE_INDEX_TABLES_SQL

INDEX_ID = "CMI3_CAP" #Crypto Market Index 3 Market Cap
COINS = ["bitcoin", "ethereum", "binancecoin"]
CURRENCY = "usd"

def compute_index_value(ti, **context) -> float:

    hook = PostgresHook(postgres_conn_id="postgres_default")
    conn = hook.get_conn()
    cur = conn.cursor()

    ts_now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)

    try:
        cur.execute(
            """
            SELECT coin_id, MIN(fetched_at)
            FROM crypto_prices_raw
            WHERE currency = %s AND coin_id = ANY(%s)
            GROUP BY coin_id
            """,
                (CURRENCY, COINS),
        )
        mins = {coin_id: ts for coin_id, ts in cur.fetchall()}
        if len(mins) != len(COINS):
            missing = set(COINS) - set(min.keys())
            raise ValueError(f"Missing baseline data for coins: {missing}")
        
        t0 = max(min.values())

        #dalsze rozwiniecie funkcji

    finally:
        cur.close()
        conn.close()
        