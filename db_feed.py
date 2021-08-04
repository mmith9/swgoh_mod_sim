import os
import mysql.connector
import processJobs
import simSettings
import json

inputPrefix="EVAL06"
maxFiles=30
fileNum=0


mysqlDatabaseName="swgoh_sim_results"
mysqlUser=os.environ.get("mysql_user")
mysqlPassword=os.environ.get("mysql_password")

insert_sim_results_query = """
INSERT INTO sim_results
(fingerprint, hash, score_high, score_mid, score_low, score_Elisa, score_ElisaM14, settings, scores)
VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s )
"""

while fileNum<maxFiles:
    inputFilename="iteration_results/"+inputPrefix + "x" + str(fileNum) + ".json"
    fileNum+= 1
    if os.path.isfile(inputFilename):
        print()
        print("Reading file ", inputFilename)
        with open(inputFilename, "r") as fp:
            results=json.load(fp)

        listToInsert=[]
        for job in results:
            jobNum=job["job"]
            jobSettings=job["settings"]
            jobSettingsJson=json.dumps(jobSettings)
            jobScores=job["scores"]
            jobScoresJson=json.dumps(jobScores)

            jobScoreHigh=jobScores["speedValue"]["high"]
            jobScoreMid=jobScores["speedValue"]["mid"]
            jobScoreLow=jobScores["speedValue"]["low"]
            jobScoreElisa=jobScores["speedValue"]["Elisa"]
            jobScoreElisaM14=jobScores["speedValue"]["ElisaM14"]

            jobFingerprint=simSettings.SimSettings.settingsFingerprintOfGetAll(jobSettings)
            jobHash=simSettings.SimSettings.settingsHashOfGetAll(jobSettings)
            listToInsert.append( (jobFingerprint, jobHash, jobScoreHigh, jobScoreMid, jobScoreLow, jobScoreElisa, jobScoreElisaM14, jobSettingsJson, jobScoresJson) )
        print("inserting", len(listToInsert), "values into table")
        try:
            with mysql.connector.connect(
                host="localhost",
                user=mysqlUser,
                password=mysqlPassword,
                database=mysqlDatabaseName,
            ) as connection:
                cursor=connection.cursor()
                
                for item in listToInsert:
                    select_check_exist_query="SELECT fingerprint, hash FROM sim_results WHERE fingerprint=" +str(item[0]) +" AND hash=" +str(item[1])
                    cursor.execute(select_check_exist_query)
                    allreadyExist=cursor.fetchall()
                    if allreadyExist:     #list not empty
                        print("-" +str(item[1]), "", end="")
                    else:
                        print("+" +str(item[1]), "", end="")
                        cursor.executemany(insert_sim_results_query, [item])
                        connection.commit()
                     
        except mysql.connector.Error as e:
            print(e)
