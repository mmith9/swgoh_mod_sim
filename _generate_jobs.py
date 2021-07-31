from simSettings import *

test=SimSettings()

test.set("uncoverStatsLimit", 2, grade="e")
test.set("minInitialSpeed", 5, grade="e")
test.set("minSpeedToKeep", 10, grade=["e","d","c","b"])

#disable all slicing except explicitly permitted (a b c d e grades, not 6abcde)
test.set("minSpeedToSlice", 100, grade="any", shape="any", speedBumps="any")

test.set("minSpeedToSlice", 5 , grade="e", speedBumps=1)
#test.set("minSpeedToSlice", 8 , grade="d", speedBumps=2)

#best policy to date
test.set("uncoverStatsLimit", 3, grade="e")
test.set("minSpeedToSlice", 5 , grade="e", speedBumps=1)

test.set("minSpeedToSlice", 9 , grade="d", speedBumps=2)

test.set("minSpeedToSlice", 10 , grade="c", speedBumps=2)
test.set("minSpeedToSlice", 13 , grade="c", speedBumps=3)

test.set("minSpeedToSlice", 10 , grade="b", speedBumps=2)
test.set("minSpeedToSlice", 13 , grade="b", speedBumps=3)
test.set("minSpeedToSlice", 14 , grade="b", speedBumps=4)

test.set("minSpeedToSlice", 14 , grade="a", speedBumps=3) 
test.set("minSpeedToSlice", 17 , grade="a", speedBumps=4) 
######## end of policy

#allow 6dot slicing
test.set("minSpeedToSlice", 0 , grade="6e")
test.set("minSpeedToSlice", 0 , grade="6d")
test.set("minSpeedToSlice", 0 , grade="6c")
test.set("minSpeedToSlice", 0 , grade="6b")



iterateList=[
    #{"target":"uncoverStatsLimit", "range":[2,3,4] , "shape":"any", "grade":"e", "speedBumps":0},  ## never 0 1 or 2 in top scores, 4 is rare
    #{"target":"minInitialSpeed", "range":[3,4,5] , "shape":"any", "grade":"e", "speedBumps":0}, 
    
    {"target":"minSpeedToSlice", "range":[8,9] , "shape":"any", "grade":"d", "speedBumps":2},

    {"target":"minSpeedToSlice", "range":[9,10,11] , "shape":"any", "grade":"c", "speedBumps":2},
    {"target":"minSpeedToSlice", "range":[12,13,14] , "shape":"any", "grade":"c", "speedBumps":3},
       
    {"target":"minSpeedToSlice", "range":[9,10,11,12] , "shape":"any", "grade":"b", "speedBumps":2}, ## always shows 10 as it was max, try higher
    {"target":"minSpeedToSlice", "range":[12,13,14] , "shape":"any", "grade":"b", "speedBumps":3}, 
    {"target":"minSpeedToSlice", "range":[17] , "shape":"any", "grade":"b", "speedBumps":4}, #never shows 18

   # {"target":"minSpeedToSlice", "range":[7,8,9,10,11,12] , "shape":"any", "grade":"a", "speedBumps":2},  # no use, always pops 12 in top 100 scores
    {"target":"minSpeedToSlice", "range":[12,13,14] , "shape":"any", "grade":"a", "speedBumps":3},
    {"target":"minSpeedToSlice", "range":[17] , "shape":"any", "grade":"a", "speedBumps":4},   #never shows 18

    {"target":"minSpeedToSlice", "range":[15] , "shape":"any", "grade":"6e", "speedBumps":3}, 
    {"target":"minSpeedToSlice", "range":[15] , "shape":"any", "grade":"6d", "speedBumps":3}, 
    {"target":"minSpeedToSlice", "range":[15] , "shape":"any", "grade":"6c", "speedBumps":3}, 
    {"target":"minSpeedToSlice", "range":[17] , "shape":"any", "grade":"6b", "speedBumps":3}, 

    {"target":"minSpeedToSlice", "range":[18] , "shape":"any", "grade":"6e", "speedBumps":4}, 
    {"target":"minSpeedToSlice", "range":[18] , "shape":"any", "grade":"6d", "speedBumps":4}, 
    {"target":"minSpeedToSlice", "range":[18] , "shape":"any", "grade":"6c", "speedBumps":4}, 
    {"target":"minSpeedToSlice", "range":[18] , "shape":"any", "grade":"6b", "speedBumps":4}, 
]

output=test.iterateSettingsByList(iterateList, outputPrefix="ITER06x", fileCut=5000, sanityConstraint=1)

#output=test.iterateSettingsByList(iterateList, benchmarkPercent=1 , outputPrefix="ITER06x", fileCut=5000, sanityConstraint=1)
#output=test.iterateSettingsByList(iterateList, countBranchOnly=1, sanityConstraint=1)


print(output)
