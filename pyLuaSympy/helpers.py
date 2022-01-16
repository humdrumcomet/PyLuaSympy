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
                             r'\newglossaryentry{' +
                             k + r'g}{name={\glsentrytext{' +
                             k + r'}}, description={' +
                             v['descriptionExt'] + r'}}') or
                             '')

            partList.append(r'\newglossaryentry{' +
                            k +
                            r'}{')

            partList.append( (('glstype' in v) and
                              r'type=' +
                              glsType[v['glstype']] +
                              r',' ) or
                             '')

            partList.append( r'name={' +
                             v['display'] +
                             r'}, ' )

            partList.append( r'description={' +
                             v['description'] +
                             r'}, ' )

            partList.append( (('plural' in v) and
                              r'plural={' +
                              v['plural'] +
                              r'},') or
                             r'plural={' +
                             v['display'] +
                             r's}, ' )

            partList.append( (('descriptionplural' in v) and
                              r'descriptionplural={' +
                              v['descriptionplural'] +
                              r'}, ') or
                             r'descriptionplural={' +
                             v['description'] +
                             r's}, ' )

            if v.get('glstype', '') == 'acronym':
                # print(v['first'])
                acrPart = ((('first' in v) and
                            r'first={' + v['first']) or
                           r'first={\glsentrydesc{' +
                           k +
                           r'} (\glsentrytext{' +
                           k +
                           r'})')

                acrGlg = ((glg and r'\glsadd{' + k + r'g}') or '') + r'}, '
                partList.append( acrPart + acrGlg )
                partList.append( 'firstplural' in v and
                                 r'firstplural={' +
                                 v['firstplural'] +
                                 r'}' or
                                 r'firstplural={\glsentrydescplural{' +
                                 k +
                                 r'} (\glsentryplural{' +
                                 k +
                                 r'})}')
            partList.append( r'} ' )

        elif getattr(v, 'description', False):
            partList.append(r'\newglossaryentry{' + k + r'}{type=')
            partList.append(glsType[v.glsType] + r', ')
            partList.append(r'name={' + ((v.ensureMath and r'\ensuremath{' + v.symbol + r'}') or v.symbol ) + r'}, ')
            partList.append(r'description={' + v.description + r'}} ')

        # print(partList)
        for i in partList:
            glsString = glsString + i + '\n '

    return glsString
