
import processJobs
from datetime import datetime



if __name__ == '__main__':

    inputFile="FILTER06"
    fileCount=30
    
    start_time = datetime.now()
    test=processJobs.JobsProcessing()
        
    print("reading")
    start_time = datetime.now()
    test.readResults(filesTotal=fileCount, inputPrefix=inputFile)
    end_time = datetime.now()
    
    print('Duration: {}'.format(end_time - start_time))
    
    #test2=test.filterByX(filter="uncoverStatsLimit", value=2)
    #test=test.filterByX(filter="microprocessor", value=3)
        
    print("sorting")
    start_time = datetime.now()
    test.sortJobsBy("high")
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    
    input("press enter to display, ")

    test.displayResultsRelevantSettings(50)

    test.sortJobsBy("mid")
    input("press enter to display, sort by mid")
    for x in range(0,20):
        print()
    test.displayResultsRelevantSettings(50)

    test.sortJobsBy("low")
    input("press enter to display, sort by low")
    for x in range(0,20):
        print()
    test.displayResultsRelevantSettings(50)

    test.sortJobsBy("Elisa")
    input("press enter to display, sort by Elisa")
    for x in range(0,20):
        print()
    test.displayResultsRelevantSettings(50)

    test.sortJobsBy("ElisaM14")
    input("press enter to display, sort by ElisaM14")
    for x in range(0,20):
        print()
    test.displayResultsRelevantSettings(50)
