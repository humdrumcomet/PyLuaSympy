import re
import yaml
from pathlib import Path
from . import eqandvar

def yamlLoader(filePath, namespace=None):
    with open(Path(filePath), 'r') as file:
        mVandE = yaml.safe_load(file)

    newVars = eqandvar.evDict()
    newEqts = eqandvar.evDict()
    newAux = {}

    for k, v in mVandE.items():
        if k == 'variables':
            for k2, preProcDict in v.items():
                newVars[k2] = eqandvar.varClass(k2,preProcDict)
        elif k == 'equations':
            for k2, preProcDict in v.items():
                newEqts[k2] = eqandvar.eqtClass(k2,newVars,newEqts,preProcDict)
        elif k == 'glossary':
            for k2, preProcDict in v.items():
                newAux[k2] = preProcDict


    # print(mVandE)
    return newVars, newEqts, newAux

def toGlossHeader(auxDict, varDict, eqtDict):
    combDict = {}
    combDict.update(auxDict)
    combDict.update(varDict)
    combDict.update(eqtDict)
    glsString = ''
    glsType = {
        'symbol': 'symbols',
        'sym': 'symbols',
        'constant': 'constants',
        'cst': 'constants',
        'acronym': r'\acronymtype',
        'acr': r'\acronymtype',
    }
    for k, v in combDict.items():
        partList = []
        if (type(v) is type(dict())) and v.get('description', False):
            glg = 'descriptionExt' in v
            partList.append( (glg and
                             r'''\newglossaryentry{''' + k + r'''g}{name={\glsentrytext{''' + k + '''}},
                             description={''' + v['descriptionExt'] + '''}
                             }

                             ''') or
                             '')

            partList.append(r'''\newglossaryentry{''' + k + '''}{''')

            partList.append( (('glstype' in v) and
                              '''type=''' + glsType[v['glstype']] + ''',
                              ''' ) or
                             '')

            partList.append( '''name={''' + v['display'] + '''},
                             ''')
            partList.append( '''description={''' + v['description'] + '''},
                             ''' )

            partList.append( (('plural' in v) and
                              '''plural={''' + v['plural'] + '''},
                              ''') or
                             '''plural={''' + v['display'] + '''s},
                             ''' )

            partList.append( (('descriptionplural' in v) and
                              '''descriptionplural={''' + v['descriptionplural'] + '''},
                              ''') or
                             '''descriptionplural={''' + v['description'] + '''s},
                             ''' )

            if v.get('glstype', '') == 'acronym':
                # print(v['first'])
                acrPart = ((('first' in v) and
                            '''first={''' + v['first']) or
                           r'''first={\glsentrydesc{''' + k + r'''} (\glsentrytext{''' + k + '''})''')

                acrGlg = ((glg and
                           r'''\glsadd{''' + k + r'''g}}, see=[Glossary:]{''' + k + '''g''') or


                          '') + '''},
                          '''
                partList.append( acrPart + acrGlg )
                partList.append( 'firstplural' in v and
                                 '''firstplural={''' + v['firstplural'] + '''},
                                 ''' or
                                 r'''firstplural={\glsentrydescplural{''' + k + r'''} (\glsentryplural{''' + k + '''})},
                                 ''')
            partList.append( '''}
                             ''' )

        elif getattr(v, 'description', False):
            partList.append(r'''\newglossaryentry{''' + k + '''}{type=''' + glsType[v.glsType] + ''',
                            ''')
            # print(k)
            # print(v.symbol)
            # print(v.ensureMath)
            partList.append('''name={''' + ((v.ensureMath and r'''\ensuremath{''' + v.symbol + '''}''') or v.symbol ) + '''},
                            ''')
            partList.append('''description={''' + v.description + '''}}
                            ''')

        # print(partList)
        for i in partList:
            glsString = glsString + i

        glsString = glsString + '''\n'''

    return re.sub(' +', ' ', glsString)

def equationOut(eqtDict, name, num=0, variant='', label=''):
    label = label or name
    eqtOut = ''
    variant = variant
    num = num
    eqtList = eqtDict[name].totex()
    if variant == 'all':
        eqtOut = eqtOut + r'''
        \begin{align}\label{eqt:''' + label + '''}
        '''
        for n, i in enumerate(eqtList[1]):
            eqtOut = eqtOut + re.sub('=', r'&=', i)
            if n < len(eqtList[1])-1:
                eqtOut = eqtOut + r'''\nonumber\\
                '''

        eqtOut = eqtOut + r'''
        \end{align}
        '''

    elif variant == 'inline':
        eqtOut = eqtOut + r'''$''' + eqtList[num] + r'''$'''

    else:
        eqtOut = eqtOut + r'''
        \begin{equation}\label{eqt:''' + label + '''}
        ''' + eqtList[num] + r'''
        \end{equation}
        '''
    # print(eqtOut)
    return re.sub(' +', ' ', eqtOut)

def dataToTable(name):
    pass

def dataToTikz(name):
    pass

# def printValue(val, name, decimalPlaces=3, units=True):
def printValue(name, inDict={}, decimalPlaces=3, units='', symbol=True): #val, name, decimalPlaces=3, units=True):
    value = getattr(inDict.get(name, False), 'val', False) or name
    units = getattr(inDict.get(name, False), 'units', False) or units
    inGls = getattr(inDict.get(name, False), 'glsType', False) and '\\gls{{{}}}' or '{}'
    call = (symbol and getattr(inDict.get(name, False), 'symbol', False)) or (type(symbol) is type(str()) and symbol) or ''
    symStr = call and ('$' + inGls.format(call) + ' = ') or ''
    endStr = symStr and '$' or ''
    valStr = ('{}\\SI{{{:.' + str(decimalPlaces) + 'E}}}{{{}}}{}').format(symStr, value, units, endStr)
    return valStr
