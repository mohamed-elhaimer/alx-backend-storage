#!/usr/bin/env python3
"""
list_all use pymongo
"""
import pymongo

def list_all(mongo_collection):
  """ list all in a collection """
  return mongo_collection.find()
