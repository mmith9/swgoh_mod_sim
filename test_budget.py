from budget import *

base = Budget()

changes = Budget()
base.calculateWeeklyBudget()

changes.applyChange({"credits":-1000})
changes.applyChange({"resistor":-1000})

print(base.getAll())


print (changes.getAll())



