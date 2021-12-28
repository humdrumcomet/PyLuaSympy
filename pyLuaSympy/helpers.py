import re
import yaml
from pathlib import Path
from . import eqandvar

def yamlLoader(filePath, namespace=None):
    with open(Path(filePath), 'r') as file:
        mVandE = yaml.safe_load(file)

    newVars = eqandvar.evDict()
    newEqts = eqandvar.evDict()

    for k, v in mVandE.items():
        if k == 'variables':
            for k2, preProcDict in v.items():
                newVars[k2] = eqandvar.varClass(k2,preProcDict)
        elif k == 'equations':
            for k2, preProcDict in v.items():
                newEqts[k2] = eqandvar.eqtClass(k2,newVars,newEqts,preProcDict)

    print(mVandE)
    return newVars, newEqts

