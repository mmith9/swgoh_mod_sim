import os
import mysql.connector


assert(False)

mysqlDatabaseName="swgoh_sim_results"
mysqlUser=os.environ.get("mysql_user")
mysqlPassword=os.environ.get("mysql_password")

print(mysqlUser, mysqlPassword)

create_db_query = "CREATE DATABASE swgoh_sim_results"
        
create_sim_results_db_query = """
CREATE TABLE sim_results(
    id INT AUTO_INCREMENT PRIMARY KEY,
    fingerprint CHAR(60),
    hash BIGINT,
    score_high DOUBLE,
    score_mid DOUBLE,
    score_low DOUBLE,
    score_Elisa DOUBLE,
    score_ElisaM14 DOUBLE,
    settings TEXT,
    scores TEXT
)
"""

describe_query="DESCRIBE sim_results"

try:
    with mysql.connector.connect(
        host="localhost",
        user=mysqlUser,
        password=mysqlPassword,
        database=mysqlDatabaseName,
    ) as connection:
        cursor=connection.cursor()
        #cursor.execute(create_db_query)
        #connection.commit()
        cursor.execute(create_sim_results_db_query)
        connection.commit()

        cursor.execute(describe_query)
        results=cursor.fetchall()
        for row in results:
            print(row)


except Error as e:
    print(e)


