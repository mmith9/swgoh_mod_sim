
import processJobs
from datetime import datetime



if __name__ == '__main__':

    inFile="ITER07"
    outFile="ITERUNIQ07"
    fileCut=5000
    fileCount=300
    

    start_time = datetime.now()
    test=processJobs.JobsProcessing()
    


    print("Filtering files vs database")
    test.filterOutJobsInDb(filesTotal=fileCount, inputPrefix=inFile, outputPrefix=outFile)
    print("Filtering done")
        
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    
    