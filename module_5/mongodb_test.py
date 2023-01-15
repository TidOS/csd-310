#!/usr/bin/env python3
from pymongo import MongoClient

# connect to mongodb using our URL from Atlas
url = "mongodb+srv://admin:admin@cluster0.523bxky.mongodb.net/pytech"
client = MongoClient(url)
# db is the database within MongoDB we want to connect to
db = client.pytech

print("-- Pytech Collection List --")
print(db.list_collection_names())