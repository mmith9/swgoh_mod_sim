from budget import *

base = Budget()

changes = Budget()
base.calculateWeeklyBudget()

changes.applyChange({"credits":-1000})
changes.applyChange({"resistor":-1000})

print(base.getAll())


print (changes.getAll())



print ("half weekly credits", base.getCredits() /2 , base.getAll()["shipCredits"]/2)

#print ("daily credits", base.getCredits()/7, base.getAll()["shipCredits"]/7)

