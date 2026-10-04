from datetime import datetime, timezone

from airflow.providers.postgres.hooks.postgres import PostgresHook


def insert_prices_and_log_run(
    data: dict,
    dag_id: str,
    run_id: str,
    postgres_conn_id: str = "postgres_default",
    source: str = "coingecko",
    currency: str = "usd",
) -> int:

    fetched_at = datetime.now(timezone.utc)

    mc_key = f"{currency}_market_cap"
    vol_key = f"{currency}_24h_vol"
    change_key = f"{currency}_24h_change"
    last_updated_key = "last_updated_at"

    rows = [
        (
            fetched_at,
            source,
            coin_id,
            currency,
            values[currency],
            values.get(mc_key),
            values.get(vol_key),
            values.get(change_key),
            values.get(last_updated_key),
        )
        for coin_id, values in data.items()
        if currency in values
    ]

    hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    conn = hook.get_conn()
    cur = conn.cursor()

    try:
        cur.executemany(
            """
            INSERT INTO crypto_prices_raw (fetched_at, source, coin_id, currency, price, market_cap, vol_24h, change_24h, last_updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            rows,
        )

        cur.execute(
            """
            INSERT INTO etl_runs (dag_id, run_id, task_id, status, finished_at, records_inserted)
            VALUES (%s, %s, %s, %s, now(), %s)
            """,
            (dag_id, run_id, "load_prices", "success", len(rows)),
        )

        conn.commit()
        return len(rows)

    except Exception as e:
        conn.rollback()
        cur.execute(
            """
            INSERT INTO etl_runs (dag_id, run_id, task_id, status, finished_at, error_message)
            VALUES (%s, %s, %s, %s, now(), %s)
            """,
            (dag_id, run_id, "load_prices", "failed", str(e)),
        )
        conn.commit()
        raise

    finally:
        cur.close()
        conn.close()
