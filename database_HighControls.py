from database import Database, datetime, random


class HighControlDB(Database):
    def createUsersTable(self):
        if (self._isConnected):
            self.query("DROP TABLE IF EXISTS Users")
            self.query("CREATE TABLE Users (\
                u_id int PRIMARY KEY AUTO_INCREMENT NOT NULL,\
                c_num VARCHAR(16) NOT NULL,\
                passwd VARCHAR(20) NOT NULL,\
                type ENUM('C', 'A') NOT NULL,\
                inf_cov ENUM('Healthy', 'Primary Inf', 'First Contact', 'Second Contact', 'Third Contact') NOT NULL,\
                f_name VARCHAR(30) NOT NULL,\
                l_name VARCHAR(30) NOT NULL,\
                age smallint NOT NULL,\
                gender ENUM('Male','Female','Other') NOT NULL,\
                street VARCHAR(30) NOT NULL,\
                barangay VARCHAR(30) NOT NULL,\
                city VARCHAR(30) NOT NULL,\
                dt_add date NOT NULL,\
                dt_rem date NULL DEFAULT NULL)")
            print("Users Table Created")

            return True
        else:
            print("Not Connected to Database")
            return False

    def createStoresTable(self):
        if (self._isConnected):
            self.query("DROP TABLE IF EXISTS Stores")
            self.query("CREATE TABLE Stores (\
                s_id int PRIMARY KEY AUTO_INCREMENT NOT NULL,\
                store_num smallint NOT NULL,\
                floor smallint UNSIGNED NOT NULL,\
                wing ENUM('North','South','East', 'West') NOT NULL,\
                name VARCHAR(50) NOT NULL,\
                c_num VARCHAR(16) NOT NULL,\
                email VARCHAR(150) NOT NULL,\
                dt_add date NOT NULL,\
                dt_rem date NULL DEFAULT NULL)")
            print("Stores Table Created")

            return True
        else:
            print("Not Connected to Database")
            return False

    def createCustHlthRec(self):
        if (self._isConnected):
            self.query("DROP TABLE IF EXISTS Customers_Health_Record")
            self.query("CREATE TABLE Customers_Health_Record (\
                u_id int, FOREIGN KEY(u_id) REFERENCES Users(u_id),\
                s_id int, FOREIGN KEY(s_id) REFERENCES Stores(s_id),\
                dt_rec datetime NOT NULL)")
            print("Customers_Health_Record Table Created")

            return True
        else:
            print("Not Connected to Database")
            return False

    def createHlthDecRec(self):
        if (self._isConnected):
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

            return True
        else:
            print("Not Connected to Database")
            return False

    def resetDatabase(self):
        if (self._isConnected):
            self.query("DROP TABLE IF EXISTS Customers_Health_Record")
            self.query("DROP TABLE IF EXISTS Stores")
            # self.query("DROP TABLE IF EXISTS Heath_Declaration_Record")
            self.query("DROP TABLE IF EXISTS Users")
            print("Tables Deleted")
            self.createUsersTable()
            self.createStoresTable()
            self.createCustHlthRec()
            # self.createHlthDecRec()

            return True
        else:
            print("Not Connected to Database")
            return False
