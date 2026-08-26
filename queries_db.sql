SELECT * FROM crypto_prices_raw
ORDER BY 1 DESC;

SELECT * FROM etl_runs
ORDER BY 1 DESC;


SELECT coin_id, MIN(fetched_at)
  FROM crypto_prices_raw
 WHERE currency = 'usd' AND coin_id IN ('bitcoin', 'ethereum', 'solana')
GROUP BY coin_id;

SELECT price
  FROM crypto_prices_raw
 WHERE coin_id IN ('bitcoin', 'ethereum', 'solana') 
   AND currency = 'usd' 
   AND fetched_at <= %s
ORDER BY fetched_at DESC
LIMIT 1;