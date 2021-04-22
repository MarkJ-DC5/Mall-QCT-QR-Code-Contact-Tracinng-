import mysql.connector
from datetime import datetime

# connection
db = mysql.connector.connect(
    host="remotemysql.com",
    user='u7uaPXYngg',
    password='INpaGTo80o',
    database="u7uaPXYngg"
)

mycursor = db.cursor()
showTable = "Show Table"

deleteTableP = "DROP TABLE Person"
createTableP = "CREATE TABLE Person (person_ID int PRIMARY KEY NOT NULL AUTO_INCREMENT , name VARCHAR(50) NOT NULL, age smallint UNSIGNED NOT NULL, gender ENUM('M','F','O') NOT NULL, added datetime NOT NULL)"
describeTableP = "DESCRIBE Person"

name = "Joseph"
age = 19
gender = 'M'
insertTableP = "INSERT INTO Person (name, age, gender, added) VALUES (%s, %s, %s, %s)", (
    name, age, gender, datetime.now())
# db.commit()

# * means select all column
selectTableP = "SELECT name FROM Person WHERE gender = 'M' ORDER BY person_ID DESC"
getRecentID = "SELECT LASt_INSERT_ID"

deleteTableS = "DROP TABLE Quiz_Attempt"
createTableS = "CREATE TABLE Quiz_Attempt (id int PRIMARY KEY AUTO_INCREMENT, userID int, FOREIGN KEY(userID) REFERENCES Person(person_ID), score int DEFAULT 0)"

# mycursor.execute(deleteTableS)
# mycursor.execute(createTableS)


# for x in mycursor:
#     print(x)

# remote connection
# db = mysql.connector.connect(
#     host="remotemysql.com",
#     user='a8tyrwZpQc',
#     password='H9G5r0oL3X',
#     database="a8tyrwZpQc"
# )

# cursor object
#mycursor = mydb.cursor()

# mycursor.execute("DROP TABLE customers")

# mycursor.execute(
#     "CREATE TABLE customers (fname text, lname text, email text)")
# mycursor.execute(
#     "INSERT INTO customers VALUES('John', 'Elder', 'john@codemy.com')")

# conn = sqlite3.connect('chinook/chinook.db')
# cursor = conn.execute('select lastname, firstname from employees')

# for row in cursor:
#     print('Lastname:' + row[0])
#     print('Firstname:' + row[1] + '\n')
