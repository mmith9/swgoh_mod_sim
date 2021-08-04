import os
import mysql.connector
import processJobs
import simSettings
import json

mysqlDatabaseName="swgoh_sim_results"
mysqlUser=os.environ.get("mysql_user")
mysqlPassword=os.environ.get("mysql_password")

test=processJobs.JobsProcessing()

testHash=1242215931

select_testHash_query="select fingerprint, hash from sim_results where hash=" + str(testHash)
select_duplicates_query="select fingerprint, hash, count(fingerprint), count(hash) from sim_results GROUP BY hash HAVING count(fingerprint)>1 "
delete_duplicates_query="DELETE t1 FROM sim_results t1 INNER JOIN sim_results t2 WHERE t1.id < t2.id AND t1.hash=t2.hash AND t1.fingerprint=t2.fingerprint"

try:
    with mysql.connector.connect(
        host="localhost",
        user=mysqlUser,
        password=mysqlPassword,
        database=mysqlDatabaseName,
    ) as connection:

        cursor=connection.cursor()

        cursor.execute(select_duplicates_query)        
        duplicatedRows=cursor.fetchall()

        for dupeRow in duplicatedRows:
            dupeFingerprint=dupeRow[0]
            dupeHash=dupeRow[1]
            select_dupe_id_query="SELECT id, fingerprint, hash FROM sim_results WHERE fingerprint=" + str(dupeFingerprint) + " AND hash=" + str(dupeHash) + " ORDER BY id"
            print(select_dupe_id_query)
            cursor.execute(select_dupe_id_query)
            firstId=cursor.fetchall()[0][0]
            delete_dupes_query="DELETE FROM sim_results WHERE fingerprint=" + str(dupeFingerprint) + " AND hash=" + str(dupeHash) + " AND id > " + str(firstId)
            print(delete_dupes_query)
            cursor.execute(delete_dupes_query)
            connection.commit()
            






except mysql.connector.Error as e:
    print(e)       

