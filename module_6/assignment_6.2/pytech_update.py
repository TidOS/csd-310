#!/usr/bin/env python3
# Jordan Thomas
# Jan 18, 2023
# CYBR-410-T301
from pymongo import MongoClient

# connect to mongodb using our URL from Atlas
url = "mongodb+srv://admin:admin@cluster0.523bxky.mongodb.net/pytech"
client = MongoClient(url)
# db is the database within MongoDB we want to connect to
db = client.pytech
col = db["students"]

# print all students in the collection
returnedStudents = col.find({})
print("-- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")
for i in returnedStudents:
    print("Student ID: " + i["student_id"])
    print("First Name: " + i["first_name"])
    print("Last Name:  " + i["last_name"])
    print()

# update student 1007 with a new name, "someguy"
col.update_one({"student_id": "1007"}, {"$set": {"last_name": "someguy"}})

print("-- DISPLAYING STUDENT DOCUMENT 1007 -- ")
returnedStudent = col.find_one({"student_id": "1007"})
print("Student ID: " + returnedStudent["student_id"])
print("First Name: " + returnedStudent["first_name"])
print("Last Name:  " + returnedStudent["last_name"])
print()
