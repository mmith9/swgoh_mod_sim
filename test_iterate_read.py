import json
from iterateAndCompareSims import *

with open("iteration_results/results_low.json", "r") as file:
    list=json.load(file)
    lines=0
    position=0
    for x in list: #range(0,50):
        sts=x["settings"]
        costs=x["costs"]
        score=x["score"]
        position+=1
        #print(costs)
        if sts["minInitialSpeed"]["e"]["square"]<100:
            lines+=1
            
            if lines<=40:

                print("grey uncover",sts["uncoverStatsLimit"]["e"]["square"],
                    "\tgrey",sts["minInitialSpeed"]["e"]["square"],
                    " \tgreen", sts["minSpeedToSlice"]["1"]["d"]["square"],
                    " \tblue", sts["minSpeedToSlice"]["1"]["c"]["square"],
                    " \tpurple", sts["minSpeedToSlice"]["1"]["b"]["square"],
                    "\tscore",score,"   \tposition"      ,position     
                    ,"energy ", costs["avgEnergy"])


