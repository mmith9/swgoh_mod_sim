
class Budget:

    def __init__(self):
        pass

        self.credits=0
        self.modEnergy=0
        self.shipCredits=0
        self.slice5Mat={}
        self.slice6Mat={}

        self.slice5Mats=["pin","disk","chip","coil","amplifier","capacitor","modulator"]
        self.slice6Mats=["module","unit","resistor","microprocessor"]

        for mat in self.slice5Mats:
            self.slice5Mat[mat]=0

        for mat in self.slice6Mats:
            self.slice6Mat[mat]=0
            
    def calculateWeeklyBudget(self):
        days=7

        ## mod energy refresh 3x, zero waste
        self.modEnergy+= days * (3 * 120 + 240 + 45)

        ## sim GW
        self.credits+= days * 647200
        self.shipCredits+= days * 139400

        ## GC challenge 2x a week, top crate
        self.credits+=110000*2
        self.shipCredits+=75000*2
        self.slice5Mat["amplifier"]+=6*2
        self.slice5Mat["capacitor"]+=20*2
        self.slice5Mat["modulator"]+=10*2

        self.slice6Mat["module"]+=20*2
        self.slice6Mat["unit"]+=32*2
        self.slice6Mat["resistor"]+=15*2
        self.slice6Mat["microprocessor"]+=6*2

        ## credits challenge 3x a week 2x sim
        self.credits+= 93000 *2 *3

        ## ship credits challenge 3x a week 2x sim
        self.shipCredits+= 190000 *2 *3

        ## TODO
        #### GAC cadence is 4 weeks, week pause
        ## my gac position is usual 11 wins per gac
        ## which means about second top rewards every week plus kyber rewards
        self.credits+= 1000000 /5
        self.slice5Mat["chip"]+= 40
        self.slice5Mat["coil"]+= 35 
        self.slice5Mat["amplifier"]+= 50
        self.slice5Mat["capacitor"]+= 50
        self.slice5Mat["modulator"]+= 20

        #### CONQUEST
        ## assuming top crate on HARD once a month
        self.credits+= 2800000 * days/30
        self.slice5Mat["amplifier"]+= 30 * days/30
        self.slice5Mat["capacitor"]+= 50 * days/30
        self.slice5Mat["modulator"]+= 20 * days/30
        self.slice6Mat["module"]+= 50 * days/30
        self.slice6Mat["unit"]+= 50 * days/30
        self.slice6Mat["resistor"]+= 50 * days/30
        self.slice6Mat["microprocessor"]+= 30 * days/30

        #### EVENTS
        ## credit heist 2020 to present avg is 14.68 days per one
        self.credits+= 5000000 * days / 14.68

        ## smugglers run 2020 to present avg days 10.57
        self.credits+=300000 * 2 * days/10.57
        self.slice5Mat["pin"]+=5 * 2 * days/10.57
        self.slice5Mat["disk"]+=5 * 2 * days/10.57
        self.slice5Mat["chip"]+=5 * 2 * days/10.57
        self.slice5Mat["coil"]+=5 * 2 * days/10.57
        self.slice5Mat["amplifier"]+=5 * 2 * days/10.57
        self.slice5Mat["capacitor"]+=5 * 2 * days/10.57
        self.slice5Mat["modulator"]+=2 * 2 * days/10.57

        ## TODO contraband cargo 2020 to present avg 9.98 days

        ## TODO minor events

        ##### RAIDS
        ## heroic sith raid, top10 spot, 2 times a week (mercs!)
        self.credits+=785000*2
        self.slice5Mat["pin"]+=12*2
        self.slice5Mat["disk"]+=12*2
        self.slice5Mat["chip"]+=12*2
        self.slice5Mat["coil"]+=12*2

        ## Hpit sim each 2 days
        self.credits+= 300000 * days / 2

        ## HAAT sim each 3 days
        self.credits+= 720000 * days / 3
        self.shipCredits+= 182000 * days / 3

        ## Cpit once a week, no pressure
        self.credits+= 900000

    def getAll(self):
        theBudget={
            "credits": self.credits
            ,"shipCredits":self.shipCredits
            ,"modEnergy":self.modEnergy
            
        }

        for mat in self.slice5Mat:
            theBudget[mat]=self.slice5Mat[mat]

        for mat in self.slice6Mat:
            theBudget[mat]=self.slice6Mat[mat]
            
        return theBudget

    def applyChange(self, changes={}):

        for change in changes:
            if change in self.slice5Mats:
                self.slice5Mat[change] += changes[change]
            elif change in self.slice6Mats:
                self.slice6Mat[change] += changes[change]
            elif change=="credits":
                self.credits+= changes[change]
            elif change=="shipCredits":
                self.shipCredits+= changes[change]
            elif change=="modEnergy":
                self.modEnergy+= changes[change]

    def getCredits(self):
        return self.credits

    def getModEnergy(self):
        return self.modEnergy
