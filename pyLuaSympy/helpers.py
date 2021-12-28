import re
import yaml
from pathlib import Path
from . import eqandvar

def yamlLoader(filePath, namespace=None):
    with open(Path(filePath), 'r') as file:
        mVandE = yaml.safe_load(file)

    newVars = eqandvar.evDict()
    newEqts = eqandvar.evDict()
    print(mVandE)
    # return newVars, newEqts

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


