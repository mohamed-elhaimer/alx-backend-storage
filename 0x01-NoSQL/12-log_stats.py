#!/usr/bin/env python3
""" 12-log_stats.py """
import pymongo
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs.nginx
    print("{} logs".format(db.count_documents({})))
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        print("\tmethod {}: {}"
              .format(method, db.count_documents({"method": method})))
    print("{} status check"
          .format(db.count_documents({"method": "GET", "path": "/status"})))
