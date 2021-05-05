import random
from datetime import datetime
from os import system

import mysql.connector
from cryptography.fernet import Fernet

system('cls')


class Database:
    def __init__(self, loadFrom='f', host="localhost", user="root", password="root", databaseName="testdb", filename="dbCreds.txt"):
        self._isConnected = False
        try:
            print("Connecting to Database...")
            self.__host = ""
            self.__user = ""
            self.__password = ""
            self.__databaseName = ""

            if (loadFrom == 'f'):
                print("Loading Credentials from {}".format(filename))
                credentials = self.__loadCredsFromFile(filename)
                self.__host = credentials[0]
                self.__user = credentials[1]
                self.__password = credentials[2]
                self.__databaseName = credentials[3]

            elif (loadFrom == 'p'):
                print("Loading Credentials from passed Argument")
                self.__host = host
                self.__user = user
                self.__password = password
                self.__databaseName = databaseName
            else:
                print("Invalid flag")

            self.db = mysql.connector.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.__databaseName
            )
            self.dbCursor = self.db.cursor()
            print("Connection to Database \"{}\" Established".format(
                self.__databaseName))
            self._isConnected = True

        except Exception as e:
            print(e)
            print("Error: Connection to Databse Not Established")
            self._isConnected = False

    def __loadCredsFromFile(self, filename):
        file = open(filename, 'r')
        key = str.encode(file.readline()[:-1])
        encryption_type = Fernet(key)
        credential = []

        credential.append(str(encryption_type.decrypt(
            str.encode(file.readline()[:-1])))[2:-1])
        credential.append(str(encryption_type.decrypt(
            str.encode(file.readline()[:-1])))[2:-1])
        credential.append(str(encryption_type.decrypt(
            str.encode(file.readline()[:-1])))[2:-1])
        credential.append(str(encryption_type.decrypt(
            str.encode(file.readline()[:-1])))[2:-1])

        file.close()
        return credential

    def saveCurrentCreds(self, filename="develop/dbCreds.txt"):
        if (self._isConnected):
            key = Fernet.generate_key()
            encryption_type = Fernet(key)

            file = open(filename, 'w')
            file.write(str(key)[2:-1] + "\n")

            # encrypted_message = encryption_type.encrypt(b"Hello World")
            file.write(str(encryption_type.encrypt(
                str.encode(self.__host)))[2:-1] + "\n")
            file.write(str(encryption_type.encrypt(
                str.encode(self.__user)))[2:-1] + "\n")
            file.write(str(encryption_type.encrypt(
                str.encode(self.__password)))[2:-1] + "\n")
            file.write(str(encryption_type.encrypt(
                str.encode(self.__databaseName)))[2:-1] + "\n")
            file.close()
            print("Credentials saved to {}".format(filename))

            return True
        else:
            print("Not Connected to Database")
            return False

    def query(self, command):
        if (self._isConnected):
            print("Query:", command)
            self.dbCursor.execute(command)
            data = self.dbCursor.fetchall()
            if (len(data) == 1):
                return data[0]
            else:
                return data
        else:
            print("Not Connected to Database")
            return False

    def commit(self):
        if (self._isConnected):
            self.db.commit()

            return True
        else:
            print("Not Connected to Database")
            return False

    def insert(self, table, cols, values):
        if (self._isConnected):
            colsString = "("
            for col in cols:
                colsString += col + ", "
            else:
                colsString = colsString[:-2] + ")"

            insert = "INSERT INTO {0} {1} VALUES {2}".format(
                table, colsString, tuple(values))
            self.query(insert)
            self.commit()

            return True
        else:
            print("Not Connected to Database")
            return False

    def update(self, table, cols, values, condition):
        if (self._isConnected):
            toChange = ""
            for i, col in enumerate(cols):
                if (type(values[i]) == str):
                    temp = "{} = \"{}\", ".format(col, values[i])
                else:
                    temp = "{} = {}, ".format(col, values[i])
                toChange += temp
            self.query("UPDATE {} SET {} WHERE {}".format(
                table, toChange[:-2], condition))
            self.commit()

            return True
        else:
            print("Not Connected to Database")
            return False
