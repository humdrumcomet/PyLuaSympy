import re
from . import helpers
from sympy import symbols, latex, sympify, Eq, lambdify, Function, solve
from sympy.parsing.sympy_parser import parse_expr as parExp


class evDict(dict):
    def __getattr__(self,item):
        return self[item]

    def nve(self, **kwargs):
        nameSpace = kwargs.pop('nameSpace', None)
        varDict = kwargs.pop('varDict', None)
        eqtDict = kwargs.pop('eqtDict', None)
        if varDict:
            eqtDict = self
        elif eqtDict:
            varDict = self

        for k,v in kwargs.items():
            if 'value' in v:
                self[k] = varClass(v)
            elif 'expr' in v:
                self[k] = eqtClass(varDict, eqtDict, v)

            if nameSpace:
                nameSpace[k] = self[k]


class evClass:
    def __init__(self, dfp):
        self.name = dfp.get('name')
        self.symbol = dfp.get('symbol')
        self.units = dfp.get('units')
        self.glsType = dfp.get('glsType') or 'sym'
        self.description = dfp.get('description')
        self.ensureMath = (dfp.get('ensureMath') or 'true').lower() == 'true'

class varClass(evClass):
    def __init__(self, dfp):
        evClass.__init__(self, dfp)
        self.val = dfp.get('value') and float(dfp.get('value'))

class eqtClass(evClass):
    def __init__(self, vDict, eDict, dfp):
        evClass.__init__(self, dfp)
        self.eDict = eDict
        self.vDict = vDict
        self.expr = dfp.get('expr')
        self.lambdOpts = dfp.get('lambdifyOpts') or 'numpy'
        self.texPrintOpts = dfp.get('texPrintOpts') and ', ' + dfp.get('texPrintOpts')
        self.specialExprOpts = ''
        self.eqtType = 'equation'
        self.computeList = {}

    def calc(self, *args, **kwargs):
        name = kwargs.pop('name', None) or (args and args[0]) or str(len(self.computeList))
        self.computeList[name] = kwargs
        eqt, steps = self.expand(**kwargs)
        return self.solution(eqt, **kwargs)

    def totex(self, *args, **kwargs):
        name = kwargs.pop('name', None) or (args and args[0])
        optsDict = self.computeList.get(name) or {}
        optsDict.update(kwargs)
        eqt, steps = self.expand(**optsDict)
        # print(len(steps))
        for idx, item in enumerate(steps):
            steps[idx] = self.latexGlsSub(item, **optsDict)

        steps.append(self.latexGlsSub(self.solutionShowSub(latex(Eq(symbols(self.name), eqt)))))
        steps.append(self.latexGlsSub(self.solution(eqt, **optsDict)))
        eqt = self.latexGlsSub(eqt, **optsDict)
        steps = list(dict.fromkeys(steps))

        # print('------print')
        # for i in steps:
            # print(i)

        # print('------printClean')
        # print(eqt)
        # for i in steps:
            # print(i)
        return [eqt, steps]


    def expand(self, **kwargs):
        varDict = kwargs.pop('varDict', None) or self.vDict
        eqtDict = kwargs.pop('eqtDict', None) or self.eDict
        # kwargs['solved'] = kwargs.get('solved') or []
        kwargs['noExp'] = kwargs.get('noExp') or []
        steps = []
        if 'solve' in self.expr:
            pass
            solvedStr, newDisplay = self.solveExpand(**kwargs)
            eqt = sympify(solvedStr)
            print(kwargs['noExp'])
            # kwargs['noExp'].append(eqtsSolved)
        else:
            eqt = sympify(self.expr)
            steps.append(eqt)

        for i in eqt.free_symbols:
            iStr = str(i)
            if iStr in eqtDict and not(iStr in kwargs) and not(iStr in kwargs['noExp']):
                inter, interSteps = eqtDict[iStr].expand(**kwargs)
                eqt = eqt.subs(i, inter)
                steps.extend(interSteps)

        eqt = eqt.doit()
        steps.append(eqt)
        return [eqt, steps]

    def solveExpand(self, solStr=None, **kwargs):
        solStr = kwargs.pop('solStr', None) or solStr or self.expr
        varDict = kwargs.pop('varDict', None) or self.vDict
        eqtDict = kwargs.pop('eqtDict', None) or self.eDict
        rootsReturn = kwargs.pop('rootsRet', None) or 0
        # kwargs['noExp'] = kwargs.get('noExp') or []
        solvePat = re.compile('solve\(')
        solves = solvePat.finditer(solStr)
        for i in solves:
            solveStart = i.end(0)
            solveEnd = i.end(0)+helpers.findBalanced(solStr[i.end(0):], '(', ')')
            solveFullSub = solStr[solveStart:solveEnd]
            endexp = i.end(0)+solveFullSub.find(',')
            solveSubStr = solStr[solveStart:endexp]
            kwargs['noExp'].append(solveSubStr)
            # eqtsSolved.append(solveSubStr)
            solveRep, comsRemoved = re.subn(',\s*', '', solStr[endexp:solveEnd])
            if 'solve' in solveSubStr:
                solveSubStr = self.solveExpand(solveSubStr, **kwargs)
    
            else:
                eqt, steps = eqtDict[solveSubStr].expand(**kwargs)
    
            solved = solve(Eq(symbols(eqtDict[solveSubStr].name),eqt), solveRep)
            solvedStr = str(solved[0])
            solStr = solStr.replace(solStr[i.start(0):solveEnd+1],solvedStr)
    
        return [solStr, solveRep]

    def solution(self, eqt,  **kwargs):
        varDict = kwargs.pop('varDict', None) or self.vDict
        eqtDict = kwargs.pop('eqtDict', None) or self.eDict
        for i in eqt.free_symbols:
            iStr = str(i)
            if iStr in varDict and not(iStr in kwargs):
                eqt = eqt.subs(i, varDict[iStr].val)
            elif iStr in kwargs:
                eqt = eqt.subs(i, kwargs[iStr])

        return eqt

    def solutionShowSub(self, eqtStr, **kwargs):
        varDict = kwargs.pop('varDict', None) or self.vDict
        eqtDict = kwargs.pop('eqtDict', None) or self.eDict
        splitEqt = re.split(r'(\w*)', eqtStr)
        for idx, item in enumerate(splitEqt):
            if item in varDict and not(item in kwargs):
                splitEqt[idx] = str(varDict[item].val)
            elif item in kwargs:
                splitEqt[idx] = str(kwargs[item])

        eqtStr = ''.join(splitEqt)
        return eqtStr

    def latexGlsSub(self, eqt, **kwargs):
        varDict = kwargs.pop('varDict', None) or self.vDict
        eqtDict = kwargs.pop('eqtDict', None) or self.eDict
        if not isinstance(eqt, str):
            texTemp = latex(Eq(symbols(self.name), eqt), )
        else:
            texTemp = eqt

        if 'Integral' in self.expr:
            texTemp, numIntChangedRemoved = re.subn(',\s*d', r',\\mathrm{d}', texTemp)

        splitEqt = re.split(r'(\w*)', texTemp)
        symsList = []
        for idx, item in enumerate(splitEqt):
            if item in eqtDict:
                if eqtDict[item].description:
                    splitEqt[idx] = '\\gls{'+item+'}'
                elif eqtDict[item].symbol and eqtDict[item].ensureMath:
                    splitEqt[idx] = '\\ensureMath{'+eqtDict[item].symbol+'}'
                elif eqtDict[item].symbol and not eqtDict[item].ensureMath:
                    splitEqt[idx] = eqtDict[item].symbol

            if item in varDict:
                if varDict[item].description:
                    splitEqt[idx] = '\\gls{'+item+'}'
                elif varDict[item].symbol and varDict[item].ensureMath:
                    splitEqt[idx] = '\\ensureMath{'+varDict[item].symbol+'}'
                elif varDict[item].symbol and not varDict[item].ensureMath:
                    splitEqt[idx] = varDict[item].symbol

        texTemp = ''.join(splitEqt)
        return texTemp
