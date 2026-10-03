# Projekt ETL – dane kryptowalut

Projekt automatycznie pobiera bieżące dane o kryptowalutach z CoinGecko, zapisuje je w PostgreSQL i udostępnia do dalszej analizy.

Przepływ danych obsługuje Apache Airflow: co godzinę pobiera ceny oraz podstawowe metryki (m.in. kapitalizację rynkową i wolumen), a następnie zapisuje je w tabeli `crypto_prices_raw`. Środowisko obejmuje również Prometheus i Grafanę do monitoringu.

## Uruchomienie

1. Uzupełnij zmienne wymagane przez `docker-compose.yml` w pliku `.env`.
2. Uruchom usługi:

   ```bash
   docker compose up -d
   ```

3. Otwórz Airflow pod adresem `http://localhost:8080` i uruchom DAG `crypto_price_etl`.

PostgreSQL jest dostępny lokalnie na porcie `5434`, Grafana na `http://localhost:3000`, a Prometheus na `http://localhost:9090`.
