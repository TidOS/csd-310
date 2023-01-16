#!/usr/bin/env python3
# Jordan Thomas
# Jan 15, 2023
# CYBR-410-T301
from pymongo import MongoClient

# connect to mongodb using our URL from Atlas
url = "mongodb+srv://admin:admin@cluster0.523bxky.mongodb.net/pytech"
client = MongoClient(url)
# db is the database within MongoDB we want to connect to
db = client.pytech
col = db["students"]

# get all Student documents and print them
returnedStudents = col.find({})
print("-- DISPLAYING STUDENTS FROM find() QUERY --")
for i in returnedStudents:
    print("Student ID: " + i["student_id"])
    print("First Name: " + i["first_name"])
    print("Last Name:  " + i["last_name"])
    print()


# get 1 instance of students with ids 1007, 1008, 1009 and print them
returnedStudents = {}
ids = range(1007,1010)
def query(id):
    return col.find_one({"student_id": id})

for i in ids:
    returnedStudents[i] = query(str(i))

print("-- DISPLAYING STUDENTS FROM find_one() QUERY --")
for i in returnedStudents:   
    # print(returnedStudents[i]) 
    print("Student ID: " + returnedStudents[i]["student_id"])
    print("First Name: " + returnedStudents[i]["first_name"])
    print("Last Name:  " + returnedStudents[i]["last_name"])
    print()