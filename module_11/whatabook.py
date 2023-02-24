#!/usr/bin/env python3
# WhatABook main application


import os  # to enable color mode on windows consoles
import sys # to quit more eloquently
import platform  # for detection of OS to enable color on windows
#import configparser # for reading configuration file
import mysql.connector
from mysql.connector import errorcode

DEBUGMODE = True    # print additional messages during runtime
ENABLECOLOR = True  # use colors in the terminal emulator
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
    ''''prints error message in red.  
    If ENABLECOLOR is not set, still print the message, 
    but RED will be defined to be an empty string'''
    print(RED + message + RESETCOLOR)

def debug(message):
    ''''prints debug messages in YELLOW
    If ENABLECOLOR is not set, still print the message,
    but YELLOW will be defined to be an empty string'''
    print(YELLOW + message + RESETCOLOR)

def showMainMenu():
    ''''Print the main menu, logic is done in main()'''
    debug("Main Menu called.")
    print(BOLD + INVERT + GREEN + "--    MAIN MENU    --" + RESETCOLOR)
    print("[1]:  View Books")
    print("[2]:  View Store Locations")
    print("[3]:  Manage Account")
    print("[4]:  Quit")
    print( GREEN + BOLD + "__________________________" + RESETCOLOR)


def printBooks():
    ''''print all books in the whatabook.book table'''
    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()
    print(RESETCOLOR + BOLD + INVERT + GREEN + "--    DISPLAYING BOOK LISTING    --" + RESETCOLOR)
    for book in books:
        printBookSingle(book)
    print(GREEN + BOLD + "___________________________________________________\n\n" + RESETCOLOR)

def printBookSingle(book):
    '''prints a book, if no summary is available it is noted in yellow text that it is unavailable'''
    # a book should have 4 entries (in order)
    # book_id, book_name, author, summary
    # summary can be null or empty but the rest cannot.
    print( GREEN + BOLD + "___________________________________________________" + RESETCOLOR)
    print(BOLD + "Book #: "  + RESETCOLOR + GREEN + str(book[0]) + RESETCOLOR)
    print(BOLD + "Book Name: " + RESETCOLOR + book[1])
    print(BOLD + "Author: " + RESETCOLOR + book[2])
    # Summary may or may not exist for a given book, so we can catch a TypeError 
    # if we try to concatenate to a NoneType
    try:
        print(BOLD + "Details: " + RESETCOLOR + book[3])
    except TypeError:
        debug("A book with no summary was found in printBookSingle().")
        print(BOLD + "Details: " + RESETCOLOR + YELLOW + "none available" + RESETCOLOR)

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
    print("[3]: Return to Main Menu")

def validateUser():
    try:
        uid = int(input(RESETCOLOR + BOLD + "Enter your customer ID: " + RESETCOLOR))
        cursor.execute("SELECT * FROM user WHERE user_id = " + str(uid))
        customer = cursor.fetchone()
        if DEBUGMODE:
            debug("Customer found: {}\nName: {} {}".format(str(customer[0]),customer[1],customer[2]))
        return customer[0]
    except ValueError:
        debug("A number was not entered.")
        printError("Enter a numerical customer ID.")
        return False
    except TypeError:
        debug("A number was found but a matching user was not.")
        printError("Sorry, your customer ID was not found.")
        return False

def showWishlist(customer):
    '''prints the current wish list of a customer
    the input customer is the id number of the customer'''
    print(RESETCOLOR)
    print(BOLD + INVERT + GREEN + "--    WISHLIST LISTING    --" + RESETCOLOR)
    print( GREEN + BOLD + "___________________________________________________" + RESETCOLOR)
    if DEBUGMODE:
        debug("SQL QUERY: SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author, book.summary " + 
        "FROM wishlist " + 
        "INNER JOIN user ON wishlist.user_id = user.user_id " + 
        "INNER JOIN book ON wishlist.book_id = book.book_id " + 
        "WHERE user.user_id = " +str(customer))
    cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author, book.summary " + 
    "FROM wishlist " + 
    "INNER JOIN user ON wishlist.user_id = user.user_id " + 
    "INNER JOIN book ON wishlist.book_id = book.book_id " + 
    "WHERE user.user_id = " +str(customer))
    wishlist = cursor.fetchall()
    # wishlist should be a list with all our user's wishlist items and user info
    for i in wishlist:
        book = (i[3], i[4], i[5], i[6])
        printBookSingle(book)
    print( GREEN + BOLD + "___________________________________________________" + RESETCOLOR)

def showAvailableBooks(customer):
    ''''prints a list of books not currently in the user's wishlist
    Then allows user to add a book by its id
    This function returns a list of book_ids that are available to the user
    '''
    print(RESETCOLOR)
    print(BOLD + INVERT + GREEN + "--    AVAILABLE BOOK LISTING    --" + RESETCOLOR)
    print( GREEN + BOLD + "___________________________________________________" + RESETCOLOR)
    cursor.execute("SELECT book_id, book_name, author, summary FROM book "+ 
    "WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = " + str(customer)+")")
    books = cursor.fetchall()
    bookindexes = []
    for book in books:
        bookindexes.append(book[0])
        #book = (i[0], i[1], i[2], i[3])
        printBookSingle(book)
    return bookindexes

def addBookToWishlist(customer, book_id):
    '''Insert a book_id into a customer's wish list given the customer id and book_id
    Error checking on these numbers should have been done in the main program logic'''
    if DEBUGMODE:
        debug("inserting into wishlist -> " + str(customer) + " " + str(book_id) )
        debug("SQL COMMAND: " + "INSERT INTO wishlist(user_id, book_id) VALUES("+ str(customer) + ", " + str(book_id) + ")")
    cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES("+ str(customer) + ", " + str(book_id) + ");")
    db.commit()
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
                validUser = False
                account_action = 0
                goback = "n"
                while goback.lower() != "y":
                    while not validUser:
                        customer = validateUser()
                        if customer:
                            validUser = True
                        else:
                            quitFromNoUserID = input(BOLD + "Quit Program? <Y/N> " + RESETCOLOR)
                            if  quitFromNoUserID.lower() == "y":
                                db.close()
                                sys.exit(1)
                    # If we get here, we should have a valid customer id in customer
                    printAccountMainMenu()
                    try:
                        account_action = int(input(BOLD + "ENTER CHOICE: " + RESETCOLOR + GREEN))
                        while goback.lower() != "y":
                            if account_action == 1:
                                showWishlist(customer)
                                #goback = input(BOLD + "GO BACK? <Y/N>: " + RESETCOLOR + GREEN)
                                break
                            elif account_action == 2:
                                bookadded = False
                                while not bookadded:
                                    bookindexes = showAvailableBooks(customer)
                                    #bookindexes is a list of book ids that are not in the wishlist for the customer
                                    try:
                                        indextoadd = int(input(RESETCOLOR + BOLD + "Enter the ID # of the book you wish to add: <#> " + RESETCOLOR))
                                        if DEBUGMODE:
                                            debug("is index to add in available books?  " + str(indextoadd in bookindexes))
                                        if indextoadd not in bookindexes:
                                            printError("The book was not available to add to the wishlist")
                                            printError("Please re-review the available options and choose again: ")
                                            input(BOLD + "Press enter to continue <ENTER> " + RESETCOLOR)
                                        else:
                                            bookadded = True
                                    except ValueError:
                                        printError("Enter a number.")
                                        printError("Please re-review the available options and choose again: ")
                                        input(BOLD + "Press enter to continue <ENTER> " + RESETCOLOR)
                                    
                                    # if we get here, we should have the id of the book to id and the customer id in "customer"
                                addBookToWishlist(customer, indextoadd)
                                #goback = input(BOLD + "GO BACK? <Y/N>: " + RESETCOLOR + GREEN)
                                break
                            elif account_action == 3:
                                goback = "y"
                    except ValueError:
                        input("press enter to continue <ENTER>")
            elif choice == 4:
                db.close()
                sys.exit(0)
            print(RESETCOLOR) 
        except ValueError:
            printError("Please enter a number between 1 and 4")
            

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        printError("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        printError("  The specified database does not exist")
    else:
        printError(err)
finally:
    db.close()