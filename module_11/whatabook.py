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

def readConfig(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    print(config.sections())

readConfig("db.cfg")

config = {
    "user": "pysports_user",
    "password": "MySQL8IsGreat!",
    "host": "localhost",
    "database": "pysports",
    "raise_on_warnings": True
}