from simSettings import *
from datetime import datetime

simSettings=SimSettings()

#disable all slicing except explicitly permitted 
simSettings.set("minSpeedToSlice", 100, grade="any", shape="any", speedBumps="any")

#best policy to date
simSettings.set("uncoverStatsLimit", 3, grade="e")
simSettings.set("minInitialSpeed", 5, grade="e")
simSettings.set("minSpeedToKeep", 10, grade=["e","d","c","b"])

simSettings.set("minSpeedToSlice", 0 , grade="e", speedBumps=1)  #min initial speed handles this

simSettings.set("minSpeedToSlice", 9 , grade="d", speedBumps=2)

simSettings.set("minSpeedToSlice", 10 , grade="c", speedBumps=2)
simSettings.set("minSpeedToSlice", 13 , grade="c", speedBumps=3)

simSettings.set("minSpeedToSlice", 10 , grade="b", speedBumps=2)
simSettings.set("minSpeedToSlice", 14 , grade="b", speedBumps=3)
simSettings.set("minSpeedToSlice", 17 , grade="b", speedBumps=4)

simSettings.set("minSpeedToSlice", 14 , grade="a", speedBumps=3) 
simSettings.set("minSpeedToSlice", 17 , grade="a", speedBumps=4) 

# uncover stats on grey 3
# minInitialSpeed on grey 5
# minSpeedToSlice:
# grade:e         1:5
# grade:d         2:9
# grade:c         2:10    3:13
# grade:b         2:10    3:14    4:17
# grade:a         2:100   3:14    4:17
# grade:6e                3:15    4:18
# grade:6d                3:15    4:18
# grade:6c                3:15    4:18
# grade:6b                3:17    4:18
# grade:6a                3:100   4:100
# seems to be best, sustainable strategy, it's actually far from exhausting limited 6dot mats

######## end of policy


iterateList=[
    {"target":"uncoverStatsLimit", "range":[2,3] , "shape":"any", "grade":"e", "speedBumps":0},  
    {"target":"minInitialSpeed", "range":[5] , "shape":"any", "grade":"e", "speedBumps":0},  # 5 is always the best
    
    {"target":"minSpeedToSlice", "range":[5,6] , "shape":"any", "grade":"d", "speedBumps":1},
    {"target":"minSpeedToSlice", "range":[8,9,10] , "shape":"any", "grade":"d", "speedBumps":2},

    {"target":"minSpeedToSlice", "range":[5,6] , "shape":"any", "grade":"c", "speedBumps":1},
    {"target":"minSpeedToSlice", "range":[8,9,10], "shape":"any", "grade":"c", "speedBumps":2},
    {"target":"minSpeedToSlice", "range":[10,11,12,13,14,15] , "shape":"any", "grade":"c", "speedBumps":3},
       
    {"target":"minSpeedToSlice", "range":[5,6] , "shape":"any", "grade":"b", "speedBumps":1},
    {"target":"minSpeedToSlice", "range":[9,10,11], "shape":"any", "grade":"b", "speedBumps":2}, 
    {"target":"minSpeedToSlice", "range":[10,11,12,13,14,15], "shape":"any", "grade":"b", "speedBumps":3}, 
    {"target":"minSpeedToSlice", "range":[13,14,15,16,17,18] , "shape":"any", "grade":"b", "speedBumps":4}, #never shows 18

    {"target":"minSpeedToSlice", "range":[5,6] , "shape":"any", "grade":"a", "speedBumps":1},
    {"target":"minSpeedToSlice", "range":[10,11,12] , "shape":"any", "grade":"a", "speedBumps":2},  # no use, always pops 12 in top 100 scores
    {"target":"minSpeedToSlice", "range":[12,13,14,15], "shape":"any", "grade":"a", "speedBumps":3},
    {"target":"minSpeedToSlice", "range":[13,14,15,16,17,18] , "shape":"any", "grade":"a", "speedBumps":4},   #never shows 18

    {"target":"minSpeedToSlice", "range":[11,12,13] , "shape":"any", "grade":"6e", "speedBumps":2}, 
    {"target":"minSpeedToSlice", "range":[11,12,13] , "shape":"any", "grade":"6d", "speedBumps":2}, 
    {"target":"minSpeedToSlice", "range":[11,12,13] , "shape":"any", "grade":"6c", "speedBumps":2}, 
    {"target":"minSpeedToSlice", "range":[11,12,13] , "shape":"any", "grade":"6b", "speedBumps":2}, 

    {"target":"minSpeedToSlice", "range":[13,14,15,16] , "shape":"any", "grade":"6e", "speedBumps":3}, 
    {"target":"minSpeedToSlice", "range":[13,14,15,16] , "shape":"any", "grade":"6d", "speedBumps":3}, 
    {"target":"minSpeedToSlice", "range":[13,14,15,16] , "shape":"any", "grade":"6c", "speedBumps":3}, 
    {"target":"minSpeedToSlice", "range":[15,16,17,18] , "shape":"any", "grade":"6b", "speedBumps":3}, 

    {"target":"minSpeedToSlice", "range":[14,15,16,17,18,19] , "shape":"any", "grade":"6e", "speedBumps":4}, 
    {"target":"minSpeedToSlice", "range":[14,15,16,17,18,19] , "shape":"any", "grade":"6d", "speedBumps":4}, 
    {"target":"minSpeedToSlice", "range":[14,15,16,17,18,19] , "shape":"any", "grade":"6c", "speedBumps":4}, 
    {"target":"minSpeedToSlice", "range":[15,16,17,18,19] , "shape":"any", "grade":"6b", "speedBumps":4}, 
]


simSettings.general["creditsLimit"] = 11000000
simSettings.general["shipCreditsLimit"] = 2500000
simSettings.noHash=iterateList


start_time = datetime.now()

iterateList.reverse()  # optimization for faster branch pruning

output=simSettings.iterateSettingsByListQuick(iterateList, outputPrefix="ITER11", fileCut=50000, sanityConstraint=1, lightweight=1)
#output=simSettings.iterateSettingsByListQuick(iterateList, benchmarkPercent=1 , outputPrefix="ITER09", fileCut=10000, sanityConstraint=1, lightweight=1)
#output=simSettings.iterateSettingsByListQuick(iterateList, countBranchOnly=1, sanityConstraint=1)

end_time = datetime.now()

print(output)

