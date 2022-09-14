#!/usr/bin/env python

import os
import psycopg2 as pg
from datetime import datetime, timezone
import sys
import requests
import json

def get_data():
    """Get Rekeningku data"""
    url = 'https://api.rekeningku.com/v2/price'
    try:
        r = requests.get(url)
    except Exception as ex:
        print(f"There's been an issue connecting to API, {repr(ex)}")
        sys.exit(1)
    return r.json()

def add_utc_time_key(data):
    """Added current UTC time to Data"""
    now = datetime.now(timezone.utc)
    return [dict(d, **{'update_utc' : now}) for d in data]

def connect_to_db():
    """Connect to database"""
    try:
        conn = pg.connect(host = os.getenv('DATABASE_HOST', default="warehouse"),
                          database = os.getenv('DATABASE_DB'),
                          user = os.getenv('DATABASE_USER'),
                          password = os.getenv('DATABASE_PASSWORD'),
                          port = os.getenv('DATABASE_PORT'))
    except Exception as ex:
        print(f"There's been an issue connecting to database: {repr(ex)}")
        sys.exit(1)
    return conn

def run():
    data = get_data()
    data = add_utc_time_key(data)
    conn = connect_to_db()
    print (json.dumps(data, indent=4, sort_keys=True, default=str))

if __name__ == "__main__":
    run()
    print(f"Update Successful at {datetime.now(timezone.utc)} utc")