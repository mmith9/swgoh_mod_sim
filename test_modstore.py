from modStore import *



modStore=ModStore()
testlevel=2

if testlevel==1:
    #for x in range(0,modStore.storeModCount):
    #    print(modStore.storeModList[x])

    mod=Mod()
    mod.primary="offense %"
    mod.grade="a"
    mod.secondary["speed"]=[1,3]
    mod.modSet="health %"
    mod.shape="square"

    #print(modStore.getModChance(mod))
    #print(modStore.getModChance(mod)*modStore.getModPrice()*64)

    item={"shape":"triangle", "grade":"a", "modSet":"offense %", "primary":"any", "speed":"any"}
    itemExpanded=[]

    modStore.expandItemToItems(item, itemExpanded)

    for x in itemExpanded:
        print(x)

if testlevel==2:

    wishlist=[
        {"pips":5, "shape":"not arrow", "grade":"a", "modSet":"any", "primary":"any", "speed":"5"}
    ]


    budget=800000
    bought=modStore.modShopping(budget, wishlist)
    for item in bought:
        print(item)
        mod=item["mod"]
        print(mod.pips, mod.shape, mod.grade, mod.modSet, mod.primary, mod.secondary, item["dailyCreditCost"], item["dailyProbability"])
