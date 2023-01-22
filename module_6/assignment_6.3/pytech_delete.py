#!/usr/bin/env python3
# Jordan Thomas
# Jan 21, 2023
# CYBR-410-T301
from pymongo import MongoClient

# connect to mongodb using our URL from Atlas
# 6.3.2
url = "mongodb+srv://admin:admin@cluster0.523bxky.mongodb.net/pytech"
client = MongoClient(url)
# db is the database within MongoDB we want to connect to
db = client.pytech
col = db["students"]

def printAll():   
    '''prints all students in the collection'''
    returnedStudents = col.find({})
    print("-- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")
    for i in returnedStudents:
        print("Student ID: " + i["student_id"])
        print("First Name: " + i["first_name"])
        print("Last Name:  " + i["last_name"])
        print()

# 6.3.3 -----------------------------------
# print all students using find()
printAll()
#------------------------------------------


# 6.3.4 ------------------------------------
# create a student to insert
student1010 = {
    "student_id": "1010",
    "first_name": "Donald",
    "last_name": "Trump"
}

# insert student1010 and print it alongside its document_id
print("-- INSERT STATEMENTS --")
returnedID = col.insert_one(student1010).inserted_id
print("Inserted student record into the students collection with document_id " 
+ str(returnedID))
#------------------------------------------

# 6.3.5 -----------------------------------
# search for the test student and print out its information
print("-- DISPLAYING STUDENT DOCUMENT 1010 TEST DOC -- ")
returnedStudent = col.find_one({"student_id": "1010"})
print("Student ID: " + returnedStudent["student_id"])
print("First Name: " + returnedStudent["first_name"])
print("Last Name:  " + returnedStudent["last_name"])
print()
#------------------------------------------

# 6.3.6 -----------------------------------
# delete student 1010
col.delete_one({"student_id": "1010"})
#------------------------------------------

# 6.3.7 -----------------------------------
# reprint all students to see if the test student was deleted
printAll()
#------------------------------------------
