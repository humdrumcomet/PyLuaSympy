import re
from sympy import symbols, latex, sympify, Eq, lambdify, Function
# from sympy.utilities.lambdify import lambdify, implemented_function
# from sympy import Function
from sympy.parsing.sympy_parser import parse_expr as parExp


class evDict(dict):
    def __getattr__(self,item):
        return self[item]

class eqtClass:
    def __init__(self, dfp):
        self.name = dfp.get('name') or ''
        self.display = dfp.get('display') or ''
        self.initExpr = dfp.get('expr') or ''
        self.units = dfp.get('units') or ''
        self.glsType = dfp.get('glsType') or 'sym'
        self.description = dfp.get('description') or ''
        self.lambdOpts = dfp.get('lambdifyOpts') or 'numpy'
        self.texPrintOpts = ''

        self.ensureMath = (dfp.get('ensureMath') or 'true').lower() == 'true'
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
        self.initLam = ''
        self.initLamSub = ''
        self.finLam = ''
        self.finLamSub = ''

        if dfp.get('texPrintOpts'):
            self.texPrintOpts = ', ' + dfp.get('texPrintOpts')

    def compute(self, **kwargs):
        pass

    def texPrint(self, **kwargs):
        pass

class varClass:
    def __init__(self, dfp):
        self.var = symbols(dfp.get('name')) #Symbol(displaySym)
        self.display = dfp.get('display') or ''
        self.val = '' #value
        self.units = dfp.get('units') or '' #units
        self.glsType = dfp.get('glsType') or 'sym' #glsType
        self.description = dfp.get('description') or '' #description
        self.ensureMath = (dfp.get('ensureMath') or 'true').lower() == 'true'

        if dfp.get('value'):
            self.val = float(dfp.get('value'))
