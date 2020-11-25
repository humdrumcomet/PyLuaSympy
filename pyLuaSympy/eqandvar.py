import re
from sympy import symbols, latex, sympify, Eq, lambdify, Function
# from sympy.utilities.lambdify import lambdify, implemented_function
# from sympy import Function
from sympy.parsing.sympy_parser import parse_expr as parExp


class evDict(dict):
    def __getattr__(self,item):
        return self[item]

class eqtClass:
    def __init__(self, dictForProcess):
        self.name = ''
        self.display = ''
        self.units = ''
        self.glsType = ''
        self.description = ''
        self.ensureMath = ''
        self.lambdOpts = ''
        self.specialExprOpts = ''
        self.eqtType = 'equation'
        self.initExpr = ''
        self.initEqt = ''
        self.initEqual = ''
        self.initSymbs = ''
        self.initTex = ''
        self.interExpr = ''
        self.interEqt = ''
        self.interEqual = ''
        self.interSymbs = ''
        self.interTex = ''
        self.finEqt = ''
        self.finEqual = ''
        self.finSymbs = ''
        self.finTex = ''
        self.eqtsSolved = {}
        self.lambd = ''
        self.texPrintOpts = ''
        self.process(dictForProcess)

    def process(self, dfp):
        self.name = dfp.get('name')
        self.display = dfp.get('display')
        self.initExpr = dfp.get('eqt')
        self.units = dfp.get('units')
        self.glsType = dfp.get('glsType')
        self.description = dfp.get('description')
        self.lambdOpts = dfp.get('lambdifyOpts')
        self.texPrintOpts = dfp.get('texPrintOpts')

        if self.ensureMath:
            self.ensureMath = self.ensureMath.lower() == 'true'
        else:
            self.ensureMath = True

        if not self.glsType:
            self.glsType = 'sym'

        if not self.lambdOpts:
            self.lambdOpts = 'numpy'

        if self.texPrintOpts:
            self.texPrintOpts = ', ' + self.texPrintOpts

        # if not 'solve' in self.expr:
            # self.eqt = sympify(self.expr)
            # self.equal = Eq(symbols(self.name), self.eqt)
            # self.symbs = self.eqt.free_symbols
        # else:
            # self.solveExpr = self.expr

class varClass:
    def __init__(self, dictForProcess):
        self.var = '' #Symbol(displaySym)
        self.display = ''
        self.val = '' #value
        self.units = '' #units
        self.glsType = '' #glsType
        self.description = '' #description
        self.ensureMath = ''
        self.process(dictForProcess)

    def process(self, dfp):
        self.var = symbols(dfp.get('name'))
        self.display = dfp.get('display')
        self.val = float(dfp.get('value'))
        self.units = dfp.get('units')
        self.glsType = dfp.get('glsType')
        self.description = dfp.get('description')
        self.ensureMath = dfp.get('ensureMath')

        if self.ensureMath:
            self.ensureMath = self.ensureMath.lower() == 'true'
        else:
            self.ensureMath = True
        
        if not self.glsType:
            self.glsType = 'sym'
