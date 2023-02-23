#!/usr/bin/env python3
# WhatABook main application


import os  # to enable color mode on windows consoles
import platform  # for detection of OS to enable color on windows
import configparser # for reading configuration file
import mysql.connector
from mysql.connector import errorcode


ENABLECOLOR = True
# define colors used in printing messages
if not ENABLECOLOR:
    CYAN = ''
    GREEN = ''
    YELLOW = ''
    RED = ''
    HEADER = ''
    INVERT = ''
    BOLD = ''
    UNDERLINE = ''
    RESETCOLOR = ''
else:
    if platform.system() == "Windows":
        os.system('color')  # this apparently enables ANSI escape codes on windows console
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    HEADER = '\033[95m'
    INVERT = '\033[7m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESETCOLOR = '\033[0m'

# todo - read config from file
# def readConfig(filename):
#     config = configparser.ConfigParser()
#     config.read(filename)
#     print(config.sections())

# readConfig("db.cfg")



config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "web",
    "database": "whatabook",
    "raise_on_warnings": True
}


def printError(message):
    print(RED + message + RESETCOLOR)

def showMainMenu():
    print(BOLD + INVERT + GREEN + "--    MAIN MENU    --" + RESETCOLOR)
    print("[1]:  View Books")
    print("[2]:  View Store Locations")
    print("[3]:  Manage Account")
    print("[4]:  Quit")
    print( GREEN + BOLD + "__________________________" + RESETCOLOR)


def printBooks():
    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()
    print(RESETCOLOR + BOLD + INVERT + GREEN + "--    DISPLAYING BOOK LISTING    --" + RESETCOLOR)
    for book in books:
        print( GREEN + BOLD + "___________________________________________________" + RESETCOLOR)
        print(BOLD + "Book #: "  + RESETCOLOR + GREEN + str(book[0]) + RESETCOLOR)
        print(BOLD + "Book Name: " + RESETCOLOR + book[1])
        print(BOLD + "Author: " + RESETCOLOR + book[2])
        # Summary may or may not exist for a given book, so we can catch a TypeError 
        # if we try to concatenate to a NoneType
        try:
            print(BOLD + "Details: " + RESETCOLOR + book[3])
        except TypeError:
            print(BOLD + "Details: " + RESETCOLOR + RED + "none available" + RESETCOLOR)
    print(GREEN + BOLD + "___________________________________________________\n\n" + RESETCOLOR)

def printLocations():
    print(RESETCOLOR)
    print(BOLD + INVERT + GREEN + "--    LOCATION LISTING    --" + RESETCOLOR)
    print( GREEN + BOLD + "___________________________________________________" + RESETCOLOR)
    cursor.execute("SELECT * FROM store")
    stores = cursor.fetchall()
    for store in stores:
        print(BOLD + "Location: " + RESETCOLOR + store[1])
        print(BOLD + "Hours: " + RESETCOLOR + str(store[2]) + BOLD + " to " + RESETCOLOR + str(store[3]))
    print(GREEN + BOLD + "___________________________________________________\n\n" + RESETCOLOR)

def printAccountMainMenu():
    print(RESETCOLOR)
    print(BOLD + INVERT + GREEN + "--    ACCOUNT MANAGEMENT    --" + RESETCOLOR)
    print("[1]: Wishlist")
    print("[2]: Add Book")   

def validateUser():
    try:
        uid = int(input(RESETCOLOR + BOLD + "Enter your customer ID: " + RESETCOLOR))
        cursor.execute("SELECT * FROM user WHERE user_id = " + str(uid))
        customer = cursor.fetchone()
        #print(customer[0])
        return customer[0]
    except ValueError:
        printError("Enter a numerical customer ID.")
        return False
    except TypeError:
        printError("Sorry, your customer ID was not found.")
        return False


try:
    db = mysql.connector.connect(**config)
    # start
    cursor = db.cursor()
    choice = 0
    while choice != 4:
    # Begin main program logic
        showMainMenu()
        try:
            choice = int(input(BOLD + "ENTER CHOICE: " + RESETCOLOR + GREEN ))  
            if choice > 4 or choice < 1:
                raise ValueError
            elif choice == 1:
                # 1 = View Books
                printBooks()
                input(BOLD + "Press enter to continue: <ENTER>" + RESETCOLOR)
            elif choice == 2:
                # 2 = View Store Locations
                printLocations()
                input(BOLD + "Press enter to continue: <ENTER>" + RESETCOLOR)
            elif choice == 3:
                # 3 = Manage Account
                doneUser = False
                validUser = False
                while not doneUser:
                    while not validUser:
                        customer = validateUser()
                        if customer:
                            validUser = True
                    # we have a valid customer id at customer[0]
                    doneUser = input(BOLD + "Are you done? <Y/N>: " + RESETCOLOR)
                printAccountMainMenu()
                

            print(RESETCOLOR) 
        except ValueError:
            printError("Please enter a number between 1 and 4")
            

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    db.close()