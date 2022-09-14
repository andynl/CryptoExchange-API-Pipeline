#!/usr/bin/env python

from psycopg2.extras import execute_values
import os
import psycopg2 as pg
from datetime import datetime, timezone
import sys
import requests
import json
from dotenv import load_dotenv

def get_data():
    """Get Rekeningku data"""
    url = 'https://api.rekeningku.com/v2/price'
    try:
        r = requests.get(url)
    except Exception as ex:
        print("There's been an issue connecting to API")
        sys.exit(1)
    return r.json()

def add_utc_time_key(data):
    """Added current UTC time to Data"""
    now = datetime.now(timezone.utc)
    return [dict(d, **{'update_utc' : now}) for d in data]

def connect_to_db():
    """Connect to database"""
    load_dotenv()
    try:
        conn = pg.connect(host = os.getenv('POSTGRES_HOST', default="localhost"),
                          database = os.getenv('POSTGRES_DB'),
                          user = os.getenv('POSTGRES_USER'),
                          password = os.getenv('POSTGRES_PASSWORD'),
                          port = os.getenv('POSTGRES_PORT'))
    except Exception as ex:
        print(f"There's been an issue connecting to database: {ex}")
        sys.exit(1)
    return conn

def remove_mk_key(data):
    """Remove MK Key from Data if exists"""
    return [{k: v for k, v in d.items() if k != 'mk'} for d in data]

def remove_st_key(data):
    """Remove ST Key from Data if exists"""
    return [{k: v for k, v in d.items() if k != 'st'} for d in data]

def ingest_data(conn, data):
    """Load data into database"""
    cur = conn.cursor()
    columns = ['coin_name', 'id', 'coin_code', 'close_price', 'last_transaction_type', 'high_price', 'low_price', 'open_price', 'volume', 'change_percentage', 'update_utc']
    cols = ','.join(columns)
    query = "INSERT INTO crypto.assets ({}) VALUES %s".format(cols)
    values = [[value for value in coin.values()] for coin in data]
    try:
        execute_values(cur, query, values)
    except Exception as ex:
        print(f"There's been an issue connecting to database: {ex}")
        sys.exit(1)
    conn.commit()

def run():
    data = get_data()
    data = add_utc_time_key(data)
    data = remove_mk_key(data)
    data = remove_st_key(data)
    conn = connect_to_db()
    ingest_data(conn, data)
    # print (json.dumps(data, indent=4, sort_keys=True, default=str))

if __name__ == "__main__":
    run()
    print(f"Update Successful at {datetime.now(timezone.utc)} utc")