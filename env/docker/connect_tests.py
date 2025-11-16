#!/usr/bin/env python3
"""
Connection and import/version test for database connectors.
Run this inside the running Superset container (or from host via
`docker compose exec -T superset python /app/connect_tests.py`).

Tests performed:
- package distribution versions (importlib.metadata)
- import of driver modules
- simple connection tests for MySQL (mysqlclient) and ClickHouse (native)

Defaults assume test services named `env-test-mariadb-1` and
`env-test-clickhouse-1` on the same Docker network. You can override via
environment variables: MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS,
CH_HOST, CH_PORT.
"""

import os
import sys
import traceback
from importlib import metadata

pkgs = [
    ("mysqlclient", "mysqlclient"),
    ("PyMySQL", "PyMySQL"),
    ("clickhouse-driver", "clickhouse-driver"),
    ("clickhouse-connect", "clickhouse-connect"),
    ("clickhouse-sqlalchemy", "clickhouse-sqlalchemy"),
    ("phoenixdb", "phoenixdb"),
    ("happybase", "happybase"),
    ("PyHive", "PyHive"),
    ("SQLAlchemy", "SQLAlchemy"),
]

print("== Package distribution versions ==")
for pretty, dist in pkgs:
    try:
        v = metadata.version(dist)
        print(f"{pretty}: {v}")
    except Exception as e:
        print(f"{pretty}: not installed ({e})")

print("\n== Module import checks ==")
modules = [
    ("MySQLdb", "MySQLdb"),
    ("pymysql", "pymysql"),
    ("clickhouse_driver", "clickhouse_driver"),
    ("clickhouse_connect", "clickhouse_connect"),
    ("clickhouse_sqlalchemy", "clickhouse_sqlalchemy"),
    ("phoenixdb", "phoenixdb"),
    ("happybase", "happybase"),
    ("pyhive", "pyhive"),
    ("sqlalchemy", "sqlalchemy"),
]
for name, mod in modules:
    try:
        __import__(mod)
        print(f"OK: import {mod}")
    except Exception:
        print(f"ERR: import {mod}")
        traceback.print_exc()

print("\n== Runtime connection tests ==")
# MySQL parameters
MYSQL_HOST = os.environ.get("MYSQL_HOST", "env-test-mariadb-1")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", "3306"))
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASS = os.environ.get("MYSQL_PASS", "test")

# ClickHouse parameters
CH_HOST = os.environ.get("CH_HOST", "env-test-clickhouse-1")
CH_PORT = int(os.environ.get("CH_PORT", "9000"))

# Run MySQL test (mysqlclient)
try:
    import MySQLdb
    print(f"\n-- MySQL test -> connecting to {MYSQL_HOST}:{MYSQL_PORT} as {MYSQL_USER}")
    conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASS, port=MYSQL_PORT, connect_timeout=5)
    cur = conn.cursor()
    cur.execute('SELECT 1')
    print("MySQL SELECT 1 ->", cur.fetchone())
    cur.close()
    conn.close()
except Exception as e:
    print("MySQL test failed:", repr(e))
    traceback.print_exc()

# Run ClickHouse native test
try:
    from clickhouse_driver import Client
    print(f"\n-- ClickHouse native test -> connecting to {CH_HOST}:{CH_PORT}")
    client = Client(host=CH_HOST, port=CH_PORT)
    res = client.execute('SELECT 1')
    print("ClickHouse native SELECT 1 ->", res)
except Exception as e:
    print("ClickHouse native test failed:", repr(e))
    traceback.print_exc()

# Try ClickHouse HTTP endpoint (8123) as a fallback
try:
    import requests
    print(f"\n-- ClickHouse HTTP test -> http://{CH_HOST}:8123/")
    r = requests.get(f'http://{CH_HOST}:8123/', params={'query': 'SELECT 1'})
    print("HTTP status:", r.status_code)
    print(r.text.strip()[:400])
except Exception as e:
    print("ClickHouse HTTP test failed:", repr(e))
    traceback.print_exc()

print('\n== Done ==')

if __name__ == '__main__':
    sys.exit(0)
