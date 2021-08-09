import json
import multiprocessing
import math

import budgeted_evaluation
import budgeted_evaluation_heat
import os
from datetime import datetime
import psutil
import mysql.connector
from copy import deepcopy
from simSettings import SimSettings

testlevel=90

class JobsProcessing:
    def __init__(self):
        self.results=[] 
        pass

    def processFileWrapper(self, filesTuple):
        self.processFile(filesTuple[0], filesTuple[1])

    def processFile(self, inputFilename, outputFilename):
        with open(inputFilename, "r") as fp:
            jobsList=json.load(fp)
                        
            results=self.processJobsList(jobsList)

            output={}
            output["header"] = jobsList["header"]
            output["results"] = results

            with open(outputFilename, "w") as fp:
                json.dump(output, fp)

    def processFiles(self, inputPrefix="ITER", outputPrefix="EVAL", filesTotal=0, fileCut=1000, multiproc=False):
        fileList=[]
        for filenum in range(0, filesTotal):
            jobsFilename="iteration_results/"+inputPrefix + "x" +str(filenum)+".json"
            outputFilename="iteration_results/"+outputPrefix + "x" + str(filenum)+".json"
            #print("input:", jobsFilename, outputFilename)
            if os.path.isfile(jobsFilename):
                if os.path.isfile(outputFilename):
                    pass
                else:
                    fileList.append( (jobsFilename, outputFilename) )

        if multiproc==False:
            for job in fileList:
                print("Processing ", job[0])
                self.processFile(job[0], job[1])

        else:
            print(fileList)
            pool=multiprocessing.Pool(multiprocessing.cpu_count())
            with pool:
                results=pool.map(self.processFileWrapper, fileList)
            pool.close()
            pool.join()
            
            


    def processJobsList(self, jobsList):

        budgetedEvaluation=budgeted_evaluation_heat.BudgetedEvaluation()

        baseSettings=jobsList["header"]["settingsSnapshot"]
        lightweightJobList=jobsList["jobList"]
        jobList=[]

        print("Recreating job list from lightweight form")
        for settingsChanges in lightweightJobList:
            jobList.append( (baseSettings, settingsChanges) )
        print("Recreated list")

        results=[]

        for job in jobList:

            baseSettings=job[0]

            jobNumber=job[1][0]
            settingsChange=job[1][1]
            settingsFingerprint=job[1][2]
            settingsHash=job[1][3]

            if testlevel>1:
                print(jobNumber,"|", end="", sep="")

            if testlevel > 99:
                print(jobNumber)
                print("base")
                print(baseSettings)
                print()
                print("change")
                print(settingsChange)
                
            jobSettings = deepcopy(baseSettings)

            if testlevel > 99:
                print("---------------------------")
                print(jobNumber)
                print("base")
                print(baseSettings)
                print()
                print("change")
                print(settingsChange)
                print()
                print("recreated")
                print(jobSettings)
                print()
                print(SimSettings.settingsFingerprintOf(jobSettings))
                print()
                print(jobSettings["minSpeedToSlice"]["3"])
                print()
                with open("iteration_results/recreated"+str(jobNumber), "w") as fp:
                    json.dump(jobSettings, fp)
                
                print()

            SimSettings.mergeSettings(jobSettings, settingsChange)

            if testlevel > 99:
                print("updated")
                
                with open("iteration_results/updated"+str(jobNumber), "w") as fp:
                    json.dump(jobSettings, fp)
                
                print(SimSettings.settingsFingerprintOf(jobSettings))
                print(SimSettings.settingsHashOf(jobSettings))
                print(settingsHash)
                print()
            
            #    print(jobSettings)

                print()
                print(jobSettings["minSpeedToSlice"]["3"])
                print()
            

                assert(SimSettings.settingsFingerprintOf(jobSettings) ==settingsFingerprint )
                if testlevel > 99:
                    print("fingetprint ok")

                assert(SimSettings.settingsHashOf(jobSettings) == settingsHash)
                if testlevel > 99:
                    print("hash ok")

                if testlevel>0:
                    print(jobNumber, end="|")

                if testlevel > 99:
                    print("---------------------------")
                    assert(False)

            output=budgetedEvaluation.evaluateWithBudget(jobSettings)

            results.append({"job":jobNumber, "settings":settingsChange, "settingsHash": settingsHash, "settingsFingerprint":settingsFingerprint, "scores":output })
            
        return results

    def readResults(self, inputPrefix="FILTER", filesTotal=0):
        self.results=[]
        if testlevel>0:
            print(psutil.virtual_memory())

        for filenum in range(0, filesTotal):
            if testlevel>0:
                startUsedMem=psutil.virtual_memory()[3]
                print("file ", filenum +1 , "out of", filesTotal)
            inputFilename="iteration_results/"+inputPrefix + "x" + str(filenum) + ".json"
            
            if testlevel>0:
                print("trying", inputFilename)

            if os.path.isfile(inputFilename):
                with open(inputFilename, "r") as fp:
                    resultsCut=json.load(fp)
                    self.results+= resultsCut      

                if testlevel>0:
                    print(psutil.virtual_memory())
                    endUsedMem=psutil.virtual_memory()[3]
                    print("mem diff:",(startUsedMem-endUsedMem)/ 1024,"Kb")
                    print()

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
        baseSettings=jobsList["header"]["settingsSnapshot"]
        lightweightJobList=jobsList["jobList"]
        jobList=[]

        print("Recreating job list for multiprocessing pool")
        for settingsChanges in lightweightJobList:
            jobList.append( (baseSettings, settingsChanges) )
        print("Recreated list")

        pool=multiprocessing.Pool(multiprocessing.cpu_count())
        with pool:
            results=pool.map(wrapperFunc, jobList)
        return results

    def displayResultsRelevantSettings(self, linesMax=40):
        for jobIndex in range (linesMax):
            job = self.results[jobIndex]
            
            jobNum=job["job"]
            jobSettings=job["settings"]
            jobScores=job["scores"]

            print("job number ", jobNum, " scores: ",end="", sep="")
            for score in jobScores["speedValue"]:
                print(score,":", f'{truncate(jobScores["speedValue"][score],3):,}' , " ", end="",sep="")
            print()

            print("Budget remaining")
            for item in ["credits", "shipCredits", "modEnergy", "amplifier", "capacitor", "module", "unit", "resistor", "microprocessor"]:
                print(item,":", truncate(jobScores["budgetBreakdown"]["budgetRemaining"][item], 3), " ", end="")
            print("| Cap Amp bought:", truncate(jobScores["budgetBreakdown"]["capAmpBought"], 3))
           

            print("uncover stats on grey:", jobSettings["uncoverStatsLimit"]["e"]["square"], end="")
            print(" |minInitialSpeed on grey:", jobSettings["minInitialSpeed"]["e"]["square"], end="")
            print(" |avg roll energy cost:",jobScores["budgetBreakdown"]["avgRollModEnergyCost"])
            #FILTERED print("minSpeedToKeep", jobSettings["minSpeedToKeep"]["1"]["e"]["square"])
            print("minSpeedToSlice:")

            for grade in Mod.allGrades:
                print("grade:", grade," ", end="",sep="")
                for speedBumps in Mod.speedBumpsStr:
                    if (Mod.speedBumpsStr.index(speedBumps) <= Mod.allGrades.index(grade)+1) and (speedBumps!="5"):

                        if speedBumps in jobSettings["minSpeedToSlice"].keys():
                            if grade in jobSettings["minSpeedToSlice"][speedBumps].keys():


                                speed=jobSettings["minSpeedToSlice"][speedBumps][grade]["square"]
                                bumps=int(speedBumps)

                                if speed <= 5+6*(bumps-1)+100:
                                    print("\t",speedBumps,":", jobSettings["minSpeedToSlice"][speedBumps][grade]["square"]," ", end="",sep="")
                                else:
                                    print("\t",end="",sep="")
                   
                print()
            print()

    def filterOutIrrelevantCrap(self, inputPrefix="EVAL", outputPrefix="FILTER", fileCut=5000):
        # filtering required because of memory limitations

        fileNum=0
        inputFileName="iteration_results/" + inputPrefix + "x" + str(fileNum) + ".json"
        
        if testlevel>0:
            print("trying to filter", inputFileName)

        while os.path.isfile(inputFileName):
            outputFileName="iteration_results/" + outputPrefix + "x" + str(fileNum) + ".json"
            if os.path.isfile(outputFileName):
                print("skipping")
                pass

            else:
                with open(inputFileName, "r") as fp:
                    results=json.load(fp)
                
                if testlevel>0:
                    print("filtering")

                for result in results:

                    if testlevel>15:
                        print("settings size", len(json.dumps(result["scores"])))

                    del(result["settings"]["general"])
                    del(result["settings"]["modStore"])
                    
                    del(result["settings"]["minInitialSpeed"]["d"])
                    del(result["settings"]["minInitialSpeed"]["c"])
                    del(result["settings"]["minInitialSpeed"]["b"])
                    del(result["settings"]["minInitialSpeed"]["a"])

                    del(result["settings"]["uncoverStatsLimit"]["d"])
                    del(result["settings"]["uncoverStatsLimit"]["c"])
                    del(result["settings"]["uncoverStatsLimit"]["b"])
                    del(result["settings"]["uncoverStatsLimit"]["a"])

                    for shape in ["arrow", "diamond", "circle", "cross", "triangle"]:
                        del(result["settings"]["uncoverStatsLimit"]["e"][shape])
                        del(result["settings"]["minInitialSpeed"]["e"][shape])

                    del(result["settings"]["minSpeedToKeep"])
                
                    del(result["settings"]["minSpeedToSlice"]["0"])
                    del(result["settings"]["minSpeedToSlice"]["5"])
                    
                    for grade in ["d", "c", "b", "a", "6e" , "6d", "6c", "6b", "6a"]:
                        del(result["settings"]["minSpeedToSlice"]["1"][grade])

                    for speedBumps in ["2"]:                                     ##, "3", "4" ]:
                        for grade in ["6e", "6d", "6c", "6b", "6a"]:
                            del(result["settings"]["minSpeedToSlice"][speedBumps][grade])
                    
                    for speedBumps in result["settings"]["minSpeedToSlice"]:
                        for grade in result["settings"]["minSpeedToSlice"][speedBumps]:
                            for shape in ["arrow", "diamond", "circle", "cross", "triangle"]:
                                del(result["settings"]["minSpeedToSlice"][speedBumps][grade][shape])

                    del(result["scores"]["squaresValue"])
                    del(result["scores"]["diamondsValue"])
                    del(result["scores"]["circlesValue"])
                    del(result["scores"]["crossesValue"])
                    del(result["scores"]["trianglesValue"])

                    del(result["scores"]["rltilt"])
                    del(result["scores"]["targetability"])

                    result["scores"]["budgetBreakdown"]["avgRollModEnergyCost"]=result["scores"]["budgetBreakdown"]["budgetRoll"]["modEnergy"]                    
                    del(result["scores"]["budgetBreakdown"]["budgetRoll"])
                    del(result["scores"]["budgetBreakdown"]["budgetBuy"])
                    del(result["scores"]["budgetBreakdown"]["Rbought"])
                    del(result["scores"]["budgetBreakdown"]["Bbought"])
                    del(result["scores"]["speedDistribution"])

                if testlevel>0 :
                    print("saving ", outputFileName)
                    
                with open(outputFileName, "w") as fp:
                    json.dump(results, fp)
            
            fileNum+= 1
            inputFileName="iteration_results/" + inputPrefix + "x" + str(fileNum) + ".json"

    def filterByX(self, filter="none", value="none"):
        filteredJob=JobsProcessing()

        if filter=="uncoverStatsLimit":
            for job in self.results:
                jobSettings=job["settings"]
                if jobSettings["uncoverStatsLimit"]["e"]["square"] == value:
                    filteredJob.results.append(job)

        if filter=="microprocessor":
            for job in self.results:
                jobScores=job["scores"]
                if jobScores["budgetBreakdown"]["budgetRemaining"]["microprocessor"] > value:
                    filteredJob.results.append(job)

        return filteredJob

    def loadTopResultsFromDb(self, maxTopResults=100):

        mysqlDatabaseName="swgoh_sim_results"
        mysqlUser=os.environ.get("mysql_user")
        mysqlPassword=os.environ.get("mysql_password")

        try:
            with mysql.connector.connect(
                host="localhost",
                user=mysqlUser,
                password=mysqlPassword,
                database=mysqlDatabaseName,
                ) as connection:
                cursor=connection.cursor()

                for valueFunc in ["high", "mid", "low", "Elisa", "ElisaM14"]:
                    select_top_scores_query="SELECT fingerprint, hash, settings, scores, score_"+valueFunc+" FROM sim_results ORDER BY score_"+valueFunc+" DESC LIMIT "+str(maxTopResults)
                    if testlevel>1 :
                        print(select_top_scores_query)
                    cursor.execute(select_top_scores_query)
                    results=cursor.fetchall()

                    for result in results:
                        if testlevel>15:
                            print(".",end="")
                        fingerprint=result[0]
                        hash=result[1]
                        settings=json.loads(result[2])
                        scores=json.loads(result[3])

                        if "avgRollModEnergyCost" not in scores["budgetBreakdown"].keys():
                            scores["budgetBreakdown"]["avgRollModEnergyCost"]=scores["budgetBreakdown"]["budgetRoll"]["modEnergy"]   

                        tmpDict={}
                        tmpDict["job"]={"fingerprint":fingerprint, "hash":hash}
                        tmpDict["settings"]=settings
                        tmpDict["scores"]=scores
                        self.results.append(tmpDict)

        except mysql.connector.Error as e:
            print(e)     
    
    def filterOutJobsInDb(self, filesTotal=30, inputPrefix="ITER", outputPrefix="ITERUNIQ"):
        mysqlDatabaseName="swgoh_sim_results"
        mysqlUser=os.environ.get("mysql_user")
        mysqlPassword=os.environ.get("mysql_password")
        fileNum=0
        jobsList=[]

        while fileNum<filesTotal:
            inputFilename="iteration_results/"+inputPrefix + "x" + str(fileNum) + ".json"
            outputFilename="iteration_results/"+outputPrefix + "x" + str(fileNum) + ".json"            
            fileNum+= 1
            
            print("trying file:", inputFilename)
            if os.path.isfile(outputFilename):
                print("skipping, output file allready exists")
            if os.path.isfile(inputFilename) and not os.path.isfile(outputFilename) :
                print("Reading file ", inputFilename)
                with open(inputFilename, "r") as fp:
                    jobsList=json.load(fp)

                uniqueJobsList=[]
                uniqueJobsCount=0
                allJobsCount=0
                try:
                    with mysql.connector.connect(
                        host="localhost",
                        user=mysqlUser,
                        password=mysqlPassword,
                        database=mysqlDatabaseName,
                    ) as connection:
                        cursor=connection.cursor()

                        for job in jobsList:
                            allJobsCount+= 1
                            jobNum=job[0]
                            jobSettings=job[1]
                            jobFingerprint=job[2]
                            jobHash=job[3]
                            
                            fingerprint=SimSettings.settingsFingerprintOfGetAll(jobSettings)
                            hash=SimSettings.settingsHashOfGetAll(jobSettings)

                            assert(jobFingerprint==fingerprint)
                            assert(jobHash==hash)

                            select_check_exist_query="SELECT fingerprint, hash FROM sim_results WHERE fingerprint=" +jobFingerprint +" AND hash=" +str(jobHash)
                            cursor.execute(select_check_exist_query)
                            allreadyExist=cursor.fetchall()
                            if not allreadyExist:    # list is empty
                                uniqueJobsList.append(job)
                                uniqueJobsCount+= 1
                                #print("+", jobHash, " ", sep="", end="")
                            else:
                                #print("-", jobHash, " ", sep="", end="")
                                pass
                        print("Unique jobs", uniqueJobsCount, "out of", allJobsCount )
                except mysql.connector.Error as e:
                    print(e)

                print()
                print("saving unique jobs to", outputFilename)
                with open(outputFilename, "w") as fp:
                    json.dump(uniqueJobsList, fp)

    @staticmethod
    def prepareResultListForDb(batchResults, trim=0) -> dict:
        header=batchResults["header"]
        results=batchResults["results"]
        preparedResults=[]

        ## [fingerprint, hash, high, mid, low, elisa, elisam14, energy, credits, microproc, avg energy, cap_amp, settings_diff, all_results]

        for result in results:
            scores=result["scores"]

            preparedResult=[]
            preparedResult.append(result["settingsFingerprint"])
            preparedResult.append(result["settingsHash"])
            
            preparedResult.append(scores["speedValue"]["high"])
            preparedResult.append(scores["speedValue"]["mid"])
            preparedResult.append(scores["speedValue"]["low"])
            preparedResult.append(scores["speedValue"]["Elisa"])
            preparedResult.append(scores["speedValue"]["ElisaM14"])

            preparedResult.append(scores["budgetBreakdown"]["budgetRemaining"]["modEnergy"])
            preparedResult.append(scores["budgetBreakdown"]["budgetRemaining"]["credits"])
            preparedResult.append(scores["budgetBreakdown"]["budgetRemaining"]["microprocessor"])

            preparedResult.append(scores["budgetBreakdown"]["budgetRoll"]["modEnergy"])
            preparedResult.append(scores["budgetBreakdown"]["capAmpBought"])

            
            if trim > 0:
                for shape in ["squaresValue", "trianglesValue", "diamondsValue", "circlesValue", "crossesValue"]:
                    del(scores[shape])
                
                del(scores["rltilt"])
                del(scores["targetability"])
                del(scores["budgetBreakdown"]["budgetRoll"])
                del(scores["budgetBreakdown"]["budgetBuy"])
                del(scores["budgetBreakdown"]["Rbought"])
                del(scores["budgetBreakdown"]["Bbought"])
                del(scores["budgetBreakdown"]["BSbought"])
                del(scores["speedDistribution"])
            
            preparedResult.append(json.dumps(result["settings"]))
            preparedResult.append(json.dumps(scores))

            preparedResults.append(preparedResult)                                    
        
        return {"header": header, "resultListForDb": preparedResults}


def wrapperFunc(job):
    baseSettings=job[0]

    jobNumber=job[1][0]
    settingsChange=job[1][1]
    settingsFingerprint=job[1][2]
    settingsHash=job[1][3]

    if testlevel > 99:
        print(jobNumber)
        print("base")
        print(baseSettings)
        print()
        print("change")
        print(settingsChange)
        

    jobSettings = deepcopy(baseSettings)
    
    if testlevel > 99:
        print("---------------------------")
        print(jobNumber)
        print("base")
        print(baseSettings)
        print()
        print("change")
        print(settingsChange)
        print()
        print("recreated")
        print(jobSettings)
        print()
        print(SimSettings.settingsFingerprintOf(jobSettings))
        print()
        print(jobSettings["minSpeedToSlice"]["3"])
        print()
        with open("iteration_results/recreated"+str(jobNumber), "w") as fp:
            json.dump(jobSettings, fp)
        
        print()

    SimSettings.mergeSettings(jobSettings, settingsChange)

    if testlevel > 99:
        print("updated")
        
        with open("iteration_results/updated"+str(jobNumber), "w") as fp:
            json.dump(jobSettings, fp)
        
        print(SimSettings.settingsFingerprintOf(jobSettings))
        print(SimSettings.settingsHashOf(jobSettings))
        print(settingsHash)
        print()
    
    #    print(jobSettings)

        print()
        print(jobSettings["minSpeedToSlice"]["3"])
        print()
    

    assert(SimSettings.settingsFingerprintOf(jobSettings) ==settingsFingerprint )
    if testlevel > 99:
        print("fingetprint ok")

    assert(SimSettings.settingsHashOf(jobSettings) == settingsHash)
    if testlevel > 99:
        print("hash ok")

    if testlevel>0:
        print(jobNumber, end="|")

    if testlevel > 99:
        print("---------------------------")
        assert(False)

    evaluation=BudgetedEvaluation()
    output=evaluation.evaluateWithBudget(jobSettings)
    
    return {"job":jobNumber, "settings":settingsChange, "settingsHash": settingsHash, "settingsFingerprint":settingsFingerprint, "scores":output}

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def rtValueHigh(x):
    return x["scores"]["speedValue"]["high"]

def rtValueMid(x):
    return x["scores"]["speedValue"]["mid"]

def rtValueLow(x):
    return x["scores"]["speedValue"]["low"]

def rtValueElisa(x):
    return x["scores"]["speedValue"]["Elisa"]

def rtValueElisaM14(x):
    return x["scores"]["speedValue"]["ElisaM14"]

