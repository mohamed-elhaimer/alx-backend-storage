#!/usr/bin/env python3
""" 11-schools_by_topic """


def schools_by_topic(mongo_collection, topic):
  """ find a list of school with a specific topic """

  return mongo_collection.find({"topics": topic})
