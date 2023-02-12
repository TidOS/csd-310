#!/usr/bin/env python3
# join tables to show team names for players in database
# jordan thomas
# Feb 12 2023
# CYBR410

import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "pysports_user",
    "password": "MySQL8IsGreat!",
    "host": "localhost",
    "database": "pysports",
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)
    # start
    cursor = db.cursor()
    #run a query that joins the player table (left) with the team table (right) 
    #where the team_id matches from each table.  We want the player id, first name,
    #last name, and team name
    cursor.execute("SELECT player_id, first_name, last_name, team_name from player "+
    "inner join team on player.team_id = team.team_id")
    # teams is an array of objects with the fields we selected
    players = cursor.fetchall()
    print("-- DISPLAYING PLAYER RECORDS --")
    for player in players:
        print("Player ID: {}".format(player[0]))
        print("First Name: {}".format(player[1]))
        print("Last Name: {}".format(player[2]))
        print("Team Name: {}".format(player[3]))
        print()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    db.close()