# swgoh_mod_sim
# swgoh_mod_sim 2.0 with HEAT 

# This is a mod slicing simulator(1) for optimizing mod slicing strategy, using exhaustive search over defined scope of possible scenarios
# heat 2.0 also uses graph mapping with re-use capability for improved performance (about 1000 times faster than v1.0)

# (1) what is mod slicing - A Star Wars game by CG, featuring items called 'mods' that give ingame characters certain bonuses
#     You are probably not interested in the project if you don't know this allready

# Other features include 
# - calculating real speed distribution instead of monte carlo approximation
# - real budget for slicing costs, all materials included
# - multithreading or even multi machine processing (manual distribution) using generated scenario files
