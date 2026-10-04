CREATE_INDEX_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS crypto_index_values (
  index_id TEXT NOT NULL,
  ts       TIMESTAMPTZ NOT NULL,
  value    NUMERIC NOT NULL,
  PRIMARY KEY (index_id, ts)
);

CREATE TABLE IF NOT EXISTS crypto_index_weights (
  index_id  TEXT NOT NULL,
  ts        TIMESTAMPTZ NOT NULL,
  coin_id   TEXT NOT NULL,
  weight    NUMERIC NOT NULL,
  PRIMARY KEY (index_id, ts, coin_id)
);

CREATE INDEX IF NOT EXISTS idx_crypto_index_values_ts
    ON crypto_index_values (ts);

CREATE INDEX IF NOT EXISTS idx_crypto_index_weights_ts
    ON crypto_index_weights (ts);
"""
