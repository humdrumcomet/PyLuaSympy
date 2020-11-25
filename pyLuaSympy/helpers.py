import re
from pathlib import Path
from . import eqandvar
import sympy
from sympy import symbols, latex, sympify, Eq, lambdify, solve
# from sympy.utilities.lambdify import lambdify, implemented_function

# def variablename(var):
    # return [tpl[0] for tpl in filter(lambda x: var is x[1], globals().items())]

def getVandEfromFile(file):
    strToConv = Path(file).read_text()
    varDict, eqtDict = getVandEfromLocal(strToConv)
    eqtPro, varPro= expandAll(eqtDict, varDict)

    # varPro, eqtPro = processVandEtoveDict(varDict, eqtDict)
    return [varPro, eqtPro]

def getVandEfromLocal(strIn):
    varDict = stringToDict(strIn, 'Var')
    eqtDict = stringToDict(strIn, 'Eq')
        
    return [varDict, eqtDict]

def stringToDict(strIn, typeSeek):
    strIn, numComsRemoved = re.subn('\s*#.*\n', '\n', strIn) # remove all comments
    namePat = re.compile('new'+typeSeek+'\s*{\s*(\w*)\s*}\s*{\s*') #patter for find variable or equation names
    names = namePat.finditer(strIn) #get an iterator of all match objects for the above pattern
    newDict = eqandvar.evDict()
    subNamePat = re.compile('\s*(\w+)\s*=\s*\{') #pattern for var or eqt parameter names
    for i in names:
        preprocessDict = {'name':i.group(1)}
        startLoc = i.end(0) # get the endlocation of the var or eq beginning 
        endLoc = startLoc+findBalanced(strIn[startLoc:],'{', '}')
        curLoc = startLoc
        strCur = strIn[curLoc:endLoc]
        while len(strCur)>5:
            subNameMatch = subNamePat.search(strCur)
            subNameVal = subNameMatch.end(0) #curLoc+len(subNameMatch.group(0))
            subNameValEnd = subNameVal+findBalanced(strCur[subNameVal:],'{','}')
            preprocessDict[subNameMatch.group(1)] = strCur[subNameVal:subNameValEnd]
            curLoc = subNameValEnd
            strCur = strCur[curLoc:]

        if typeSeek == 'Var':
            newDict[i.group(1)] = eqandvar.varClass(preprocessDict) # add a dictionary entry for this var or eq
        elif typeSeek == 'Eq':
            newDict[i.group(1)] = eqandvar.eqtClass(preprocessDict) # add a dictionary entry for this var or eq

    return newDict

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
        eqDict[key].eqtExp, eqDict[key].equalExp = equationExpand(eqDict[key], eqDict)
        print('postpop')
        print(eqDict[key].eqtExp, eqDict[key].equalExp)
        eqDict[key].symbsExp = eqDict[key].eqtExp.free_symbols
        eqDict[key].lambd = lambdExpand(eqDict[key],varDict)
        eqDict[key].tex = latexGlsSub(eqDict[key].equal,eqDict, varDict, eqDict[key].texPrintOpts)
        eqDict[key].texExp = latexGlsSub(eqDict[key].equalExp, eqDict, varDict, eqDict[key].texPrintOpts)

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

        eqDict[solveSubStr].eqtExp, eqDict[solveSubStr].equalExp = equationExpand(eqDict[solveSubStr],eqDict)
        solved = solve(eqDict[solveSubStr].equalExp, solveRep)
        solvedStr = str(solved[0])
        solStr = solStr.replace(solStr[i.start(0):solveEnd+1],solvedStr)

    return [solStr, eqtsSolved]


def equationExpand(eqClassItem, eqDict):
    if eqClassItem.eqtExp:
        return [eqClassItem.eqtExp, eqClassItem.equalExp]

    if eqClassItem.solveExpr and not eqClassItem.eqt:
        solvedStr, eqtsSolved = solveExpand(eqClassItem.solveExpr, eqDict)
        eqClassItem.eqt = sympify(solvedStr)
        eqClassItem.equal = Eq(symbols(eqClassItem.name), eqClassItem.eqt)
        eqClassItem.symbs = eqClassItem.eqt.free_symbols
        eqClassItem.eqtsSolved = set(eqtsSolved)
        print(eqClassItem.eqtsSolved)
        print('inop')
        print(eqClassItem.eqt)
        print(eqClassItem.symbs)
        # eqDict[eqClassItem.name] = eqClassItem

    expExprTemp = eqClassItem.eqt
    equalExpTemp = eqClassItem.equal
    for sym in eqClassItem.symbs:
        symStr = str(sym)
        if symStr in eqDict and not symStr in eqClassItem.eqtsSolved:
            if not eqDict[symStr].eqtExp:
                eqDict[symStr].eqtExp, eqDict[symStr].equalExp = equationExpand(eqDict[symStr],eqDict)

            expExprTemp = expExprTemp.subs(sym, eqDict[symStr].eqtExp)
            equalExpTemp = equalExpTemp.subs(sym, eqDict[symStr].eqtExp)

    return [expExprTemp, equalExpTemp]

def lambdExpand(eqClassItem, varDict):
    expExprTemp = eqClassItem.eqtExp
    # for sym in eqDict[key].symbsExp:
        # if sym in varDict:
            # if varDict[sym].value:
                # expExprTemp = expExprTemp.subs(sym, varDict[sym].value)

    lambdRet = lambdify(expExprTemp.free_symbols, expExprTemp, eqClassItem.lambdOpts)
    return lambdRet

def latexGlsSub(exprExp, eqDict, varDict, texOpts):
    texTemp = latex(exprExp, )
    splitEqt = re.split(r'(\w*)', texTemp)
    symsList = []
    for idx, item in enumerate(splitEqt):
        if item in eqDict:
            splitEqt[idx] = '\\gls{'+item+'}'

        if item in varDict:
            splitEqt[idx] = '\\gls{'+item+'}'


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
