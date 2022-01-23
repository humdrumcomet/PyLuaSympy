import os
import pyLuaSympy.helpers as lsh

path = os.path.join(os.path.dirname(__file__), './test.yaml')
var, eqt, aux = lsh.yamlLoader(path)
# glsString =
a = 12
print(lsh.toGlossHeader(aux, var, eqt))
print(lsh.equationOut(eqt, 'scndEq', 0, 'all', 'hbarfull'))
print(lsh.equationOut(eqt, 'hbart', 0, 'inline'))
print(lsh.equationOut(eqt, 'hbart'))
print(lsh.printValue('c', var))
print(lsh.printValue(a))
print(lsh.printValue(a, symbol='\\alpha'))
print(lsh.printValue(a, symbol='\\alpha', units='\\gram'))

t = eqt.scdnEg.lambd(x=4, aVar=2, )

# printValue(name, inDict=locals(), decimalPlaces=3, units='', symbol=True): #val, name, decimalPlaces=3, units=True):
# print(var)
# print('')
# print(eqt)
# print('')
# print(aux)
# print('')
# print(eqt.scndEq)

# # print(aVar)
# # print(scndEq)
# t = eqt.scndEq.calc('t', x=1e3)
# print(t)
# # s = thrdEq.calc('s')
# # tex = scndEq.totex('t')
# # tex2 = thrdEq.totex('s')
# tex3 = eqt['scndEq'].totex()
# print(tex3)
# print(glsString)
# print(tex[0])
# print(tex[1][:-1])
# print(tex[1][-1])
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
