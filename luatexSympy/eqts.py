import re
from sympy import Symbol, latex, sympify
from sympy.utilities.lambdify import lambdify, implemented_function
from sympy import Function
from sympy.parsing.sympy_parser import parse_expr as parExp


class eqDict:
    def __init__(self):
        self.dict = {}

    def add(self, name, display, syms, eq, units, glsType, description):
        self.dict[name] = eqtClass(display, syms, eq, units, glsType, description)

class eqtClass:
    def __init__(self, display, symsDict, eqt, units, glsType, description):
        self.display = display
        self.expr, self.tex, self.eqt, self.symbs = self.getExpr(eqt, symsDict)
        self.units = units
        self.glsType = glsType
        self.description = description

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
