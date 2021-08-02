
import processJobs
from datetime import datetime



if __name__ == '__main__':

    inputFile="EVAL06"
    outputFile="FILTER06"
    fileCut=5000
    fileCount=30
    

    start_time = datetime.now()
    test=processJobs.JobsProcessing()

    test.filterOutIrrelevantCrap(inputPrefix=inputFile, outputPrefix=outputFile)
