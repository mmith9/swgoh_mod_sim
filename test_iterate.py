from iterateAndCompareSims import *
import json

if __name__ == "__main__":

    print("MAIN START ONCE")
    globalManager=multiprocessing.Manager()
    globalReturnDict=globalManager.dict()
    test=ModSimulationIteration()

    #output=test.runSimsV1(countBranchOnly=True)

    output = test.runSimsV1(benchmark=0.1)

    #output=test.runSimsV1()

    print(test.branchCount)


    #   for x in output:
    #       print(rtValueHigh(x), rtValueMid(x), rtValueLow(x), rtValueElisa(x), rtValueElisaM14(x))
        
    with open('iteration_results/results_high.json', "w") as file:
        output.sort(key=rtValueHigh, reverse=True)    
        list=[]
        for x in output:
            score=rtValueHigh(x)
            settings=x["settings"]
            costs=x["costs"]
            scores=x["scores"]
            list.append({"score":score, "settings":settings, "costs":costs, "scores":scores})
        json.dump(list ,file)

    with open('iteration_results/results_mid.json', "w") as file:
        output.sort(key=rtValueMid, reverse=True)    
        list=[]
        for x in output:
            score=rtValueMid(x)
            settings=x["settings"]
            costs=x["costs"]
            scores=x["scores"]
            list.append({"score":score, "settings":settings, "costs":costs, "scores":scores})
        json.dump(list ,file)

    with open('iteration_results/results_low.json', "w") as file:
        output.sort(key=rtValueLow, reverse=True)    
        list=[]
        for x in output:
            score=rtValueLow(x)
            settings=x["settings"]
            costs=x["costs"]
            scores=x["scores"]
            list.append({"score":score, "settings":settings, "costs":costs, "scores":scores})
        json.dump(list ,file)

    with open('iteration_results/results_Elisa.json', "w") as file:
        output.sort(key=rtValueElisa, reverse=True)    
        list=[]
        for x in output:
            score=rtValueElisa(x)
            settings=x["settings"]
            costs=x["costs"]
            scores=x["scores"]
            list.append({"score":score, "settings":settings, "costs":costs, "scores":scores})
        json.dump(list ,file)

    with open('iteration_results/results_ElisaM14.json', "w") as file:
        output.sort(key=rtValueElisaM14, reverse=True)    
        list=[]
        for x in output:
            score=rtValueElisaM14(x)
            settings=x["settings"]
            costs=x["costs"]
            scores=x["scores"]
            list.append({"score":score, "settings":settings, "costs":costs, "scores":scores})
        json.dump(list ,file)


