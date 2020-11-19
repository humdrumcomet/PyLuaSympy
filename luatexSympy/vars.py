from sympy import Symbol, latex, sympify

class varDict:
    def __init__(self):
        self.dict = {}

    def add(self, name, displaySym, value, units, glsType, description):
        self.dict[name] = varClass(displaySym, value, units, glsType, description)

class varClass:
    def __init__(self, displaySym, value, units, glsType, description):
        self.var = Symbol(displaySym)
        self.val = value
        self.units = units
        self.glsType = glsType
        self.description = description
