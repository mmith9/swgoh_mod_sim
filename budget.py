
class Budget:

    def __init__(self):
        
        self.testlevel=0
        
        self.slice5Mats=["pin","disk","chip","coil","amplifier","capacitor","modulator"]
        self.slice6Mats=["module","unit","resistor","microprocessor"]

        self.resources={
        "credits":0
        ,"modEnergy":0
        ,"normalEnergy":0
        ,"shipEnergy":0
        ,"cantinaEnergy":0
        ,"shipCredits":0
        }

        for mat in self.slice5Mats:
            self.resources[mat]=0

        for mat in self.slice6Mats:
            self.resources[mat]=0
            
    def calculateWeeklyBudget(self):
        days=7

        ## mod energy refresh 3x, zero waste
        self.resources["modEnergy"]+= days * (3*120 + 240 + 45)
        self.resources["normalEnergy"]+= days * (3*120 + 240 + 3*45)
        self.resources["shipEnergy"]+= days * (3*120 + 240 +45)
        self.resources["cantinaEnergy"]+= days * (3*120 +120 +45)
        
        # node farming
        # Between 80 and 115 credits/fleet energy and between 23 and 33 ship credits/fleet energy on fleet nodes.
        # g12+ material is 115+33 for t5, 98+32 for t4, 96+29 for t3, 88+29 for t2
        self.resources["credits"]+= self.resources["shipEnergy"] * 100
        self.resources["shipCredits"]+= self.resources["shipEnergy"] * 31

        # normal energy nodes
        # Between 31.67 credits/energy and 138 credits/energy and between 0 and 50 ship credits/energy on normal energy nodes.
        # ex: bokatan node is 69.375 per energy darktrooper 27.5, mecho 72 plus 50 ship, hunter 61.25, bayonet node 138 plus 50 ship
        self.resources["credits"]+= self.resources["normalEnergy"] * 50 #just to add something i guess
        self.resources["shipCredits"]+= self.resources["normalEnergy"] * 50 /2 # another out-of-ass-estimate

        # cantina relic materials farming 500 credits 100 shipcredits per 1 energy
        self.resources["credits"]+= self.resources["cantinaEnergy"] * 500
        self.resources["shipCredits"]+= self.resources["cantinaEnergy"] * 100

        # mod energy gains are accounted for in mod simulator

        # Daily login rewards average 20.33k credits per day.
        self.resources["credits"]+= 20330 *days
        #Daily activity rewards 36.25k credits per day, 25k ship credits per day. 
        self.resources["credits"]+= 36250 *days
        self.resources["shipCredits"]+= 25000 *days
        #Don't know the chances for the daily rewards box which can bring up to 500k. I'd say 50k is a good assumption.
        self.resources["credits"]+= 50000 *days

        ## squad arena, assuming first place
        self.resources["credits"]+= 50000 * days
        ## ship arena, assuming first place
        self.resources["shipCredits"]+= 200000 * days

        ## sim GW
        self.resources["credits"]+= days * 647200
        self.resources["shipCredits"]+= days * 139400

        ## GC challenge 2x a week, top crate
        self.resources["credits"]+=110000*2
        self.resources["shipCredits"]+=75000*2
        self.resources["amplifier"]+=6*2
        self.resources["capacitor"]+=20*2
        self.resources["modulator"]+=10*2

        self.resources["module"]+=20*2
        self.resources["unit"]+=32*2
        self.resources["resistor"]+=15*2
        self.resources["microprocessor"]+=6*2

        ## credits challenge 3x a week 3x sim
        self.resources["credits"]+= 105000 *3 *3

        ## ship credits challenge 3x a week 2x sim (155-290k per sim)
        self.resources["shipCredits"]+= 190000 *2 *3

        #### GAC cadence is 4 weeks, week pause
        ## my gac position is usual 11 wins per gac
        ## which means about second top rewards every week plus kyber rewards
        self.resources["credits"]+= 1000000 /5
        self.resources["chip"]+= 40
        self.resources["coil"]+= 35 
        self.resources["amplifier"]+= 50
        self.resources["capacitor"]+= 50
        self.resources["modulator"]+= 20
        ### plus full board clear 90k per ship, 100k per squad in 5v5, 70k per squad in 3v3, 3 times a week
        ## 10x 100k squad or 14x 70k avg is 990k , 2x90k ship
        self.resources["credits"]+= (990000+180000) *3 *4/5

        #### CONQUEST
        ## assuming top crate on HARD once a month
        self.resources["credits"]+= 2800000 * days/30
        self.resources["amplifier"]+= 30 * days/30
        self.resources["capacitor"]+= 50 * days/30
        self.resources["modulator"]+= 20 * days/30
        self.resources["module"]+= 50 * days/30
        self.resources["unit"]+= 50 * days/30
        self.resources["resistor"]+= 50 * days/30
        self.resources["microprocessor"]+= 30 * days/30

        ## TW assuming top gp bracket, win is 725k loss is 175k
        # one win, one loss, 1 tw per week
        self.resources["credits"]+= (725000 + 175000)/2

        #### EVENTS
        ## credit heist 2020 to present avg is 14.68 days per one
        self.resources["credits"]+= 5000000 * days / 14.68

        ## smugglers run 2020 to present avg days 10.57
        self.resources["credits"]+=300000 * 2 * days/10.57
        self.resources["pin"]+=5 * 2 * days/10.57
        self.resources["disk"]+=5 * 2 * days/10.57
        self.resources["chip"]+=5 * 2 * days/10.57
        self.resources["coil"]+=5 * 2 * days/10.57
        self.resources["amplifier"]+=5 * 2 * days/10.57
        self.resources["capacitor"]+=5 * 2 * days/10.57
        self.resources["modulator"]+=2 * 2 * days/10.57

        ## top tier contraband cargo 2020 to present avg 9.98 days
        self.resources["shipCredits"]+= 100000 *2 *days/9.98

        ## omega battles, each event is 112500 credits. on avg each reappears after 30.38 days , 7 different omega battles
        self.resources["credits"]+= 112500 *7 *days/30.38

        ## endor escalation avg 29.09 days
        self.resources["credits"]+= 150000 *days/29.09
        #galactic bounties I avg 47.68 days
        self.resources["credits"]+= 500000 *2 *days/47.68
        #galactic bounties II avg 49.72
        self.resources["credits"]+= 100000 *2 *days/49.72

        ## ASSAULT BATTLES, only few give credits and only 3 first tiers
        # forest moon avg 30.9 days
        self.resources["credits"]+= (150000 + 200000 + 250000) * 7/30.9
        # places of power avg 32.65 days
        self.resources["shipCredits"]+= (200000 *3) * 7/32.65
        # secrets and shadows avg 28.38 days
        self.resources["credits"]+= (200000 *3) *7/28.38

        ### MYTHIC EVENTS 
        # 3 tiers each, 5 different events. avg 73.96 on bundled raids
        self.resources["credits"]+= (185000 + 185000 +360000) *5 *days/73.96
                
        ### FLEET MASTERY events #TODO
        # executrix home1 endurance 30k ship credits each avg 28.49 days
        # nothing for finalizer and raddus
        self.resources["shipCredits"]+= 30000 *3 *days/28.49

        ##### RAIDS
        ## heroic sith raid, top10 spot, 2 times a week (mercs!)
        self.resources["credits"]+=785000*2
        self.resources["pin"]+=12*2
        self.resources["disk"]+=12*2
        self.resources["chip"]+=12*2
        self.resources["coil"]+=12*2

        ## Hpit sim each 2 days
        self.resources["credits"]+= 300000 * days / 2

        ## HAAT sim each 3 days
        self.resources["credits"]+= 720000 * days / 3
        self.resources["shipCredits"]+= 182000 * days / 3

        ## Cpit once a week, no pressure
        self.resources["credits"]+= 900000

    def getAll(self):          
        return self.resources

    def getEssential(self):
        essential={}
        for mat in ["credits", "shipCredits", "modEnergy", "amplifier", "capacitor", "module", "unit", "resistor", "microprocessor"]:
            essential[mat]=self.resources[mat]
        return essential

    def applyChange(self, changes={}):

        for change in changes:
            if change in self.resources:
                self.resources[change] += changes[change]
            else:
                pass
                #TODO

    def set(self, changes={}):
        for change in changes:
            if change in self.resources:
                self.resources[change] = changes[change]
            else:
                pass
                #TODO

    def getCredits(self):
        return self.resources["credits"]

    def getModEnergy(self):
        return self.resources["modEnergy"]

    def get(self, getWhat):
        if getWhat in self.resources:
            return self.resources[getWhat]

        else:
            #TODO
            assert(False)

    def compareToBudget(self, otherBudget, multiplier=1 ):
        budget1=self.getAll()
        budget2=otherBudget.getAll()

        difference={}

        for resource in budget1:
            diffMinus=budget1[resource]-budget2[resource]*multiplier
            if budget1[resource]==0:
                diffPercent="div0"
            else:
                diffPercent=(100 * budget2[resource] * multiplier) / budget1[resource]
            
            difference[resource]= [diffMinus, diffPercent]
        
        return difference

    def convert4BaseSlicingMatsToEnergy(self):       
        matsToConvert=["pin", "disk", "chip", "coil"]
        matsTotal=0
        for mat in matsToConvert:
            matsTotal+=self.get(mat)
            self.applyChange({mat: -self.get(mat)})  #zero em all
        self.applyChange({"credits": -1000*matsTotal, "modEnergy": 10*matsTotal})

        if self.testlevel>3:
            print("mats converted",matsTotal)

    def reverseCosts(self):
        for mat in self.resources:
            self.resources[mat]*= -1

    def addBudget(self, budgetToAdd, multiplier=1):
        for what in self.resources:
            self.resources[what]+= budgetToAdd.resources[what] *multiplier
    
    def canAfford(self, budgetToFit):
        deficit={}

        for what in self.resources:
            if self.resources[what]-budgetToFit.resources[what] <0:
                deficit[what]=self.resources[what]-budgetToFit.resources[what]

        return deficit

    def energyToMaterial(self, mat, amount):
        #
        # energy conversion ratios amp and cap one= 14/1.2 energy
        # 

        if mat in ["amplifier", "capacitor"]:
            if self.resources["modEnergy"]> amount*14/1.2 :
                self.resources["modEnergy"] -= amount*14/1.2
                self.resources[mat]+= amount
                self.resources["credits"]+= amount*1400/1.2
                return True
            else:
                return False

        else:
            assert(False)
            
            pass
            #TODO