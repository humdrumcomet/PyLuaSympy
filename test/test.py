import os
import pyLuaSympy.helpers as lsh

path = os.path.join(os.path.dirname(__file__), './test.yaml')
var,eqt,aux = lsh.yamlLoader(path)
print(var)
print(eqt)
print(aux)
print(eqt.scndEq)

# print(aVar)
# print(scndEq)
t = eqt.scndEq.calc('t', x=1e3)
print(t)
# s = thrdEq.calc('s')
# tex = scndEq.totex('t')
# tex2 = thrdEq.totex('s')
tex3 = eqt['scndEq'].totex()
print(tex3)
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

# **** # """"""""""""""""""""""""""""""""""""""" """""""""""""""""""""""""""""""""""""""
# glossary
# \newglossaryentry{cpp}
# {%
#     name={C++},
#     description={C++ is a programming language that can be used as an object oriented programming language, an imperative programming language, and still provide low-level memory control. Note: All C++ code used in this work is compiled under the C++11 standard}
#  3 }
# **** glossary with plural
# \newglossaryentry{acdc}
# {
#     name={rectifier},
#     description={a \glsentrytext{ac} to \glsentrytext{dc} voltage converter (\glsentrytext{acdc})},
#     plural={rectifiers},
#     descriptionplural={\glsentrytext{ac} to \glsentrytext{dc} voltage converters (\glsentrytext{acdc})}
#   3 }
# **** acronym
# \newglossaryentry{cad}
# {
#     type=\acronymtype,
#     name={CAD},
#     description={computer aided design},
#     first={\glsentrydesc{cad} (\glsentrytext{cad})}
#   3 }
# **** acronym with plural
# \newglossaryentry{cpt}
# {
#     type=\acronymtype,
#     name={CPT},
#     description={coreless planar transformer},
#     first={\glsentrydesc{cpt} (\glsentrytext{cpt})},
#     plural={CPTs},
#     descriptionplural={coreless planar transformers},
#     firstplural={\glsentrydescplural{cpt} (\glsentryplural{cpt})}
#   3 }
# **** acronym with gloss ext
# \newglossaryentry{mfpg}
# {
#     name={\glsentrytext{mfp}},
#     description={\glsentrydesc{mfp} (\glsentrytext{mfp}) is the average distance travelled by particles between interactions}
#   3 }
# \newglossaryentry{mfp}
# {
#     type=\acronymtype,
#     name={MFP},
#     description={mean free path},
#     first={\glsentrydesc{mfp} (\glsentrytext{mfp})\glsadd{mfpg}},
#     see=[Glossary:]{mfpg}
#   3 }
# **** acronym with plural with gloss ext
# \newglossaryentry{cwvmg}
# {
#     name={\glsentrytext{cwvm}},
#     description={\glsentrydesc{cwvm} (\glsentrytext{cwvm}) is a voltage multiplier that can be cascaded to give an output voltage of \SI{n}{\vpp}}
#   3 }
# \newglossaryentry{cwvm}
# {
#     type=\acronymtype,
#     name={CWVM},
#     description={Cockroft-Walton voltage multiplier},
#     first={\glsentrydesc{cwvm} (\glsentrytext{cwvm})\glsadd{cwvmg}},
#     plural={CWVMs},
#     descriptionplural={Cockroft-Walton voltage multipliers},
#     firstplural={\glsentrydescplural{cwvm} (\glsentryplural{cwvm})},
#     see=[Glossary:]{cwvmg}
#   3 }
# **** const
# \newglossaryentry{h}
# {
#     type=constants,
#     name={\ensuremath{h}},
#     description={\mbox{} Planck constant (\SI{6.626070e-34}{\meter\tothe{2}\kilogram\per\second})}
#   3 }
# **** symb
# \newglossaryentry{EB}
# {
#     type=symbols,
#     name={\ensuremath{E_{B}}},
#     description={nuclear binding energy (\si{\electronvolt})}
#   3 }
