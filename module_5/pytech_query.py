#!/usr/bin/env python3
from pymongo import MongoClient

# connect to mongodb using our URL from Atlas
url = "mongodb+srv://admin:admin@cluster0.523bxky.mongodb.net/pytech"
client = MongoClient(url)
# db is the database within MongoDB we want to connect to
db = client.pytech
col = db["students"]

returnedStudents = {}
ids = range(1007,1010)
def query(id):
    return col.find_one({"student_id": id})

for i in ids:
    returnedStudents[i] = query(str(i))

print("-- DISPLAYING STUDENTS FROM find() QUERY --")
for i in returnedStudents:   
    # print(returnedStudents[i]) 
    print("Student ID: " + returnedStudents[i]["student_id"])
    print("First Name: " + returnedStudents[i]["first_name"])
    print("Last Name:  " + returnedStudents[i]["last_name"])
    print()