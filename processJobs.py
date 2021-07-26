import json
import multiprocessing
from budgeted_evaluation import *
import os

class JobsProcessing:
    def __init__(self):

        pass

    def processFiles(self, inputPrefix="ITER", outputPrefix="EVAL", filesTotal=0, fileCut=1000, multiproc=False):

        for filenum in range(1,filesTotal+1):
            jobsFilename="iteration_results/"+inputPrefix+str(filenum)+"x"+str(fileCut)+".json"
            outputFilename="iteration_results/"+outputPrefix+str(filenum)+"x"+str(fileCut)+".json"
            with open(jobsFilename, "r") as fp:
                jobsList=json.load(fp)
            
            if os.path.isfile(outputFilename):
                pass
            else:
                results=self.processJobsList(jobsList, multiproc=multiproc)
                with open(outputFilename, "w") as fp:
                    json.dump(results, fp)


    def processJobsList(self, jobsList, multiproc=False):

        if multiproc==False:
            results=[]
            for job in jobsList:
                jobNumber=job[0]
                jobSettings=job[1]
        
                evaluation=BudgetedEvaluation()
                output=evaluation.evaluateWithBudget(jobSettings)

                results.append({"job":jobNumber, "settings":jobSettings, "scores":output})

            return results
        else:
            #print(jobsList)
            results=self.processJobsListMulti(jobsList)
            return results

    def readResults(self, inputPrefix="EVAL", filesTotal=0, fileCut=1000):
        self.results=[]

        for filenum in range(1,filesTotal+1):
            outputFilename="iteration_results/"+inputPrefix+str(filenum)+"x"+str(fileCut)+".json"
            with open(outputFilename, "r") as fp:
                resultsCut=json.load(fp)
                self.results+= resultsCut      

    def displayResults(self, linesMax=40):
        lines=0
        for job in self.results:
            print(job["job"])
            lines+=1
            if lines>=linesMax:
                break
    
    def sortJobsBy(self, sortScore):
        if sortScore=="high":
            self.results.sort(key=rtValueHigh, reverse=True)

        if sortScore=="mid":
            self.results.sort(key=rtValueMid, reverse=True)
        
        if sortScore=="low":
            self.results.sort(key=rtValueLow, reverse=True)

        if sortScore=="Elisa":
            self.results.sort(key=rtValueElisa, reverse=True)

        if sortScore=="ElisaM14":
            self.results.sort(key=rtValueElisaM14, reverse=True)
                
    def processJobsListMulti(self, jobsList):
        pool=multiprocessing.Pool(4)
        with pool:
            results=pool.map(wrapperFunc, jobsList)
        return results

    def displayResultsRelevantSettings(self, linesMax=40):
        for jobIndex in range (linesMax):
            job = self.results[jobIndex]
            
            jobNum=job["job"]
            jobSettings=job["settings"]
            jobScores=job["scores"]

            print("job number ", jobNum, " scores: ",end="", sep="")
            for score in jobScores["speedValue"]:
                print(score,":",jobScores["speedValue"][score], " ", end="",sep="")
            print()

            print("uncover stats on grey", jobSettings["uncoverStatsLimit"]["e"]["square"])
            print("minInitialSpeed on grey", jobSettings["minInitialSpeed"]["e"]["square"])
            print("minSpeedToKeep", jobSettings["minSpeedToKeep"]["1"]["e"]["square"])
            print("minSpeedToSlice:")

            for grade in Mod.grades:
                print("grade:", grade," ", end="",sep="")
                for speedBumps in Mod.speedBumpsStr:
                    if (Mod.speedBumpsStr.index(speedBumps) <= Mod.grades.index(grade)+1) and (speedBumps!="5"):
                        speed=jobSettings["minSpeedToSlice"][speedBumps][grade]["square"]
                        bumps=int(speedBumps)

                        if speed <= 5+6*(bumps-1):
                            print("\t",speedBumps,":", jobSettings["minSpeedToSlice"][speedBumps][grade]["square"]," ", end="",sep="")
                        else:
                            print("\t",end="",sep="")
                   
                print()
            


def wrapperFunc(job):
    jobNumber=job[0]
    jobSettings=job[1]
        
    evaluation=BudgetedEvaluation()
    output=evaluation.evaluateWithBudget(jobSettings)
    
    return {"job":jobNumber, "settings":jobSettings, "scores":output}

def rtValueHigh(x):
    return x["scores"]["speedValue"]["high"]

def rtValueMid(x):
    return x["scores"]["speedValue"]["mid"]

def rtValueLow(x):
    return x["scores"]["speedValue"]["low"]

def rtValueElisa(x):
    return x["scores"]["speedValue"]["Elisa"]

def rtValueElsiaM14(x):
    return x["scores"]["speedValue"]["ElisaM14"]