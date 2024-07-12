#!/usr/bin/env python3
""" Logs Nginx from MongoDB and prints stats
"""
from pymongo import MongoClient


def stats():
    """ stats function """
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx
    print(f"{collection.count_documents({})} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    status_get = collection.count_documents(
        {'method': 'GET', 'path': '/status'})
    print(f"{status_get} status check")
    print("IPs:")
    pipeline = [
        {
            "$group": {
                "_id": "$ip",
                "count": {
                    "$sum": 1
                }
            }
        },
        {
            "$sort": {
                "count": -1
            }
        },
        {
            "$limit": 10
        }
    ]
    for doc in collection.aggregate(pipeline):
        print(f"\t{doc['_id']}: {doc['count']}")


if __name__ == "__main__":
    stats()
