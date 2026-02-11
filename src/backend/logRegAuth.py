import backend.auth as au

_log = False
_use = None
_useObjDat = None

def setLog(emaVal, useObjDat=None):
    global _log, _use, _useObjDat
    _log = True
    _use = emaVal
    _useObjDat = useObjDat

def logOut():
    global _log, _use, _useObjDat
    _log = False
    _use = None
    _useObjDat = None

def isLog():
    return _log

def getUse():
    return _use

def getUseObj():
    return _useObjDat

def regUse(emaVal, pasWor, rolVal, firNam=None, konPer=None, vorNam=None, nacNam=None):
    useObj = au.regUse(emaVal, pasWor, rolVal, firNam, konPer, vorNam, nacNam)
    if useObj:
        setLog(emaVal, useObj)
        return True
    return False

def logUse(emaVal, pasWor):
    useObj = au.logUse(emaVal, pasWor)
    if useObj:
        setLog(emaVal, useObj)
        return True
    return False

def sitVie(page):
    if isLog():
        import sites as si
        return si.appSite(page)
    else:
        import logreg as lr
        return lr.logRegPag(page)

def updVie(page):
    page.controls.clear()
    page.add(sitVie(page))
    page.update()
