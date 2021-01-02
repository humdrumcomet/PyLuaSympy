import re
from pathlib import Path
from . import eqandvar
import sympy
from sympy import symbols, latex, sympify, Eq, lambdify, solve
# from sympy.utilities.lambdify import lambdify, implemented_function

def variablename(var):
    print(var.__name__)
    print(tpl for tpl in filter(lambda x: var is x[1], globals().items()))
    return [tpl[0] for tpl in filter(lambda x: var is x[1], globals().items())]

def getVandEfromFile(file, nameSpace=globals()):
    strToConv = Path(file).read_text()
    varDict, eqtDict = getVandEfromLocal(strToConv)
    eqtPro, varPro= expandAll(eqtDict, varDict)
    nameSpace.update(eqtPro)
    nameSpace.update(varPro)
    return [varPro, eqtPro]

def getVandEfromLocal(strIn):
    varDict, eqtDict = stringToDict(strIn)
        
    return [varDict, eqtDict]

def stringToDict(strIn):
    strIn, numComsRemoved = re.subn('\s*#.*\n', '\n', strIn) # remove all comments
    namePat = re.compile('\s*(\w*)\s*=\s*nve\(\s*') #patter for find variable or equation names
    names = namePat.finditer(strIn) #get an iterator of all match objects for the above pattern
    newEqDict = eqandvar.evDict()
    newVarDict = eqandvar.evDict()
    subNamePat = re.compile('\s*(\w+)\s*=\s*(.*?),\s*\w*\s*=\s*|\s*(\w+)\s*=\s*(.*?),?\s*$')
    for i in names:
        preprocessDict = {'name':i.group(1)}
        startLoc = i.end(0) # get the endlocation of the var or eq beginning 
        endLoc = startLoc+findBalanced(strIn[startLoc:],'(', ')')
        curLoc = startLoc
        strCur = strIn[curLoc:endLoc]
        print(i.group(1))
        while len(strCur)>3:
            subNameMatch = subNamePat.search(strCur)
            # print('-----in------')
            key = subNameMatch.group(1) or subNameMatch.group(3)
            val = subNameMatch.group(2) or subNameMatch.group(4)
            # print(key)
            # print(val)
            # print('---------------')
            preprocessDict[key] = val #strCur[subNameVal:subNameValEnd]
            curLoc = subNameMatch.end(2) #subNameValEnd
            strCur = strCur[curLoc:]

        if 'expr' in preprocessDict:
            newEqDict[i.group(1)] = eqandvar.eqtClass(preprocessDict) # add a dictionary entry for this var or eq
        elif 'value' in preprocessDict:
            newVarDict[i.group(1)] = eqandvar.varClass(preprocessDict) # add a dictionary entry for this var or eq

    return [newVarDict, newEqDict]

def findBalanced(strIn, bO, bC): # find the balanced bracket (or similar) b0 and bC
    openBr = 1
    loc = 1 #start from 1 and assume that a lone instance of b0 has already passed (for while loop)
    while openBr:
        if strIn[loc] == bO:
            openBr = openBr+1
        elif strIn[loc] == bC:
            openBr = openBr-1

        loc = loc+1

    loc = loc-1
    return loc

def expandAll(eqDict, varDict):
    for key in eqDict:
        equationExpand(eqDict[key], eqDict)
        # print('postpop')
        eqDict[key].initLam, eqDict[key].finLam = lambdExpand(eqDict[key],varDict)
        eqDict[key].initTex = latexGlsSub(eqDict[key].initEqual,eqDict, varDict, eqDict[key].texPrintOpts)
        eqDict[key].interTex = latexGlsSub(eqDict[key].interEqual, eqDict, varDict, eqDict[key].texPrintOpts)
        eqDict[key].finTex = latexGlsSub(eqDict[key].finEqual, eqDict, varDict, eqDict[key].texPrintOpts)

    return [eqDict, varDict]

def solveExpand(solStr, eqDict):
    solvePat = re.compile('solve\(')
    solves = solvePat.finditer(solStr)
    eqtsSolved = []
    for i in solves:
        solveStart = i.end(0)
        solveEnd = i.end(0)+findBalanced(solStr[i.end(0):], '(', ')')
        solveFullSub = solStr[solveStart:solveEnd]
        endexp = i.end(0)+solveFullSub.find(',')
        solveSubStr = solStr[solveStart:endexp]
        eqtsSolved.append(solveSubStr)
        solveRep, comsRemoved = re.subn(',\s*', '', solStr[endexp:solveEnd])
        if 'solve' in solveSubStr:
            solveSubStr = solveExpand(solveSubStr, eqDict)

        if not eqDict[solveSubStr].finEqt:
            equationExpand(eqDict[solveSubStr],eqDict)

        solved = solve(eqDict[solveSubStr].finEqual, solveRep)
        solvedStr = str(solved[0])
        solStr = solStr.replace(solStr[i.start(0):solveEnd+1],solvedStr)

    return [solStr, eqtsSolved, solveRep]


def equationExpand(eqClassItem, eqDict):
    if eqClassItem.finEqt:
        return None

    if 'solve' in eqClassItem.initExpr:
        solvedStr, eqtsSolved, newDisplay = solveExpand(eqClassItem.initExpr, eqDict)
        # print('printer')
        # print(solvedStr)
        # print(newDisplay)
        eqClassItem.interExpr = solvedStr
        eqClassItem.initEqt = sympify(solvedStr)
        eqClassItem.initEqual = Eq(symbols(newDisplay), eqClassItem.initEqt)
        eqClassItem.eqtsSolved = set(eqtsSolved)
    else:
        # print(eqClassItem.initExpr)
        eqClassItem.initEqt = sympify(eqClassItem.initExpr)
        eqClassItem.initEqual = Eq(symbols(eqClassItem.name), eqClassItem.initEqt)

    eqClassItem.initSymbs = eqClassItem.initEqt.free_symbols
    exprTemp = eqClassItem.initEqt
    for sym in eqClassItem.initSymbs:
        symStr = str(sym)
        if symStr in eqDict and not symStr in eqClassItem.eqtsSolved:
            if not eqDict[symStr].finEqt:
                equationExpand(eqDict[symStr],eqDict)

            exprTemp = exprTemp.subs(sym, eqDict[symStr].finEqt)

    eqClassItem.interEqt = exprTemp
    eqClassItem.interEqual = Eq(symbols(eqClassItem.name), exprTemp)
    eqClassItem.interEqt = exprTemp.free_symbols
    eqClassItem.finEqt = exprTemp.doit()
    eqClassItem.finEqual = Eq(symbols(eqClassItem.name), exprTemp.doit())
    eqClassItem.finSymbs = exprTemp.doit().free_symbols

    return None

def lambdExpand(eqClassItem, varDict):
    exprTempFin = eqClassItem.finEqt
    exprTempInit = eqClassItem.initEqt.doit()
    # for sym in eqDict[key].symbsExp:
        # if sym in varDict:
            # if varDict[sym].value:
                # expExprTemp = expExprTemp.subs(sym, varDict[sym].value)

    lambdRetInit = lambdify(exprTempInit.free_symbols, exprTempInit, eqClassItem.lambdOpts)
    lambdRetFin = lambdify(exprTempFin.free_symbols, exprTempFin, eqClassItem.lambdOpts)
    return lambdRetInit, lambdRetFin

def latexGlsSub(exprExp, eqDict, varDict, texOpts):
    texTemp = latex(exprExp, )
    if 'Integral' in str(exprExp):
        texTemp, numIntChangedRemoved = re.subn(',\s*d', r',\\mathrm{d}', texTemp)

    splitEqt = re.split(r'(\w*)', texTemp)
    symsList = []
    for idx, item in enumerate(splitEqt):
        if item in eqDict:
            if eqDict[item].description:
                splitEqt[idx] = '\\gls{'+item+'}'
            elif eqDict[item].display and eqDict[item].ensureMath:
                # print(eqDict[item].display)
                splitEqt[idx] = '\\ensuremath{'+eqDict[item].display+'}'
            elif eqDict[item].display and not eqDict[item].ensureMath:
                splitEqt[idx] = eqDict[item].display

        if item in varDict:
            if varDict[item].description:
                splitEqt[idx] = '\\gls{'+item+'}'
            elif varDict[item].display and varDict[item].ensureMath:
                # print(varDict[item].display)
                splitEqt[idx] = '\\ensuremath{'+varDict[item].display+'}'
            elif varDict[item].display and not varDict[item].ensureMath:
                splitEqt[idx] = varDict[item].display


    texTemp = ''.join(splitEqt)
    return texTemp

def getExpr(eqt, symsDict):
    splitEqt = re.split(r'(\w*)', eqt)
    symsList = []
    for idx, item in enumerate(splitEqt):
        if item in symsDict.dict:
            symsList.append(symsDict.dict[item].var)
            splitEqt[idx] = 'Symbol(r\''+str(symsDict.dict[item].var)+'\')'

    exprStr = ''.join(splitEqt)
    expression = parExp(exprStr)
    texExpr = latex(expression)
    lambdaExpr = lambdify(symsList, expression, 'numpy')
    return [expression, texExpr, lambdaExpr, symsList]
