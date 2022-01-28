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
    def __init__(self, name, dfp):
        self.name = name
        self.symbol = dfp.get('symbol')
        self.units = dfp.get('units')
        self.glsType = dfp.get('glsType', 'sym')
        self.description = dfp.get('description')
        self.ensureMath = dfp.get('ensureMath', True) 

class varClass(evClass):
    def __init__(self, name, dfp):
        evClass.__init__(self, name, dfp)
        self.val = dfp.get('value') and float(dfp.get('value'))

    def __eq__(self, other):
        # Define equality
        pass

    def __ne__(self, other):
        # define inequality
        pass

    def __lt__(self, other):
        # define less-than
        pass

    def __gt__(self, other):
        # define greater-than
        pass

    def __le__(self, other):
        # define less-than-or-equal
        pass

    def __ge__(self, other):
        # define greater-than-or-equal
        pass

    def __pos__(self):
        # implement unary positive
        pass

    def __neg__(self):
        # implement negation
        pass

    def __abs__(self):
        # implement the abs function (absolute value)
        pass

    def __invert__(self):
        # implement bitwise inversion
        pass

    def __round__(self, n):
        # round to n decimal places (default 0)
        pass

    def __floor__(self):
        # round down to nearest integer
        pass

    def __ceil__(self):
        # round up to nearest integer
        pass

    def __trunc__(self):
        # truncate decimal places
        pass

    def __add__(self, other):
        # Implements addition.
        pass

    def __sub__(self, other):
        # Implements subtraction.
        pass

    def __mul__(self, other):
        # Implements multiplication.
        pass

    def __floordiv__(self, other):
        # Implements integer division using the // operator.
        pass

    def __div__(self, other):
        # Implements division using the / operator.
        pass

    def __truediv__(self, other):
        # Implements true division. Note that this only works when from __future__ import division is in effect.
        pass

    def __mod__(self, other):
        # Implements modulo using the % operator.
        pass

    def __divmod__(self, other):
        # Implements behavior for long division using the divmod() built in function.
        pass

    def __pow__(self, other):
        # Implements behavior for exponents using the ** operator.
        pass

    def __lshift__(self, other):
        # Implements left bitwise shift using the << operator.
        pass

    def __rshift__(self, other):
        # Implements right bitwise shift using the >> operator.
        pass

    def __and__(self, other):
        # Implements bitwise and using the & operator.
        pass

    def __or__(self, other):
        # Implements bitwise or using the | operator.
        pass

    def __xor__(self, other):
        # Implements bitwise xor using the ^ operator.
        pass

    def __radd__(self, other):
        # Implements reflected addition.
        pass

    def __rsub__(self, other):
        # Implements reflected subtraction.
        pass

    def __rmul__(self, other):
        # Implements reflected multiplication.
        pass

    def __rfloordiv__(self, other):
        # Implements reflected integer division using the // operator.
        pass

    def __rdiv__(self, other):
        # Implements reflected division using the / operator.
        pass

    def __rtruediv__(self, other):
        # Implements reflected true division. Note that this only works when from __future__ import division is in effect.
        pass

    def __rmod__(self, other):
        # Implements reflected modulo using the % operator.
        pass

    def __rdivmod__(self, other):
        # Implements behavior for long division using the divmod() built in function, when divmod(other, self) is called.
        pass

    def __rpow__(self, other):
        # Implements behavior for reflected exponents using the ** operator.
        pass

    def __rlshift__(self, other):
        # Implements reflected left bitwise shift using the << operator.
        pass

    def __rrshift__(self, other):
        # Implements reflected right bitwise shift using the >> operator.
        pass

    def __rand__(self, other):
        # Implements reflected bitwise and using the & operator.
        pass

    def __ror__(self, other):
        # Implements reflected bitwise or using the | operator.
        pass

    def __rxor__(self, other):
        # Implements reflected bitwise xor using the ^ operator.
        pass

    def __int__(self):
        # Implements type conversion to int.
        pass

    def __long__(self):
        # Implements type conversion to long.
        pass

    def __float__(self):
        # Implements type conversion to float.
        pass

    def __complex__(self):
        # Implements type conversion to complex.
        pass

    def __oct__(self):
        # Implements type conversion to octal.
        pass

    def __hex__(self):
        # Implements type conversion to hexadecimal.
        pass

    def __index__(self):
        # Implements type conversion to an int when the object is used in a slice expression. If you define a custom numeric type that might be used in slicing, you should define __index__.
        pass

    def __trunc__(self):
        # Called when math.trunc(self) is called. __trunc__ should return the value of `self truncated to an integral type (usually a long).
        pass

    def __coerce__(self, other):
        #
        pass

    def __iadd__(self, other):
        # Implements addition with assignment.
        pass

    def __isub__(self, other):
        # Implements subtraction with assignment.
        pass

    def __imul__(self, other):
        # Implements multiplication with assignment.
        pass

    def __ifloordiv__(self, other):
        # Implements integer division with assignment using the //= operator.
        pass

    def __idiv__(self, other):
        # Implements division with assignment using the /= operator.
        pass

    def __itruediv__(self, other):
        # Implements true division with assignment. Note that this only works when from __future__ import division is in effect.
        pass

    def __imod__(self, other):
        # Implements modulo with assignment using the %= operator.
        pass

    def __ipow__(self, other):
        # Implements behavior for exponents with assignment using the **= operator.
        pass

    def __ilshift__(self, other):
        # Implements left bitwise shift with assignment using the <<= operator.
        pass

    def __irshift__(self, other):
        # Implements right bitwise shift with assignment using the >>= operator.
        pass

    def __iand__(self, other):
        # Implements bitwise and with assignment using the &= operator.
        pass

    def __ior__(self, other):
        # Implements bitwise or with assignment using the |= operator.
        pass

    def __ixor__(self, other):
        # Implements bitwise xor with assignment using the ^= operator.
        pass

    def __str__(self):
        # Defines behavior for when str() is called on an instance of your class.
        pass

    def __repr__(self):
        # Defines behavior for when repr() is called on an instance of your class. The major difference between str() and repr() is intended audience. repr() is intended to produce output that is mostly machine-readable (in many cases, it could be valid Python code even), whereas str() is intended to be human-readable.
        pass

    def __unicode__(self):
        # Defines behavior for when unicode() is called on an instance of your class. unicode() is like str(), but it returns a unicode string. Be wary: if a client calls str() on an instance of your class and you've only defined __unicode__(), it won't work. You should always try to define __str__() as well in case someone doesn't have the luxury of using unicode.
        pass

    def __format__(self, formatstr):
        # Defines behavior for when an instance of your class is used in new-style string formatting. For instance, "Hello, {0:abc}!".format(a) would lead to the call a.__format__("abc"). This can be useful for defining your own numerical or string types that you might like to give special formatting options.
        pass

    def __hash__(self):
        # Defines behavior for when hash() is called on an instance of your class. It has to return an integer, and its result is used for quick key comparison in dictionaries. Note that this usually entails implementing __eq__ as well. Live by the following rule: a == b implies hash(a) == hash(b).
        pass

    def __nonzero__(self):
        # Defines behavior for when bool() is called on an instance of your class. Should return True or False, depending on whether you would want to consider the instance to be True or False.
        pass

class eqtClass(evClass):
    def __init__(self, name, vDict, eDict, dfp):
        evClass.__init__(self, name, dfp)
        self.eDict = eDict
        self.vDict = vDict
        self.expr = dfp.get('expr')
        self.lambdOpts = dfp.get('lambdifyOpts', 'numpy')
        self.texPrintOpts = dfp.get('texPrintOpts') and ', ' + dfp.get('texPrintOpts')
        self.specialExprOpts = ''
        self.eqtType = 'equation'
        self.computeList = {}
        self.delayExp = (dfp.get('delayExp') and re.split('\s*,\s*', dfp.get('delayExp'))) or []
        self.noExp = (dfp.get('noExp') and re.split('\s*,\s*', dfp.get('noExp'))) or []

    def calc(self, *args, **kwargs):
        name = kwargs.pop('name', None) or (args and args[0]) or str(len(self.computeList))
        self.computeList[name] = kwargs
        eqt, steps = self.expand(**kwargs)
        return self.solution(eqt, **kwargs)

    def totex(self, *args, **kwargs):
        name = kwargs.pop('name', None) or (args and args[0])
        mulSymbol = kwargs.pop('mulSymbol', 'dot')
        optsDict = self.computeList.get(name) or {}
        optsDict.update(kwargs)
        eqt, steps = self.expand(**optsDict)
        for idx, item in enumerate(steps):
            steps[idx] = self.latexGlsSub(item, **optsDict)

        steps.append(self.latexGlsSub(self.solutionShowSub(str(Eq(symbols(self.name), eqt)), **optsDict)))
        steps.append(self.latexGlsSub(self.solution(eqt, **optsDict)))
        eqt = self.latexGlsSub(eqt, **optsDict)
        steps = list(dict.fromkeys(steps))

        return [eqt, steps]

    def expand(self, **kwargs):
        varDict = kwargs.pop('varDict', None) or self.vDict
        eqtDict = kwargs.pop('eqtDict', None) or self.eDict
        fromExp = kwargs.pop('fromExp', False)
        steps = kwargs.pop('steps', [])
        kwargs['noExp'] = self.noExp+(kwargs.get('noExp') or [])
        if 'solve(' in self.expr:
            solvedStr, newDisplay = self.solveExpand(**kwargs)
            eqt = sympify(solvedStr)
        else:
            eqt = sympify(self.expr)
            steps.append(eqt)
        
        if 'Integral(' in self.expr or 'Derivative(' in self.expr:
            for i in eqt.variables:
                iStr = str(i)
                if iStr in eqtDict:
                    self.delayExp.append(iStr)

        kwargs['delayExp'] = self.delayExp+(kwargs.get('delayExp') or [])
        curFree = set(map(str, eqt.free_symbols))
        toExp = list((curFree & set(eqtDict.keys())) - (curFree & set(list(kwargs.keys())+kwargs['noExp']+kwargs['delayExp'])))

        while toExp and not fromExp:
            for i in toExp:
                inter, interSteps = eqtDict[i].expand(fromExp = True, **kwargs)
                eqt = eqt.subs(i, inter)
            
            steps.append(eqt)
            curFree = set(map(str, eqt.free_symbols))
            toExp = list((curFree & set(eqtDict.keys())) - (curFree & set(list(kwargs.keys())+kwargs['noExp']+kwargs['delayExp'])))

        eqt = eqt.doit()
        steps.append(eqt)
        steps = list(dict.fromkeys(steps))
        for i in eqt.free_symbols:
            iStr = str(i)
            if iStr in eqtDict and iStr in kwargs['delayExp']:
                inter, interSteps = eqtDict[iStr].expand(**kwargs)
                eqt = eqt.subs(i, inter)
                steps.append(interSteps)

        return [eqt, steps]

    def solveExpand(self, solStr=None, **kwargs):
        solStr = kwargs.pop('solStr', None) or solStr or self.expr
        varDict = kwargs.pop('varDict', None) or self.vDict
        eqtDict = kwargs.pop('eqtDict', None) or self.eDict
        rootsReturn = kwargs.pop('rootsRet', None) or 0
        solvePat = re.compile('solve\(')
        solves = solvePat.finditer(solStr)
        for i in solves:
            solveStart = i.end(0)
            solveEnd = i.end(0)+helpers.findBalanced(solStr[i.end(0):], '(', ')')
            solveFullSub = solStr[solveStart:solveEnd]
            endexp = i.end(0)+solveFullSub.find(',')
            solveSubStr = solStr[solveStart:endexp]
            kwargs['noExp'].append(solveSubStr)
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

        eqtStr = latex(sympify(''.join(splitEqt), evaluate=False))
        return eqtStr

    def latexGlsSub(self, eqt, **kwargs):
        varDict = kwargs.pop('varDict', None) or self.vDict
        eqtDict = kwargs.pop('eqtDict', None) or self.eDict
        if not isinstance(eqt, str):
            texTemp = latex(Eq(symbols(self.name), eqt), )
        else:
            texTemp = eqt

        if 'Integral' in self.expr:
            texTemp, numIntChangedRemoved = re.subn(',\s*d', r''',\mathrm{d}''', texTemp)

        splitEqt = re.split(r'(\w*)', texTemp)
        symsList = []
        for idx, item in enumerate(splitEqt):
            if item in eqtDict:
                if eqtDict[item].description:
                    splitEqt[idx] = r'''\gls{''' + item + r'''}'''
                elif eqtDict[item].symbol:
                    splitEqt[idx] = eqtDict[item].symbol

            if item in varDict:
                if varDict[item].description:
                    splitEqt[idx] = r'''\gls{''' + item + r'''}'''
                elif varDict[item].symbol:
                    splitEqt[idx] = varDict[item].symbol

        texTemp = ''.join(splitEqt)
        return texTemp

    def __eq__(self, other):
        # Define equality
        pass

    def __ne__(self, other):
        # define inequality
        pass

    def __lt__(self, other):
        # define less-than
        pass

    def __gt__(self, other):
        # define greater-than
        pass

    def __le__(self, other):
        # define less-than-or-equal
        pass

    def __ge__(self, other):
        # define greater-than-or-equal
        pass

    def __pos__(self):
        # implement unary positive
        pass

    def __neg__(self):
        # implement negation
        pass

    def __abs__(self):
        # implement the abs function (absolute value)
        pass

    def __invert__(self):
        # implement bitwise inversion
        pass

    def __round__(self, n):
        # round to n decimal places (default 0)
        pass

    def __floor__(self):
        # round down to nearest integer
        pass

    def __ceil__(self):
        # round up to nearest integer
        pass

    def __trunc__(self):
        # truncate decimal places
        pass

    def __add__(self, other):
        # Implements addition.
        pass

    def __sub__(self, other):
        # Implements subtraction.
        pass

    def __mul__(self, other):
        # Implements multiplication.
        pass

    def __floordiv__(self, other):
        # Implements integer division using the // operator.
        pass

    def __div__(self, other):
        # Implements division using the / operator.
        pass

    def __truediv__(self, other):
        # Implements true division. Note that this only works when from __future__ import division is in effect.
        pass

    def __mod__(self, other):
        # Implements modulo using the % operator.
        pass

    def __divmod__(self, other):
        # Implements behavior for long division using the divmod() built in function.
        pass

    def __pow__(self, other):
        # Implements behavior for exponents using the ** operator.
        pass

    def __lshift__(self, other):
        # Implements left bitwise shift using the << operator.
        pass

    def __rshift__(self, other):
        # Implements right bitwise shift using the >> operator.
        pass

    def __and__(self, other):
        # Implements bitwise and using the & operator.
        pass

    def __or__(self, other):
        # Implements bitwise or using the | operator.
        pass

    def __xor__(self, other):
        # Implements bitwise xor using the ^ operator.
        pass

    def __radd__(self, other):
        # Implements reflected addition.
        pass

    def __rsub__(self, other):
        # Implements reflected subtraction.
        pass

    def __rmul__(self, other):
        # Implements reflected multiplication.
        pass

    def __rfloordiv__(self, other):
        # Implements reflected integer division using the // operator.
        pass

    def __rdiv__(self, other):
        # Implements reflected division using the / operator.
        pass

    def __rtruediv__(self, other):
        # Implements reflected true division. Note that this only works when from __future__ import division is in effect.
        pass

    def __rmod__(self, other):
        # Implements reflected modulo using the % operator.
        pass

    def __rdivmod__(self, other):
        # Implements behavior for long division using the divmod() built in function, when divmod(other, self) is called.
        pass

    def __rpow__(self, other):
        # Implements behavior for reflected exponents using the ** operator.
        pass

    def __rlshift__(self, other):
        # Implements reflected left bitwise shift using the << operator.
        pass

    def __rrshift__(self, other):
        # Implements reflected right bitwise shift using the >> operator.
        pass

    def __rand__(self, other):
        # Implements reflected bitwise and using the & operator.
        pass

    def __ror__(self, other):
        # Implements reflected bitwise or using the | operator.
        pass

    def __rxor__(self, other):
        # Implements reflected bitwise xor using the ^ operator.
        pass

    def __int__(self):
        # Implements type conversion to int.
        pass

    def __long__(self):
        # Implements type conversion to long.
        pass

    def __float__(self):
        # Implements type conversion to float.
        pass

    def __complex__(self):
        # Implements type conversion to complex.
        pass

    def __oct__(self):
        # Implements type conversion to octal.
        pass

    def __hex__(self):
        # Implements type conversion to hexadecimal.
        pass

    def __index__(self):
        # Implements type conversion to an int when the object is used in a slice expression. If you define a custom numeric type that might be used in slicing, you should define __index__.
        pass

    def __trunc__(self):
        # Called when math.trunc(self) is called. __trunc__ should return the value of `self truncated to an integral type (usually a long).
        pass

    def __coerce__(self, other):
        #
        pass

    def __iadd__(self, other):
        # Implements addition with assignment.
        pass

    def __isub__(self, other):
        # Implements subtraction with assignment.
        pass

    def __imul__(self, other):
        # Implements multiplication with assignment.
        pass

    def __ifloordiv__(self, other):
        # Implements integer division with assignment using the //= operator.
        pass

    def __idiv__(self, other):
        # Implements division with assignment using the /= operator.
        pass

    def __itruediv__(self, other):
        # Implements true division with assignment. Note that this only works when from __future__ import division is in effect.
        pass

    def __imod__(self, other):
        # Implements modulo with assignment using the %= operator.
        pass

    def __ipow__(self, other):
        # Implements behavior for exponents with assignment using the **= operator.
        pass

    def __ilshift__(self, other):
        # Implements left bitwise shift with assignment using the <<= operator.
        pass

    def __irshift__(self, other):
        # Implements right bitwise shift with assignment using the >>= operator.
        pass

    def __iand__(self, other):
        # Implements bitwise and with assignment using the &= operator.
        pass

    def __ior__(self, other):
        # Implements bitwise or with assignment using the |= operator.
        pass

    def __ixor__(self, other):
        # Implements bitwise xor with assignment using the ^= operator.
        pass

    def __str__(self):
        # Defines behavior for when str() is called on an instance of your class.
        pass

    def __repr__(self):
        # Defines behavior for when repr() is called on an instance of your class. The major difference between str() and repr() is intended audience. repr() is intended to produce output that is mostly machine-readable (in many cases, it could be valid Python code even), whereas str() is intended to be human-readable.
        pass

    def __unicode__(self):
        # Defines behavior for when unicode() is called on an instance of your class. unicode() is like str(), but it returns a unicode string. Be wary: if a client calls str() on an instance of your class and you've only defined __unicode__(), it won't work. You should always try to define __str__() as well in case someone doesn't have the luxury of using unicode.
        pass

    def __format__(self, formatstr):
        # Defines behavior for when an instance of your class is used in new-style string formatting. For instance, "Hello, {0:abc}!".format(a) would lead to the call a.__format__("abc"). This can be useful for defining your own numerical or string types that you might like to give special formatting options.
        pass

    def __hash__(self):
        # Defines behavior for when hash() is called on an instance of your class. It has to return an integer, and its result is used for quick key comparison in dictionaries. Note that this usually entails implementing __eq__ as well. Live by the following rule: a == b implies hash(a) == hash(b).
        pass

    def __nonzero__(self):
        # Defines behavior for when bool() is called on an instance of your class. Should return True or False, depending on whether you would want to consider the instance to be True or False.
        pass

    def __call__(self, **kwargs):
        # Define what happens when the equation is called with not attribute, but handed kwargs (compute itself)
        pass
