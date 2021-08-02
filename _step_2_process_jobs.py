
import processJobs
from datetime import datetime



if __name__ == '__main__':

    inFile="ITER06x"
    outFile="EVAL06x"
    fileCut=5000
    fileCount=30
    

    start_time = datetime.now()
    test=processJobs.JobsProcessing()
    print("processing files")
    test.processFiles(filesTotal=fileCount, multiproc=True, inputPrefix=inFile, outputPrefix=outFile, fileCut=fileCut)
    print("processing done")
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    
    
    print("reading")
    start_time = datetime.now()
    test.readResults(filesTotal=fileCount, inputPrefix=outFile, fileCut=fileCut)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    
    print("sorting")
    start_time = datetime.now()
    test.sortJobsBy("low")
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    
    input("press enter to display")
    test.displayResultsRelevantSettings(50)

