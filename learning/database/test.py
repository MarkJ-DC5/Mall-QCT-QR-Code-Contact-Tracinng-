import mysql.connector
from datetime import datetime

# connection
db = mysql.connector.connect(
    host="localhost",
    user='root',
    password='root',
    database='Development'
)

mycursor = db.cursor()
mycursor.execute("SHOW DATABASES")
print(mycursor)
