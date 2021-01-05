import re
from pathlib import Path
from . import eqandvar

def variablename(var, namespace):
    return [tpl[0] for tpl in filter(lambda x: var is x[1], globals().items())]

def multiVandEfromFile(file, nameSpace=None):
    strToConv = Path(file).read_text()
    newVars = eqandvar.evDict()
    newEqts = eqandvar.evDict()
    multiVandEfromString(strToConv, newVars, newEqts)

    if nameSpace:
        nameSpace.update(newVars)
        nameSpace.update(newEqts)

    return newVars, newEqts

def multiVandEfromString(strIn, varDict, eqtDict):
    strIn, numComsRemoved = re.subn('\s*#.*\n', '\n', strIn) # remove all comments
    namePat = re.compile('\s*(\w*)\s*=\s*nve\(\s*') #patter for find variable or equation names
    names = namePat.finditer(strIn) #get an iterator of all match objects for the above pattern
    subNamePat = re.compile('\s*(\w+)\s*=\s*(.*?),\s*\w*\s*=\s*|\s*(\w+)\s*=\s*(.*?),?\s*$')
    for i in names:
        preprocessDict = {'name':i.group(1)}
        startLoc = i.end(0) # get the endlocation of the var or eq beginning 
        endLoc = startLoc+findBalanced(strIn[startLoc:],'(', ')')
        curLoc = startLoc
        strCur = strIn[curLoc:endLoc]
        while len(strCur)>3:
            subNameMatch = subNamePat.search(strCur)
            key = subNameMatch.group(1) or subNameMatch.group(3)
            val = subNameMatch.group(2) or subNameMatch.group(4)
            preprocessDict[key] = val #strCur[subNameVal:subNameValEnd]
            curLoc = subNameMatch.end(2) #subNameValEnd
            strCur = strCur[curLoc:]

        if 'value' in preprocessDict:
            varDict[i.group(1)] = eqandvar.varClass(preprocessDict) # add a dictionary entry for this var or eq
        elif 'expr' in preprocessDict:
            eqtDict[i.group(1)] = eqandvar.eqtClass(varDict,eqtDict,preprocessDict) # add a dictionary entry for this var or eq


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
