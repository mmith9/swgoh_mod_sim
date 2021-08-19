from re import A
import dbOperations
import os
import json
import processJobs_heat
from simSettings import SimSettings

aDatabase=dbOperations.DbOperations()

aDatabase.connect()

aDatabase.createMainTable()

inputPrefix="HEAT11"




fileCount=20


testlevel=1

for filenum in range(0, fileCount):
    if testlevel>0:
        print("file ", filenum +1 , "out of", fileCount)
    inputFilename="iteration_results/"+ inputPrefix + "x" + SimSettings.padNameWithZeros(str(filenum),6) + ".json"
    
    if testlevel>0:
        print("trying", inputFilename)

    if os.path.isfile(inputFilename):
        with open(inputFilename, "r") as fp:
            results=json.load(fp)
        

        
        aList= processJobs_heat.JobsProcessing.prepareResultListForDb(results, trim=1)

        # for x in aList["resultListForDb"]:
        #     print(x)
        #     input()



        #dump data to csv

        with open("iteration_results/csv.txt", "w") as fp:
            results=aList["resultListForDb"]
            for result in results:
                row=str(result[0])
                for x in range(1,len(result)):
                    row+=","+str(result[x])
                row+="\n"
                fp.write(row)


        batchJob=aList
        header=batchJob["header"]
        simListForDb=batchJob["resultListForDb"]

        baseSettings=header["settingsSnapshot"]
        baseHash=header["snapshotHash"]
        baseFingerprint=header["snapshotFingerprint"]
        iterateList=header["iterateList"]

        tableName=aDatabase.getTableNameForSim(baseFingerprint, baseHash, iterateList, baseSettings)

        aDatabase.feedCsvToDb(tableName, "iteration_results/csv.txt")


