import mysql.connector
import os
import json
import time
import simSettings
from copy import deepcopy

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
    
        self.tempTables=[]

    def connect(self):
        try:
            connection=mysql.connector.connect(host= self.mysqlServer, user=self.mysqlUser, password=self.mysqlPassword, database=self.mysqlDatabaseName, allow_local_infile=True)
            cursor=connection.cursor()

        except mysql.connector.Error as e:
            print(e)
            input()
            
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

    def createTempTable(self, tableName):
        assert(False)
        if not self.dbConnection.is_connected():
            self.connect()
        
        query = "CREATE TEMPORARY TABLE " + tableName + "("
        query+= """
                id INT AUTO_INCREMENT PRIMARY KEY,
                settings_fingerprint CHAR(100),
                settings_hash BIGINT,
                score_high FLOAT,
                score_mid FLOAT,
                score_low FLOAT,
                score_Elisa FLOAT,
                score_ElisaM14 FLOAT,
                leftover_mod_energy FLOAT,
                leftover_credits FLOAT,
                leftover_microprocessor FLOAT,
                roll_avg_energy_cost FLOAT,
                total_cap_amp_bought FLOAT,
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

        self.cursor.execute(query)
        return tableName

    def getTableNameForSim_old(self, baseFingerprint, baseHash, iterateList, baseSettings):
        assert(False)
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
                    score_high FLOAT,
                    score_mid FLOAT,
                    score_low FLOAT,
                    score_Elisa FLOAT,
                    score_ElisaM14 FLOAT,
                    leftover_mod_energy FLOAT,
                    leftover_credits FLOAT,
                    leftover_microprocessor FLOAT,
                    roll_avg_energy_cost FLOAT,
                    total_cap_amp_bought FLOAT,
                    settings_iterated_diff TEXT,
                    all_results TEXT,
                    INDEX idx_fingerprint (settings_fingerprint),
                    INDEX idx_hash (settings_hash),
                    INDEX idx_score_high (score_high),
                    INDEX idx_score_mid (score_mid),
                    INDEX idx_score_low (score_low),
                    INDEX idx_score_Elisa (score_Elisa),
                    INDEX idx_score_ElisaM14 (score_ElisaM14),
                    UNIQUE KEY (settings_fingerprint, settings_hash)
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
                    settings_fingerprint_hash BIGINT,
                    settings_hash BIGINT,
                    score_high FLOAT,
                    score_mid FLOAT,
                    score_low FLOAT,
                    score_Elisa FLOAT,
                    score_ElisaM14 FLOAT,
                    leftover_mod_energy FLOAT,
                    leftover_credits FLOAT,
                    leftover_microprocessor FLOAT,
                    roll_avg_energy_cost FLOAT,
                    roll_avg_credit_cost FLOAT,
                    total_cap_amp_bought FLOAT,
                    u_e TINYINT,
                    u_d TINYINT,
                    
                    mi_e TINYINT,
                    mi_d TINYINT,

                    ms_1d TINYINT,
                    ms_2d TINYINT,

                    ms_1c TINYINT,
                    ms_2c TINYINT,
                    ms_3c TINYINT,

                    ms_1b TINYINT,
                    ms_2b TINYINT,
                    ms_3b TINYINT,
                    ms_4b TINYINT,

                    ms_1a TINYINT,
                    ms_2a TINYINT,
                    ms_3a TINYINT,
                    ms_4a TINYINT,

                    ms_16e TINYINT,
                    ms_26e TINYINT,
                    ms_36e TINYINT,
                    ms_46e TINYINT,

                    ms_16d TINYINT,
                    ms_26d TINYINT,
                    ms_36d TINYINT,
                    ms_46d TINYINT,

                    ms_1c6 TINYINT,
                    ms_26c TINYINT,
                    ms_36c TINYINT,
                    ms_46c TINYINT,

                    ms_16b TINYINT,
                    ms_26b TINYINT,
                    ms_36b TINYINT,
                    ms_46b TINYINT,

                    
                    INDEX idx_score_high (score_high),
                    INDEX idx_score_mid (score_mid),
                    INDEX idx_score_low (score_low),
                    INDEX idx_score_Elisa (score_Elisa),
                    INDEX idx_score_ElisaM14 (score_ElisaM14),
                    UNIQUE KEY (settings_fingerprint_hash, settings_hash)
                    )
            """
                    #                    id INT AUTO_INCREMENT PRIMARY KEY,

                    # INDEX idx_fingerprint (settings_fingerprint),
                    # INDEX idx_hash (settings_hash),
                    # INDEX idx_score_high (score_high),
                    # INDEX idx_score_mid (score_mid),
                    # INDEX idx_score_low (score_low),
                    # INDEX idx_score_Elisa (score_Elisa),
                    # INDEX idx_score_ElisaM14 (score_ElisaM14),
                    # UNIQUE KEY (settings_fingerprint, settings_hash)


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
            
    def feedInBulkBatchToDB(self, batchJob):
        header=batchJob["header"]
        simListForDb=batchJob["resultListForDb"]

        baseSettings=header["settingsSnapshot"]
        baseHash=header["snapshotHash"]
        baseFingerprint=header["snapshotFingerprint"]
        iterateList=header["iterateList"]

        tableName=self.getTableNameForSim(baseFingerprint, baseHash, iterateList, baseSettings)

        ## prepared by processJobs
        ## [fingerprint, hash, high, mid, low, elisa, elisam14, energy, credits, microproc, avg energy, cap_amp, settings_diff, all_results]

        insert_sim_query="INSERT IGNORE INTO " +tableName +" ("
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
            roll_avg_credit_cost,
            total_cap_amp_bought, 

            u_e, 
            u_d,
            
            mi_e, 
            mi_d,

            ms_1d,
            ms_2d,

            ms_1c,
            ms_2c,
            ms_3c,

            ms_1b,
            ms_2b,
            ms_3b,
            ms_4b,

            ms_1a,
            ms_2a,
            ms_3a,
            ms_4a,

            ms_16e,
            ms_26e,
            ms_36e,
            ms_46e,

            ms_16d,
            ms_26d,
            ms_36d,
            ms_46d,

            ms_1c6,
            ms_26c,
            ms_36c,
            ms_46c,

            ms_16b,
            ms_26b,
            ms_36b,
            ms_46b

            )
            VALUES (
            """

        commaCount=insert_sim_query.count(",")
        for x in range(0,commaCount):
            insert_sim_query+= "%s, "
        insert_sim_query+= "%s )"


        if self.testlevel>99:
            print(insert_sim_query)

        rowsToInsert=len(simListForDb)
        packetNum=0
        rowsPerPacket=50000
        
        start_time = time.time()
        print("inserting ", rowsToInsert, "rows")
        while packetNum*rowsPerPacket <= rowsToInsert:
            self.cursor.executemany(insert_sim_query, simListForDb[packetNum*rowsPerPacket:(packetNum+1)*rowsPerPacket])
            self.dbConnection.commit()
            packetNum+=1 
            print(".", end="")
        print()
        print(time.time() - start_time, "seconds")

        query="SELECT COUNT(*) FROM "+tableName
        self.cursor.execute(query)
        row=self.cursor.fetchone()
        self.cursor.fetchall()
        print(tableName," rows total", row[0])

        return tableName
    
    
    def feedCsvToDb(self, tableName, fileName):
        
        ## prepared by processJobs
        ## [fingerprint hash, hash, high, mid, low, elisa, elisam14, energy, credits, microproc, avg energy, cap_amp, settings_diff, all_results]

        query="LOAD DATA LOCAL INFILE '" +fileName +"' INTO TABLE " +tableName +" fields terminated by ','"


        if self.testlevel>99:
            print(query)

        packetNum=0
        rowsPerPacket=50000
        
        start_time = time.time()
        print("inserting ")

        self.cursor.execute(query)
        self.dbConnection.commit()
        
        print(time.time() - start_time, "seconds")

        query="SELECT COUNT(*) FROM "+tableName
        self.cursor.execute(query)
        row=self.cursor.fetchone()
        self.cursor.fetchall()
        print(tableName," rows total", row[0])

        return tableName
    
    

    
    def feedInBulkBatchToDB__(self, batchJob):
        header=batchJob["header"]
        simListForDb=batchJob["resultListForDb"]

        baseSettings=header["settingsSnapshot"]
        baseHash=header["snapshotHash"]
        baseFingerprint=header["snapshotFingerprint"]
        iterateList=header["iterateList"]
        
        tableName="temp_"+str(baseHash)
        if tableName not in self.tempTables:
            self.createTempTable(tableName)
            self.tempTables.append(tableName)

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

        rowsToInsert=len(simListForDb)
        packetNum=0
        rowsPerPacket=2000
        
        start_time = time.process_time()
        print("inserting ", rowsToInsert, "rows")
        while packetNum*rowsPerPacket <= rowsToInsert:
            self.cursor.executemany(insert_sim_query, simListForDb[packetNum*rowsPerPacket:(packetNum+1)*rowsPerPacket])
            self.dbConnection.commit()
            packetNum+=1 
            print(".", end="")
        print()
        print(time.process_time() - start_time, "seconds")

        query="SELECT COUNT(*) FROM "+tableName
        self.cursor.execute(query)
        row=self.cursor.fetchone()
        self.cursor.fetchall()
        print("temp rows total", row[0])

        return tableName


    def loadTopResultsFromDb(self, hash,  maxTopResults=100):
        if not self.dbConnection.is_connected():
            self.connect()

 
        query="select base_fingerprint, base_hash, iterate_list, base_settings, sims_table_name FROM swgoh_sims WHERE base_hash='" +str(hash) +"'"
        self.cursor.execute(query)
        row=self.cursor.fetchone()
        self.cursor.fetchall

        baseFingerpring=row[0]
        baseHash=row[1]
        iterateList=json.loads(row[2])
        baseSettings=json.loads(row[3])
        simsTableName=row[4]

        results5={}
   

        for valueFunc in ["high", "mid", "low", "Elisa", "ElisaM14"]:
            select_top_scores_query="SELECT settings_fingerprint, settings_hash, settings_iterated_diff, all_results, score_"+valueFunc+", roll_avg_energy_cost FROM sim_results_for_"+str(hash)
            select_top_scores_query+=" ORDER BY score_"+valueFunc+" DESC LIMIT "+str(maxTopResults)
        
            self.cursor.execute(select_top_scores_query)
            rows=self.cursor.fetchall()
            
            results=[]
            
            for row in rows:
                jobNum=row[0] +"x" +str(row[1])

                jobSettings=deepcopy(baseSettings)
                simSettings.SimSettings.mergeSettings(jobSettings, json.loads(row[2]))

                jobScores=json.loads(row[3])
                jobScores["budgetBreakdown"]["avgRollModEnergyCost"]= row[5]

                results.append({"job":jobNum, "settings":jobSettings, "scores": jobScores})
              

            results5[valueFunc]=results

        return results5 
