import multiprocessing
import processJobs

if __name__ == '__main__':

    test=processJobs.JobsProcessing()

    test.processFiles(filesTotal=8, multiproc=True, inputPrefix="ITER01x", outputPrefix="EVAL01x")

    print("processing done")

    test.readResults(filesTotal=8, inputPrefix="EVAL01x")

    test.sortJobsBy("low")

    
    test.displayResultsRelevantSettings(50)

