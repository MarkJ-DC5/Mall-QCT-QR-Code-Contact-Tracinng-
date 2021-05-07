import random
from datetime import datetime
from os import system

import mysql.connector
from cryptography.fernet import Fernet

system('cls')


class Database:
    def __init__(self, loadFrom='f', host="localhost", user="root", password="root", databaseName="testdb", fileName="dbCreds.txt"):
        self._isConnected = False
        self._fileName = fileName
        print("Connecting to Database...")
        self.__host = ""
        self.__user = ""
        self.__password = ""
        self.__databaseName = ""

        if (loadFrom == 'f'):
            print("Loading Credentials from {}".format(self._fileName))
            self.__loadCredsFromFile(self._fileName)

        elif (loadFrom == 'p'):
            print("Loading Credentials from passed Argument")
            self.__host = host
            self.__user = user
            self.__password = password
            self.__databaseName = databaseName
        else:
            raise Exception("Invalid Value for \"loadfrom\"")

        try:
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
            self._isConnected = False
            print(e)
            print("Connection to Databse Not Established")

    def __loadCredsFromFile(self, filename):
        try:
            file = open(filename, 'r')
            key = str.encode(file.readline()[:-1])
            encryption_type = Fernet(key)

            self.__host = str(encryption_type.decrypt(
                str.encode(file.readline()[:-1])))[2:-1]
            self.__user = str(encryption_type.decrypt(
                str.encode(file.readline()[:-1])))[2:-1]
            self.__password = str(encryption_type.decrypt(
                str.encode(file.readline()[:-1])))[2:-1]
            self.__databaseName = str(encryption_type.decrypt(
                str.encode(file.readline()[:-1])))[2:-1]
            file.close()
        except Exception as e:
            print(e)
            raise Exception("Error Reading File")

    def saveCurrentCreds(self, filename="develop/dbCreds.txt"):
        try:
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
                raise Exception("Not Connected to Database")
        except Exception as e:
            print(e)
            return None

    def query(self, command):
        if (self._isConnected):
            # print("Query:", command)
            self.dbCursor.execute(command)
            data = self.dbCursor.fetchall()
            if (len(data) == 1):
                return data[0]
            else:
                return data
        else:
            raise Exception("Not Connected to Database")

    def commit(self):
        if (self._isConnected):
            self.db.commit()
        else:
            raise Exception("Not Connected to Database")

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
        else:
            raise Exception("Not Connected to Database")

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
            raise Exception("Not Connected to Database")

    def convertOutputToArray(self, output):
        outputLen = len(output)
        if(outputLen == 1):
            if(type(output) == list):
                return list(output[0])
            elif(type(output) == tuple):
                return list(output)
        elif(outputLen > 1):
            for i, tup in enumerate(output):
                output[i] = tup[0]
            return output
        else:
            return []
