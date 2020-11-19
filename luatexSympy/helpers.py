import re
from pathlib import Path

# def variablename(var):
    # return [tpl[0] for tpl in filter(lambda x: var is x[1], globals().items())]

def getVandEfromFile(file):
    strToConv = Path(file).read_text()
    varDict, eqtDict = getVandEfromLocal(strToConv)
    return [varDict, eqtDict]

def getVandEfromLocal(strIn):
    varDict = stringToDict(strIn, 'Var')
    eqtDict = stringToDict(strIn, 'Eq')
        
    return [varDict, eqtDict]

def stringToDict(strIn, typeSeek):
    strIn, numComsRemoved = re.subn('\s*#.*\n', '\n', strIn) # remove all comments
    namePat = re.compile('new'+typeSeek+'\s*{\s*(\w*)\s*}\s*{\s*') #patter for find variable or equation names
    names = namePat.finditer(strIn) #get an iterator of all match objects for the above pattern
    newDict = {}
    subNamePat = re.compile('\s*(\w+)\s*=\s*\{') #pattern for var or eqt parameter names
    for i in names:
        newDict[i.group(1)] = {} # add a dictionary entry for this var or eq
        startLoc = i.end(0) # get the endlocation of the var or eq beginning 
        endLoc = startLoc+findBalanced(strIn[startLoc:],'{', '}')
        curLoc = startLoc
        strCur = strIn[curLoc:endLoc]
        while len(strCur)>5:
            subNameMatch = subNamePat.search(strCur)
            subNameVal = subNameMatch.end(0) #curLoc+len(subNameMatch.group(0))
            subNameValEnd = subNameVal+findBalanced(strCur[subNameVal:],'{','}')
            newDict[i.group(1)][subNameMatch.group(1)] = strCur[subNameVal:subNameValEnd]
            curLoc = subNameValEnd
            strCur = strCur[curLoc:]
    
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
