
import processJobs_heat
import dbOperations
from datetime import datetime



if __name__ == '__main__':

    # inputFile="FILTER06"
    # fileCount=30
    
    start_time = datetime.now()
    
    processJobs=processJobs_heat.JobsProcessing()
    test=dbOperations.DbOperations()
    test.connect()

    #hash=81002551
    #hash=2545693919
    hash=3766640408
       
    print("reading")
    start_time = datetime.now()
    result5=test.loadTopResultsFromDb(hash, maxTopResults=100)
    end_time = datetime.now()
    
    print('Duration: {}'.format(end_time - start_time))
    
    for valueFunc in ["high", "mid", "low", "Elisa", "ElisaM14"]:

        processJobs.displayResultsRelevantSettings(result5[valueFunc], 10)
        
        input()

        for x in range(0,20):
            print()

