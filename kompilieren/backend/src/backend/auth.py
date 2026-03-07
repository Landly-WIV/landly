import hashlib
import secrets
from sqlalchemy.orm import Session
from typing import Optional

from backend import models
from backend.db import SessionLocal


def hasPas(pasWor):
    salVal = secrets.token_hex(16)
    hasVal = hashlib.pbkdf2_hmac('sha256', pasWor.encode('utf-8'), salVal.encode('utf-8'), 100000)
    return f"{salVal}${hasVal.hex()}"


def verPas(plaPass: str, hasPass: str) -> bool:
    try:
        salVal, hasVal = hasPass.split('$')
        newHas = hashlib.pbkdf2_hmac('sha256', plaPass.encode('utf-8'), salVal.encode('utf-8'), 100000)
        return newHas.hex() == hasVal
    except:
        return False


def regUse(emaVal, pasWor, rolVal, firNam, konPer, vorNam, nacNam):
    db = SessionLocal()
    try:
        exiUse = db.query(models.User).filter(models.User.email == emaVal).first()
        if exiUse:
            return None

        hasPass = hasPas(pasWor)

        bauId = None
        kunId = None

        if rolVal == "bauer":
            newBau = models.Bauer(
                firmenname=firNam,
                kontaktperson=konPer,
                email=emaVal
            )
            db.add(newBau)
            db.flush()
            bauId = newBau.bauer_id

        elif rolVal == "kunde":
            newKun = models.Kunde(
                vorname=vorNam,
                nachname=nacNam,
                email=emaVal
            )
            db.add(newKun)
            db.flush()
            kunId = newKun.kunden_id

        newUse = models.User(
            email=emaVal,
            passwort_hash=hasPass,
            rolle=rolVal,
            kunde_id=kunId,
            bauer_id=bauId
        )

        db.add(newUse)
        db.commit()
        db.refresh(newUse)

        return newUse

    except Exception as e:
        db.rollback()
        print(f"Fehler: {e}")
        return None
    finally:
        db.close()


def logUse(emaVal, pasWor):
    db = SessionLocal()
    try:
        useObj = db.query(models.User).filter(models.User.email == emaVal).first()

        if not useObj:
            return None

        if useObj.aktiv != 1:
            return None

        if not verPas(pasWor, useObj.passwort_hash):
            return None

        return useObj

    except Exception as e:
        print(f"Fehler: {e}")
        return None
    finally:
        db.close()


def autUse(emaVal, pasWor):
    return logUse(emaVal, pasWor)
