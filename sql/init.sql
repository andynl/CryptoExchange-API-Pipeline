CREATE SCHEMA IF NOT EXISTS crypto;
CREATE TABLE IF NOT EXISTS crypto.assets (
    id VARCHAR(50) NOT NULL,
    coin_name VARCHAR(50),
    coin_code VARCHAR(50),
    close_price NUMERIC,
    last_transaction_type NUMERIC,
    high_price NUMERIC,
    low_price NUMERIC,
    open_price NUMERIC,
    volume NUMERIC,
    change_percentage NUMERIC,
    update_utc TIMESTAMP WITH TIME ZONE
);