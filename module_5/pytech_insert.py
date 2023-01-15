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

# define our students and put them in an array 
student1007 = {
    "student_id": "1007",
    "first_name": "Fred",
    "last_name": "Flintstone"
}

student1008 = {
    "student_id": "1008",
    "first_name": "Bill",
    "last_name": "Clinton"
}

student1009 = {
    "student_id": "1009",
    "first_name": "George",
    "last_name": "Washington"
}
students = [student1007, student1008, student1009]
print("-- INSERT STATEMENTS --")
for i in students:
    returnedID = col.insert_one(i).inserted_id
    print("Inserted student record " + i["first_name"] + " " + i["last_name"] + 
    "into the students collection with document_id " + str(returnedID))