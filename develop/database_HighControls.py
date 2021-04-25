from database import Database
from datetime import datetime
import random


class HighControlDB(Database):
    def createUsersTable(self):
        self.query("DROP TABLE IF EXISTS Users")
        self.query("CREATE TABLE Users (\
            u_id int PRIMARY KEY AUTO_INCREMENT NOT NULL,\
            c_num VARCHAR(16) NOT NULL,\
            passwd VARCHAR(20) NOT NULL,\
            inf_cov ENUM('T', 'F') NOT NULL,\
            f_name VARCHAR(30) NOT NULL,\
            m_name VARCHAR(30) NOT NULL,\
            l_name VARCHAR(30) NOT NULL,\
            age smallint NOT NULL,\
            gender ENUM('M','F','O') NOT NULL,\
            street VARCHAR(30) NOT NULL,\
            barangay VARCHAR(30) NOT NULL,\
            city VARCHAR(30) NOT NULL,\
            country VARCHAR(30) NOT NULL,\
            dt_add date NOT NULL,\
            dt_rem date NULL DEFAULT NULL)")
        print("Users Table Created")

    def createStoresTable(self):
        self.query("DROP TABLE IF EXISTS Stores")
        self.query("CREATE TABLE Stores (\
            s_id int PRIMARY KEY AUTO_INCREMENT NOT NULL,\
            store_num smallint NOT NULL,\
            floor smallint UNSIGNED NOT NULL,\
            wing ENUM('North','South','East', 'West') NOT NULL,\
            u_id int, FOREIGN KEY(u_id) REFERENCES Users(u_id),\
            name VARCHAR(50) NOT NULL,\
            contact_num int NOT NULL,\
            email VARCHAR(150) NOT NULL,\
            dt_add date NOT NULL,\
            dt_rem date NULL DEFAULT NULL)")
        print("Stores Table Created")

    def createCustHlthRec(self):
        self.query("DROP TABLE IF EXISTS Customers_Health_Record")
        self.query("CREATE TABLE Customers_Health_Record (\
            u_id int, FOREIGN KEY(u_id) REFERENCES Users(u_id),\
            s_id int, FOREIGN KEY(s_id) REFERENCES Stores(s_id),\
            dt_rec datetime NOT NULL)")
        print("Customers_Health_Record Table Created")

    def createHlthDecRec(self):
        self.query("DROP TABLE IF EXISTS Heath_Declaration_Record")
        self.query("CREATE TABLE Heath_Declaration_Record(\
            u_id int, FOREIGN KEY(u_id) REFERENCES Users(u_id),\
            temp DECIMAL(4, 2) NOT NULL,\
            fever ENUM('T', 'F') NOT NULL,\
            cough ENUM('T', 'F') NOT NULL,\
            headache ENUM('T', 'F') NOT NULL,\
            diff_breath  ENUM('T', 'F') NOT NULL,\
            bd_pains ENUM('T', 'F') NOT NULL,\
            s_throat ENUM('T', 'F') NOT NULL,\
            bd_weak ENUM('T', 'F') NOT NULL,\
            diarrhea ENUM('T', 'F') NOT NULL,\
            l_taste ENUM('T', 'F') NOT NULL,\
            hosp_vst ENUM('T', 'F') NOT NULL,\
            cont_covid ENUM('T', 'F') NOT NULL,\
            mem_cont_covid ENUM('T', 'F') NOT NULL,\
            dt_rec datetime NOT NULL)")
        print("Heath_Declaration_Record Table Created")

    def resetDatabase(self):
        self.query("DROP TABLE IF EXISTS Customers_Health_Record")
        self.query("DROP TABLE IF EXISTS Heath_Declaration_Record")
        self.query("DROP TABLE IF EXISTS Stores")
        self.query("DROP TABLE IF EXISTS Users")
        print("Tables Deleted")
        self.createUsersTable()
        self.createStoresTable()
        self.createCustHlthRec()
        self.createHlthDecRec()


# db = HighControlDB("localhost", "root", "root", "Development")
# db.createHlthDecRec()
# database.resetDatabase()


# i = 0
# while i < 20:
#     db.insert("customers_health_record ", ["u_id", "s_id", "dt_rec"], [
#               random.randint(1, 10), random.randint(1, 5), dt])
#     i += 1


def dencryptCredsFromFile(filename="credential.txt"):
    file = open(filename, 'r')
    key = str.encode(file.readline()[:-1])
    encryption_type = Fernet(key)

    creds = []
    creds.append(str(encryption_type.decrypt(
        str.encode(file.readline()[:-1])))[2:-1])
    creds.append(str(encryption_type.decrypt(
        str.encode(file.readline()[:-1])))[2:-1])
    creds.append(str(encryption_type.decrypt(
        str.encode(file.readline()[:-1])))[2:-1])
    creds.append(str(encryption_type.decrypt(
        str.encode(file.readline()[:-1])))[2:-1])

    file.close()
    return creds


# encryptCredsToFile("localhost", "root", "root",
#                    "testdb", "Test/credetials.txt")
print(dencryptCredsFromFile())
# b'e70uZngEEePhpiAy5EqaRcNbgsqYgTApzK0d5w_3XFU='
# db = HighControlDB(dencryptCredsFromFile())
