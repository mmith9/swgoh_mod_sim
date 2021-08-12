
import os
import simSettings

files=3000

prefix="HEAT11"

for x in range(0,files):

    name1="d:/_swgoh/iterations/_11"+prefix+"x" + simSettings.SimSettings.padNameWithZeros(str(x),6) + ".json"

    name2="d:/_swgoh/iterations/_11/"+prefix+"x" +simSettings.SimSettings.padNameWithZeros(str(x),6) + ".json"
    if os.path.isfile(name1):
        #print(".", end="")
        #print(name2)
        os.rename(name1, name2)



