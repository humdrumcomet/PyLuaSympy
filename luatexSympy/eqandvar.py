import re
from sympy import symbols, latex, sympify
from sympy.utilities.lambdify import lambdify, implemented_function
from sympy import Function
from sympy.parsing.sympy_parser import parse_expr as parExp


class evDict(dict):
    def __getattr__(self,item):
        return self[item]

class eqtClass:
    def __init__(self, dictForProcess):
        self.display = ''
        self.expr = ''
        self.units = ''
        self.glsType = ''
        self.description = ''
        self.lambdOpts = ''
        self.specialExprOpts = ''
        self.process(dictForProcess)
        self.eqt = sympify(self.expr)
        self.symbs = self.eqt.free_symbols
        self.eqtExp = ''
        self.symbsExp = ''
        self.lambd = ''
        self.tex = ''

    def process(self, dfp):
        self.display = dfp.get('display')
        self.expr = dfp.get('eqt')
        self.units = dfp.get('units')
        self.glsType = dfp.get('glsType')
        self.description = dfp.get('description')
        self.lambdOpts = dfp.get('lambdifyOpts')

        if not self.glsType:
            self.glsType = 'symbol'

        if not self.lambdOpts:
            self.glsType = 'numpy'

    def expandAll(self, eqDict, varDict):
        self.eqtExp = self.equationExpand(eqDict)
        self.symbsExp = self.eqtExp.free_symbols
        self.lambd = lambdify(self.symbsExp, self.eqtExp, self.lambdOpts)
        self.tex = latexGlsSub(self, eqDict, varDict)

    def equationExpand(self, eqDict):
        pass

    def latexGlsSub(self, eqDict, varDict):
        pass

    def getExpr(self, eqt, symsDict):
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

class varClass:
    def __init__(self, dictForProcess):
        self.var = '' #Symbol(displaySym)
        self.val = '' #value
        self.units = '' #units
        self.glsType = '' #glsType
        self.description = '' #description
        self.process(dictForProcess)

    def process(self, dfp):
        self.var = symbols(dfp.get('name'))
        self.display = dfp.get('display')
        self.val = dfp.get('value')
        self.units = dfp.get('units')
        self.glsType = dfp.get('glsType')
        self.description = dfp.get('description')
        self.ensureMath = dfp.get('ensureMath').lower() == 'true'

        if not self.ensureMath:
            self.ensureMath = True
        
        if not self.glsType:
            self.glsType = 'symbol'
