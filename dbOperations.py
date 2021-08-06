import mysql.connector
import os
import json


class DbOperations():
    def __init__(self) -> None:

        self.testlevel=99

        self.mysqlServer="localhost"
        self.mysqlDatabaseName="swgoh_sim_results"
        self.mysqlMainTable="swgoh_sims"
        self.mysqlUser=os.environ.get("mysql_user")
        self.mysqlPassword=os.environ.get("mysql_password")
        
        self.cursor :mysql.connector.connection.MySQLCursor
        self.dbConnection :mysql.connector.CMySQLConnection
    
    def connect(self):
        try:
            connection=mysql.connector.connect(host= self.mysqlServer, user=self.mysqlUser, password=self.mysqlPassword, database=self.mysqlDatabaseName)
            cursor=connection.cursor()

        except mysql.connector.Error as e:
            print(e)
        
        self.dbConnection= connection
        self.cursor=cursor
        return cursor

    def createMainTable(self):
        if not self.dbConnection.is_connected():
            self.connect()
        
        ## check if table allready exists
        query="SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '"+self.mysqlMainTable+"'"

        #print(query)
        self.cursor.execute(query)
        rows=self.cursor.fetchall()
        count=rows[0][0]
        if count>0 :
            print("Main table allready exists")
        else:
            query = "CREATE TABLE " + self.mysqlMainTable + "("
            query+= """
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    base_fingerprint CHAR(100), 
                    base_hash BIGINT,
                    iterate_list TEXT,
                    base_settings TEXT,
                    sims_table_name CHAR(100),
                    INDEX idx_fingerprint (base_fingerprint),
                    INDEX idx_hash (base_hash)
                    )
                """
            self.cursor.execute(query)

    def getTableNameForSim(self, baseFingerprint, baseHash, iterateList, baseSettings):
        if not self.dbConnection.is_connected():
            self.connect()

        ## check if table allready exists
        query="SELECT sims_table_name FROM " + self.mysqlMainTable + " WHERE base_hash=" +str(baseHash) +" and base_fingerprint='" +baseFingerprint +"'"
        if self.testlevel>99:
            print(query)
        self.cursor.execute(query)
        rows=self.cursor.fetchall()
        if self.testlevel>99:
            print(rows)
        if rows :
            return rows[0][0]
        else:
            # have to create table and insert it into list
            tableName="sim_results_for_" +str(baseHash)

            query="SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '" +tableName+ "'"
            self.cursor.execute(query)
            rows=self.cursor.fetchall()
            if rows[0][0] > 0:
                print("But table itself allready exists!!!! cannot add :", tableName)
                assert(False)

            query = "CREATE TABLE " + tableName + "("
            query+= """
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    settings_fingerprint CHAR(100),
                    settings_hash BIGINT,
                    score_high DOUBLE,
                    score_mid DOUBLE,
                    score_low DOUBLE,
                    score_Elisa DOUBLE,
                    score_ElisaM14 DOUBLE,
                    leftover_mod_energy DOUBLE,
                    leftover_credits DOUBLE,
                    leftover_microprocessor DOUBLE,
                    roll_avg_energy_cost DOUBLE,
                    total_cap_amp_bought DOUBLE,
                    settings_iterated_diff TEXT,
                    all_results TEXT,
                    INDEX idx_fingerprint (settings_fingerprint),
                    INDEX idx_hash (settings_hash),
                    INDEX idx_score_high (score_high),
                    INDEX idx_score_mid (score_mid),
                    INDEX idx_score_low (score_low),
                    INDEX idx_score_Elisa (score_Elisa),
                    INDEX idx_score_ElisaM14 (score_ElisaM14)
                    )
            """
            if self.testlevel>99:
                print(query)
            self.cursor.execute(query)

            query="INSERT INTO " +self.mysqlMainTable +"( base_fingerprint, base_hash, iterate_list, base_settings, sims_table_name ) VALUES (%s, %s, %s, %s, %s)"
            if self.testlevel>99:
                print(query)
            self.cursor.execute(query, (baseFingerprint, baseHash, json.dumps(iterateList), json.dumps(baseSettings), tableName))
            self.dbConnection.commit()
            
            return tableName

    def feedBatchToDB(self, batchJob):
        header=batchJob["header"]
        simListForDb=batchJob["resultListForDb"]

        baseSettings=header["settingsSnapshot"]
        baseHash=header["snapshotHash"]
        baseFingerprint=header["snapshotFingerprint"]
        iterateList=header["iterateList"]

        tableName=self.getTableNameForSim(baseFingerprint, baseHash, iterateList, baseSettings)

        ## prepared by processJobs
        ## [fingerprint, hash, high, mid, low, elisa, elisam14, energy, credits, microproc, avg energy, cap_amp, settings_diff, all_results]

        insert_sim_query="INSERT INTO " +tableName +" ("
        insert_sim_query+= """
            settings_fingerprint,
            settings_hash,
            score_high ,
            score_mid ,
            score_low ,
            score_Elisa,
            score_ElisaM14,
            leftover_mod_energy,
            leftover_credits,
            leftover_microprocessor,
            roll_avg_energy_cost,
            total_cap_amp_bought, 
            settings_iterated_diff,
            all_results )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
            """
        if self.testlevel>99:
            print(insert_sim_query)

        for sim in simListForDb:
            currFingerprint=sim[0]
            currHash=sim[1]
            query="SELECT COUNT(*) from " +tableName +" WHERE settings_fingerprint='" +currFingerprint +"' AND settings_hash=" +str(currHash)
            if self.testlevel>99:
                print(query)
            self.cursor.execute(query)
            rows=self.cursor.fetchall()
            if rows[0][0] > 0:
                if self.testlevel>99:
                    print("Allready in db:", currHash)
                pass    ## allready exists in database
            else:
                if self.testlevel>99:
                    print("Inserting to db:", currHash)
                
                self.cursor.execute(insert_sim_query, sim)
                self.dbConnection.commit()
            
