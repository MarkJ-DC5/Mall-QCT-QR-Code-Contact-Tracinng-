from datetime import datetime
from os import system

import cv2 as cv
import mysql.connector
import qrcode
from PIL import Image

system('cls')


class Database:
    def __init__(self, p_host="localhost", p_user="root", p_password="root", p_databaseName=""):
        try:
            print("Connecting to Database...")

            if(p_host == "remotemysql.com"):
                p_databaseName = p_user

            self.db = mysql.connector.connect(
                host=p_host,
                user=p_user,
                password=p_password,
                database=p_databaseName
            )
            self.dbCursor = self.db.cursor()
            # self.dbCursor.execute("CREATE DATABASE testDB")
            print("Connection to Databse Established")

        except:
            print("Error: Connection to Databse Not Established")

    def query(self, command):
        self.dbCursor.execute(command)
        return self.dbCursor.fetchall()

    def commit(self):
        self.db.commit()

    def insert(self, table, cols, values):
        colsString = "("
        for col in cols:
            colsString += col + ", "
        else:
            colsString = colsString[:-2] + ")"

        insert = "INSERT INTO {0} {1} VALUES {2}".format(
            table, colsString, tuple(values))
        self.query(insert)
        self.commit()

    def __del__(self):
        print("Object Cleared")
