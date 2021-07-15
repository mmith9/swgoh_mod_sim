from warnings import resetwarnings


class Resources:

    def __init__(self,mats,credits,energy):
        self.resources={"credits":credits,"mats":mats,"energy":energy}
        
    def add(self,change):
        for what in change:
            self.resources[what]+=change[what]

    def substract(self,change):
        for what in change:
            self.resources[what]-=change[what]

    def rollForMats(self):
        self.resources["energy"]-=12
        self.resources["credits"]+=1200
        self.resources["mats"]+=1.2

    def getCredits(self):
        return self.resources["credits"]

    def getMats(self):
        return self.resources["mats"]

    def getEnergy(self):
        return self.resources["energy"]
        