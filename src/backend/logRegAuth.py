import logreg as lr
import sites as si

_log = False
_user = None

def setLog(useNam):
    global _log, _user
    _log = True
    _user = useNam

def logOut():
    global _log, _user
    _log = False
    _user = None

def isLog():
    return _log

def getUse():
    return _user

def sitVie(page):
    if isLog():
        return si.appSite(page)
    else:
        return lr.logRegPag(page)

def updVie(page):
    page.controls.clear()
    page.add(sitVie(page))
    page.update()