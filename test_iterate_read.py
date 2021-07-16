import json
from iterateAndCompareSims import *

with open("iteration_results/results_mid.json", "r") as file:
    list=json.load(file)
    lines=0
    position=0
    for x in list: #range(0,50):
        sts=x["settings"]
        score=x["score"]
        position+=1
        if sts["minInitialSpeed"]["e"]["square"]<7:
            lines+=1
            
            if lines<=40:

                print("grey uncover",sts["general"]["greyMaxInitialStats"],
                    "\tgrey",sts["minInitialSpeed"]["e"]["square"],
                    " \tgreen", sts["minLev12Speed"]["d"]["square"],
                    " \tblue", sts["minLev12Speed"]["c"]["square"],
                    " \tpurple", sts["minLev12Speed"]["b"]["square"],
                    "\tscore",score,"   \tposition"      ,position     )

