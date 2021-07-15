import json
import csv
import requests
from mod import *
from modAnalysis import *
import matplotlib.pyplot as plt

from api_swgoh_help import api_swgoh_help, settings

# Change the settings below
creds = settings('smith007', '900FYO5683FJK2W6DFUYK57890')
client = api_swgoh_help(creds)
pikappa = 479536574
scythe= 313757769 

players=client.fetchPlayers(pikappa)
units=players[0]["roster"]

translateStats={
    'UNITSTATOFFENSEPERCENTADDITIVE':"offense %",
    'UNITSTATMAXSHIELDPERCENTADDITIVE':"protection %",
    'UNITSTATDEFENSEPERCENTADDITIVE':"defense %",
    'UNITSTATMAXHEALTHPERCENTADDITIVE':"health %",
    
    'UNITSTATOFFENSE':"offense",
    'UNITSTATMAXSHIELD':"defense",
    'UNITSTATDEFENSE':"defense",
    'UNITSTATMAXHEALTH':"health",
    
    'UNITSTATCRITICALCHANCEPERCENTADDITIVE':"crit chance",
    'UNITSTATRESISTANCE':"tenacity",
    'UNITSTATACCURACY':"potency",
    'UNITSTATCRITICALDAMAGE':"crit dmg",
    'UNITSTATSPEED':"speed",
    'UNITSTATCRITICALNEGATECHANCEPERCENTADDITIVE':"crit avoidance",
    'UNITSTATEVASIONNEGATEPERCENTADDITIVE':"accuracy"
}

tierToGrade={1:"e", 2:"d", 3:"c", 4:"b", 5:"a"}

slotToShape={1:"square", 2:"arrow", 3:"diamond", 4:"triangle", 5:"circle", 6:"cross"}

modList=[]

for unit in units:
    if unit["combatType"]=="CHARACTER":
        mods=unit["mods"]
        for mod in mods:
            newMod=Mod()
            #print(mod)
            level=mod["level"]
            grade=tierToGrade[mod["tier"]]
            primary=translateStats[mod["primaryStat"]["unitStat"]]
            secondary={}
            for stat in mod["secondaryStat"]:
                secondary[translateStats[stat["unitStat"]]]=[stat["roll"],stat["value"]]

            #print(level,grade,primary,secondary)
            set=mod["set"]
            pips=mod["pips"]
            shape=slotToShape[mod["slot"]]
            newMod.setStats(level,grade,shape,set,pips,primary,secondary)
            modList.append(newMod)

test=ModAnalysis()
test.analyzeModList(modList)

print(test.speedDistribution)

plt.style.use('seaborn')

fig, ax = plt.subplots()
#ax.plot(range(0,32),speeds)

colorList={"square":"rs","arrow":"r--","diamond":"yd","triangle":"g^","circle":"b.","cross":"bX"}

for shape in Mod.getShapes():
    if shape!="arrow":
        plt.plot(range(0,32),test.speedPerShapeDistribution[shape][0:32],colorList[shape])

plt.show()

# for newMod in modList:
#         print(newMod.getShape())
#         print(newMod.getLevel())
#         print(newMod.getGrade())
#         print(newMod.getPips())
#         print(newMod.getPrimary())
#         print(newMod.getSecondary())

