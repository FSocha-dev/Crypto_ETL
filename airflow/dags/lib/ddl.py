CREATE_TABLES_SQL =  """
CREATE TABLE IF NOT EXISTS crypto_prices_raw (
  id            BIGSERIAL PRIMARY KEY,
  fetched_at    TIMESTAMPTZ NOT NULL,
  source        TEXT NOT NULL DEFAULT 'coingecko',
  coin_id       TEXT NOT NULL,
  currency      TEXT NOT NULL DEFAULT 'usd',
  price         NUMERIC(20, 8) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_crypto_prices_raw_coin_time
  ON crypto_prices_raw (coin_id, fetched_at);

CREATE INDEX IF NOT EXISTS idx_crypto_prices_raw_fetched_at
  ON crypto_prices_raw (fetched_at);

ALTER TABLE crypto_prices_raw
  ADD COLUMN IF NOT EXISTS market_cap NUMERIC,
  ADD COLUMN IF NOT EXISTS vol_24h NUMERIC,
  ADD COLUMN IF NOT EXISTS change_24h NUMERIC,
  ADD COLUMN IF NOT EXISTS last_updated_at BIGINT;

CREATE TABLE IF NOT EXISTS etl_runs (
  id               BIGSERIAL PRIMARY KEY,
  dag_id           TEXT NOT NULL,
  run_id           TEXT NOT NULL,
  task_id          TEXT,
  status           TEXT NOT NULL,
  started_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  finished_at      TIMESTAMPTZ,
  records_inserted INTEGER,
  error_message    TEXT
);

CREATE INDEX IF NOT EXISTS idx_etl_runs_dag_time
  ON etl_runs (dag_id, started_at);
"""