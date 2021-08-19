
import os
import simSettings

files=30000



for x in range(0,files):

    name1="iteration_results/ITERX11x" + simSettings.SimSettings.padNameWithZeros(str(x),6) + ".json"

    name2="iteration_results/ITER11x" + simSettings.SimSettings.padNameWithZeros(str(x),6) + ".json"
    if os.path.isfile(name1):
        #print(".", end="")
        #print(name2)
        os.rename(name1, name2)



