import dbOperations
import os
import json
import processJobs_heat

aDatabase=dbOperations.DbOperations()

aDatabase.connect()

aDatabase.createMainTable()

inputPrefix="HEAT09"


fileCount=300


testlevel=1

for filenum in range(0, fileCount):
    if testlevel>0:
        print("file ", filenum +1 , "out of", fileCount)
    inputFilename="iteration_results/"+inputPrefix + "x" + str(filenum) + ".json"
    
    if testlevel>0:
        print("trying", inputFilename)

    if os.path.isfile(inputFilename):
        with open(inputFilename, "r") as fp:
            results=json.load(fp)
        
        aList= processJobs_heat.JobsProcessing.prepareResultListForDb(results, trim=1)
        aDatabase.feedInBulkBatchToDB(aList)
        



