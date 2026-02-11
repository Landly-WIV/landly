import requests
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import API_URL

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
    try:
        params = {
            "email": emaVal,
            "passwort": pasWor,
            "rolle": rolVal
        }
        if firNam:
            params["firmenname"] = firNam
        if konPer:
            params["kontaktperson"] = konPer
        if vorNam:
            params["vorname"] = vorNam
        if nacNam:
            params["nachname"] = nacNam
        
        res = requests.post(f"{API_URL}/auth/register", params=params)
        if res.status_code == 200:
            useObj = res.json()
            setLog(emaVal, useObj)
            return True
    except Exception as e:
        print(f"Registrierung fehlgeschlagen: {e}")
    return False

def logUse(emaVal, pasWor):
    try:
        res = requests.post(f"{API_URL}/auth/login", params={"email": emaVal, "passwort": pasWor})
        if res.status_code == 200:
            useObj = res.json()
            setLog(emaVal, useObj)
            return True
    except Exception as e:
        print(f"Login fehlgeschlagen: {e}")
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
