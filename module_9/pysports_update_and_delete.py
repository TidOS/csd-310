#!/usr/bin/env python3
# insert a row, update it, and delete it
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

def printPlayers():
    #run a query that joins the player table (left) with the team table (right) 
    #where the team_id matches from each table.  We want the player id, first name,
    #last name, and team name
    cursor.execute("SELECT player_id, first_name, last_name, team_name FROM player "+
    "INNER JOIN team ON player.team_id = team.team_id")
    # players is an array of objects with the fields we selected
    players = cursor.fetchall()
    print("-- DISPLAYING PLAYER RECORDS --")
    for player in players:
        print("Player ID: {}".format(player[0]))
        print("First Name: {}".format(player[1]))
        print("Last Name: {}".format(player[2]))
        print("Team Name: {}".format(player[3]))
        print()

try:
    db = mysql.connector.connect(**config)
    # start
    cursor = db.cursor()
    #insert a new player on team gandalf (team_id = 1 for gandalf)
    cursor.execute("INSERT INTO player (first_name, last_name, team_id) VALUES('Smeagol', 'Shire Folk', 1)")
    print("-- ADDED A PLAYER --")
    printPlayers()

    #SQL query to change team_id to 2, name to Gollum Ring Stealer of the player we just added
    cursor.execute("UPDATE player SET team_id = 2, first_name = 'Gollum', last_name = 'Ring Stealer' WHERE first_name = 'Smeagol'")
    print("-- UPDATED A PLAYER --")
    printPlayers()

    #SQL query to delete the Gollum player
    cursor.execute("DELETE from player WHERE first_name = 'Gollum'")
    print("-- DELETED THE PLAYER --")
    printPlayers()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    db.close()