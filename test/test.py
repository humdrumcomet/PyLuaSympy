import pyLuaSympy.helpers as lsh

var, eqt = lsh.getVandEfromFile('./equations.py')
# print(var)
# print(eqt)

print(eqt.scndEq.lambd(x=4, aVar=2, c=var.c.val, anotherVar=var.anotherVar.val))
# print(eqt.scndEq.eqt)
# print(eqt.scndEq.eqtExp)
print(eqt.scndEq.tex)
print(eqt.scndEq.texExp)
print(eqt.thrdEq.texExp)
