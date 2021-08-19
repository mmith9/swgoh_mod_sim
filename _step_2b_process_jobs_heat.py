
import processJobs_heat
from datetime import datetime



if __name__ == '__main__':

    inFile="ITER11"
    outFile="HEAT11"
    fileCount=30000
    

    start_time = datetime.now()
    test=processJobs_heat.JobsProcessing()
    print("processing files")
    test.processFiles(filesTotal=fileCount, multiproc=True, inputPrefix=inFile, outputPrefix=outFile)
    print("processing done")
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    
    