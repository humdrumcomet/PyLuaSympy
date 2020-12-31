import pyLuaSympy.helpers as lsh

var, eqt = lsh.getVandEfromFile('./equations.py', globals())
# print(var)
# print(eqt)

print(aVar)
print(scndEq)
# print(eqt.scndEq.lambd(x=4, aVar=2, c=var.c.val, anotherVar=var.anotherVar.val))
# print(eqt.scndEq.eqt)
# print(eqt.scndEq.eqtExp)
print(scndEq.finTex)
print(scndEq.interTex)
print(thrdEq.initTex)
print(thrdEq.finTex)
# print(frthEq.finTex)
# print(ffthEq.finTex)

# qch = vne.add(
    # value = 5, 
    # eqt = aVar**2,
    # display = r'\alpha',
    # units = \hertz,
    # description = a different variable,
    # glsType
    # ensureMath
    # lambdifyOpts
    # specialExprOpts
# )
# qch.calc()
