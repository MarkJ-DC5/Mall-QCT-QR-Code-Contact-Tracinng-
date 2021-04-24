from database import Database
from datetime import datetime, timedelta
import random


class HighControlDB(Database):
    def createUsersTable(self):
        self.query("DROP TABLE IF EXISTS Users")
        self.query("CREATE TABLE Users (\
            u_id int PRIMARY KEY AUTO_INCREMENT NOT NULL,\
            c_num VARCHAR(16) NOT NULL,\
            passwd VARCHAR(20) NOT NULL)")
        print("Users Table Created")

    def createStoresTable(self):
        self.query("DROP TABLE IF EXISTS Stores")
        self.query("CREATE TABLE Stores (\
            s_id int PRIMARY KEY AUTO_INCREMENT NOT NULL,\
            store_num smallint NOT NULL,\
            floor smallint UNSIGNED NOT NULL)")
        print("Stores Table Created")

    def createCustHlthRec(self):
        self.query("DROP TABLE IF EXISTS Customers_Health_Record")
        self.query("CREATE TABLE Customers_Health_Record (\
            u_id int,\
            s_id int,\
            dt_rec datetime NOT NULL)")
        print("Customers_Health_Record Table Created")

    def resetDatabase(self):
        self.query("DROP TABLE IF EXISTS Customers_Health_Record")
        self.query("DROP TABLE IF EXISTS Stores")
        self.query("DROP TABLE IF EXISTS Users")
        print("Tables Deleted")
        self.createUsersTable()
        self.createStoresTable()
        self.createCustHlthRec()


db = HighControlDB("localhost", "root", "root", "testDB")
# db.resetDatabase()
#dt = datetime.now().replace(microsecond=0)
# i = 0
# while i < 40:
#     db.insert("customers_health_record ", ["u_id", "s_id", "dt_rec"], [
#               random.randint(1, 40), random.randint(1, 10), dt])
#     i += 1


def incrementHR(dtStr="2021-04-25 00:41:00"):
    dtObj = datetime.strptime(dtStr, '%Y-%m-%d %H:%M:%S') + timedelta(hours=1)
    return str(dtObj)
print(incrementHR())

# dt_rec BETWEEN "2021-04-25 00:41:00" AND "2021-04-25 01:41:00"
