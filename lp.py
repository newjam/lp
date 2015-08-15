from pulp import *

prob = LpProblem("Maximize Village Economy", LpMaximize)

houseInFood   = LpVariable("houseInFood", 0, 10)
houseOutLabor = LpVariable("houseOutLabor", 0, 10)

# house outputs as much labor as there is available food.
prob += houseOutLabor == houseInFood

mineInLabor   = LpVariable("mineInLabor", 0, 5)
mineOutOre    = LpVariable("mineOutOre", 0, 5)

# ore doesn't mine itself!
prob += mineOutOre == mineInLabor

farmInTools   = LpVariable("farmInTools", 0, 5)
farmInLabor   = LpVariable("farmInLabor", 0, 5)
farmOutFood   = LpVariable("farmOutFood", 0, 10)

# tools can't work themselves!
prob += farmInTools == farmInLabor

# food is created by farmers and tools
prob += farmOutFood == farmInTools + farmInLabor

factoryInOre    = LpVariable("factoryInOre" , 0, 5)
factoryInLabor  = LpVariable("factoryInLabor" , 0, 5)
factoryOutTools = LpVariable("factoryOutTools", 0, 10)

# tools are created by workers.
prob += factoryInOre == factoryInLabor
prob += factoryOutTools == factoryInLabor + factoryInOre

# conserve labor
prob += factoryInLabor + farmInLabor + mineInLabor == houseOutLabor

# conserve tools
prob += farmInTools == factoryOutTools

# conserve ore
prob += mineOutOre == factoryInOre

# conserve food
prob += houseInFood == farmOutFood

# maximize total output of everything.
prob += farmOutFood + houseOutLabor + factoryOutTools + mineOutOre

status = prob.solve(GLPK())
print LpStatus[status]

# display results
print 'House:', value(houseInFood), 'food' , '=>', value(houseOutLabor), 'labor'
print 'Mine:', value(mineInLabor), 'labor', '=>', value(mineOutOre), 'ore'
print 'Factory:', value(factoryInLabor), 'labor', '+', value(factoryInOre), 'ore', '=>', value(factoryOutTools), 'tools'
print 'Farm:', value(farmInLabor), 'labor', '+', value(farmInTools), 'tools', '=>', value(farmOutFood), 'food'
