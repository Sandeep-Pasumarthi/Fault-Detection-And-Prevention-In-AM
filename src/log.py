from cassandra_ops import CassandraDBManagement
from datetime import date
import time
import os

BUNDLE_PATH = os.path.join("src", "secure-connect-ai14predictivemaintenance.zip")
CLIENT_ID = "rwQwrUoTqtCSDQxfJTCYmRKz"
CLIENT_SECRET = "ExLBPzzNWZYPGTE7+s3djY7HGferjymf5DejRt3zbsC_+70ObwrHv7+-WKUcQq0wrglZWM-t7c," \
                "on5TWNmtsttQOW,d.M8ZbN+o0OnZJSCBUZqe2Sgxec8DhEOz,8YC6"
KEYSPACE = "logged_data"
TABLE_NAME = "log"


def get_manager():
    manager = CassandraDBManagement(BUNDLE_PATH, CLIENT_ID, CLIENT_SECRET)
    return manager


def log_detail(manager, messages):
    values = []
    for i in messages:
        today = date.today().strftime("%y-%m-%d")
        now = time.localtime()
        now = time.strftime("%H:%M:%S", now)
        values.append([i, today, now])
    manager.insert_values(KEYSPACE, TABLE_NAME, values)
