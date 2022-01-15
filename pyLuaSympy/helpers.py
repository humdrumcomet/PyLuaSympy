import os
import re
import yaml
from pathlib import Path
from . import eqandvar

def yamlLoader(filePath):
    # print(filePath)
    # filePath = os.path.join(os.path.dirname(__file__), filePath)
    # print(filePath)
    with open(Path(filePath), 'r') as file:
        yamlDict = yaml.safe_load(file)

    return list(yamlDict.values())


def eqandVarFromYaml(filePath, namespace=None):
    yamlDict = yamlLoader(filePath)
    newVars = eqandvar.evDict()
    newEqts = eqandvar.evDict()
    newAux = {}

    for k, v in mVandE.items():
        if k == 'variables':
            for k2, preProcDict in v.items():
                newVars[k2] = eqandvar.varClass(k2,preProcDict)
        elif k == 'equations':
            for k2, preProcDict in v.items():
                newEqts[k2] = eqandvar.eqtClass(k2,newVars,newEqts,preProcDict)

    return newVars, newEqts, newAux

def glossFromYaml(filePath):
    yamlDict = yamlLoader(filePath)

def glossBuilder(*args):
    pass

def fromMixYaml(inputFile):
    pass

def fromEqtYaml(inputFile, symLib):
    pass

def fromSymYaml(inputFile):
    pass

def fromAuxYaml(inputFile):
    pass

def fromMixDict(inputDict):
    pass

def fromEqtDict(inputDict, symLib):
    pass

def fromSymDict(inputDict):
    pass

def fromAuxDict(inputDict):
    pass

# function newGl(kind, name, inputStr)
#     --Order is:
#     --callName
#     --type -> gls, acr (can add ext, pl), cst, sym
#     --name
#     --description
#     --plural form
#     --plural description
#     --extended description
#     local typeCall = {
#         cst = [[type=constants, ]],
#         sym = [[type=symbols, ]],
#         acr = [[type=\acronymtype, ]],
#         gls = ''
#     }
#     local acrG = ''
#     local acrPl = ''
#     local glsAdd = ''
#     if type(inputStr)=='string' then
#         inputs = {kind = kind, name = name}
#         trimmed = string.gsub(inputStr, '^%s*(.-)%s*$', '%1')
#         modStr = trimmed..[[,]]
#         for key, value in string.gmatch(modStr, '(%w-)%s*=%s*(%b{}),') do
#             inputs[key] = string.gsub(value, '^{(.-)}$', '%1')
#         end
#         if inputs.descriptionExt then
#             acrG = [[see=[Glossary:]{]]..inputs.name..[[g}} \newglossaryentry{]]..
#                     inputs.name..[[g}{name={\glsentrytext{]]..
#                     inputs.name..[[}}, description={]]..inputs.descriptionExt..[[}]]

#             glsAdd = [[\glsadd{]]..inputs.name..[[g}]]
#         end
#         if inputs.displayPl then
#             acrPl = [[plural={]]..inputs.displayPl..[[}, descriptionplural={]]..
#                     inputs.descriptionPl..[[}, firstplural={\glsentrydescplural{]]..
#                     inputs.name..[[} (\glsentryplural{]]..inputs.name..[[})]]..glsAdd..[[},]]
#         end
#     else
#         inputs = inputStr
#         print('----in gls')
#         print(inputs.kind)
#     end

#     callBuild = {
#         base = function(inputs) return [[\newglossaryentry{]]..inputs.name..[[}{]]..
#                     typeCall[inputs.kind]..[[name={]]..
#                     inputs.display..[[}, description={]]..
#                     inputs.description..[[},]] end,

#         cst = function(inputs) return callBuild.base(inputs)..[[}]] end,
#         sym = function(inputs) return callBuild.base(inputs)..[[}]] end,
#         gls = function(inputs) return callBuild.base(inputs)..[[}]] end,
#         acr = function(inputs) return callBuild.base(inputs)..[[first={\glsentrydesc{]]..
#                 inputs.name..[[} (\glsentrytext{]]..inputs.name..[[})]]..glsAdd..[[}, ]]..
#                 acrPl..acrG..[[}]] end,
#     }
#     texString = callBuild[inputs.kind](inputs)
#     tex.sprint(texString..' ')

# end
