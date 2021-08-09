
import processJobs_heat
from datetime import datetime



if __name__ == '__main__':

    inFile="ITER08"
    outFile="HEAT08"
    fileCut=5000
    fileCount=300
    

    start_time = datetime.now()
    test=processJobs_heat.JobsProcessing()
    print("processing files")
    test.processFiles(filesTotal=fileCount, multiproc=True, inputPrefix=inFile, outputPrefix=outFile, fileCut=fileCut)
    print("processing done")
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    
    