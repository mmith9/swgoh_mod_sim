from mod import Mod

class SimSettings:

    def __init__(self):
        self.resources={"dailyEnergy":645, "dailyCredits":900000}

        self.general={
            "sellAccuracyArrows":1, "keepSpeedArrows":1, "ignoreRestOfArrows":1
            ,"sellNoSpeedMods":1, "sellTooLowInitialSpeedMods":1, "sellTooSlowFinalMods":1
            ,"allowSpeedBumpMisses":1
            ,"modSet":"offense"
            ,"quickPrimaryForking":1, "quickSecondaryForking":1, "quickSpeedForking":1
            }

        self.modStore={
            "enableShopping":True,
            "wishList":[
                {"pips":5, "shape":"not arrow", "grade":"a", "modSet":"any", "primary":"any", "speed":"5"}
            ]
        }       

        # level up mod to uncover stats DEFAULT 4 = uncover all
        self.uncoverStatsLimit={} #2 dimension dict  GRADE x SHAPE
        for grade in Mod.grades:
            self.uncoverStatsLimit[grade]={}
            for shape in Mod.shapes:
                self.uncoverStatsLimit[grade][shape]=4

        # If mod got speed uncovered, this is the limit when to sell DEFAULT 0
        self.minInitialSpeed={} #2 dimension dict, GRADE x SHAPE
        for grade in Mod.grades:
            self.minInitialSpeed[grade]={}
            for shape in Mod.shapes:
                self.minInitialSpeed[grade][shape]=0

        self.minSpeedToSlice={} #3 dimension dict. DEFAULT 0   BUMPS x GRADE x SHAPE
        for speedBumps in range(0,6):
            self.minSpeedToSlice[speedBumps]={}
            for grade in Mod.grades:
                self.minSpeedToSlice[speedBumps][grade]={}
                for shape in Mod.shapes:
                    self.minSpeedToSlice[speedBumps][grade][shape]=0

        self.minSpeedToKeep={} #3 dimension dict. DEFAULT 0 speed BUMPS x GRADE x SHAPE
        for speedBumps in range(0,6):
            self.minSpeedToKeep[speedBumps]={}
            for grade in Mod.grades:
                self.minSpeedToKeep[speedBumps][grade]={}
                for shape in Mod.shapes:
                    self.minSpeedToKeep[speedBumps][grade][shape]=0


    # NECCESARY FOR MULTIPROCESSING
    # modsimulation takes argument in this form
    def getAll(self):
        settings={
            "resources" : self.resources
            ,"general" : self.general
            ,"minInitialSpeed": self.minInitialSpeed
            ,"uncoverStatsLimit": self.uncoverStatsLimit
            ,"minSpeedToSlice": self.minSpeedToSlice
            ,"minSpeedToKeep": self.minSpeedToKeep
            ,"modStore": self.modStore
        }
        return settings

    # settings.set("minSpeedToSlice", grade=any, shape=any,)
    def set(self, target, value, grade="any", shape="any", speedBumps="any"):       
        if grade=="any":
            for gradeExpand in Mod.grades:
                self.setIterateShape(target, gradeExpand, shape, speedBumps, value)    
        elif type(grade) is list:
            for gradeExpand in grade:
                self.setIterateShape(target, gradeExpand, shape, speedBumps, value)
        else:
            self.setIterateShape(target, grade, shape, speedBumps, value)

    def setIterateShape(self, target, grade, shape, speedBumps, value ):
        if shape=="any":
            for shapeExpand in Mod.shapes:
                self.setIterateSpeedBumps(target, grade, shapeExpand, speedBumps, value)
        elif type(shape) is list:
            for shapeExpand in shape:
                self.setIterateSpeedBumps(target, grade, shapeExpand, speedBumps, value)
        else:
            self.setIterateSpeedBumps(target, grade, shape, speedBumps, value)

    def setIterateSpeedBumps(self, target, grade, shape, speedBumps, value):
        if speedBumps=="any":
            for speedBumpsExpand in range (0,6):
                self.setIterateTheSet(target, grade, shape, speedBumpsExpand, value)
        elif type(speedBumps) is list:
            for speedBumpsExpand in speedBumps:
                self.setIterateTheSet(target, grade, shape, speedBumpsExpand, value)
        else:
            self.setIterateTheSet(target, grade, shape, speedBumps, value)

    def setIterateTheSet(self, target, grade, shape, speedBumps, value):
        if target=="uncoverStatsLimit":
            self.uncoverStatsLimit[grade][shape]=value

        if target=="minInitialSpeed":
            self.minInitialSpeed[grade][shape]=value
        
        if target=="minSpeedToSlice":
            self.minSpeedToSlice[speedBumps][grade][shape]=value
        
        if target=="minSpeedToKeep":
            self.minSpeedToKeep[speedBumps][grade][shape]=value

        


