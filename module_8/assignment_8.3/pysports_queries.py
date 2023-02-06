#!/usr/bin/env python3
# test queries against a mysql database
# jordan thomas
# Feb 1 2023
# CYBR410

import mysql.connector
from mysql.connector import errorcode

#info for our MySQL server
config = {
    "user": "pysports_user",
    "password": "MySQL8IsGreat!",
    "host": "web",
    "database": "pysports",
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)
    #print("\n Database user {} connected to MySQL on host {} with database {}".format(
    #    config["user"], config["host"],  config["database"]))

    cursor = db.cursor()
    #run a query for all rows in the team table
    cursor.execute("SELECT team_id, team_name, mascot FROM team")
    # teams is an array of objects with the fields we selected
    teams = cursor.fetchall()
    print("-- DISPLAYING TEAM RECORDS --")
    for team in teams:
        print("Team ID: {}".format(team[0]))
        print("Team Name: {}".format(team[1]))
        print("Mascot: {}".format(team[2]))
        print()

    print()
    #run a query for all rows in the player table and print them
    cursor.execute("SELECT player_id, first_name, last_name, team_id FROM player")
    players = cursor.fetchall()
    # players is an array of objects with the fields we selected
    print("-- DISPLAYING PLAYER RECORDS --")
    for player in players:
        print("Player ID: {}".format(player[0]))
        print("First Name: {}".format(player[1]))
        print("Last Name: {}".format(player[2]))
        print("Team ID: {}".format(player[3]))
        print()

# case of failed connection to db
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)
# close our connection to the database so that we're not taking
# up resources on the server for no reason
finally:
    db.close()