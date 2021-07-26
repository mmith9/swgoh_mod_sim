from budget import *

base = Budget()

changes = Budget()
base.calculateWeeklyBudget()

changes.applyChange({"credits":-1000})
changes.applyChange({"resistor":-1000})

print(base.getAll())


print (changes.getAll())



print ("weekly credits", base.getCredits(), base.getAll()["shipCredits"])
print ("daily credits", base.getCredits()/7, base.getAll()["shipCredits"]/7)

