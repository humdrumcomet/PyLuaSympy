import os
import pyLuaSympy.helpers as lsh

path = os.path.join(os.path.dirname(__file__), './test.yaml')
var, eqt = lsh.yamlLoader(path)

# print(aVar)
# print(scndEq)
t = scndEq.calc('t', x=1e3)
s = thrdEq.calc('s')
tex = scndEq.totex('t')
tex2 = thrdEq.totex('s')
tex3 = scndEq.totex()
print(tex[0])
print(tex[1][:-1])
print(tex[1][-1])
# print(tex2[0])
# print(tex2[1])
# print(tex3[0])
# print(tex3[1])
# print(
# print(t)
# print(eqt.scndEq.lambd(x=4, aVar=2, c=var.c.val, anotherVar=var.anotherVar.val))
# print(eqt.scndEq.eqt)
# print(eqt.scndEq.eqtExp)
# print(scndEq.finTex)
# print(scndEq.interTex)
# print(thrdEq.initTex)
# print(thrdEq.finTex)
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
