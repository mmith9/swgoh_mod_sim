
import processJobs
from datetime import datetime



if __name__ == '__main__':

    inFile="ITERUNIQ06x"
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
    