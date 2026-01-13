"""
Backend-Funktionen für den Warenkorb
Verbindet Frontend-Warenkorb mit der Datenbank
"""

import requests
from typing import Optional, Dict, List

# Backend URL (später in .env auslagern)
BACKEND_URL = "http://localhost:8000"


def get_warenkorb(user_id: int) -> Optional[Dict]:
    """
    Holt den aktiven Warenkorb eines Users aus der Datenbank
    Erstellt automatisch einen neuen wenn keiner existiert
    
    Args:
        user_id: ID des eingeloggten Users
    
    Returns:
        Warenkorb-Daten mit allen Positionen
        {
            'warenkorb_id': 1,
            'user_id': 1,
            'status': 'offen',
            'positionen': [
                {
                    'warenkorb_position_id': 1,
                    'produkt_id': 5,
                    'menge': 2,
                    'preis_je_einheit': 3.50,
                    'produkt': {
                        'name': 'Bio-Tomaten',
                        'beschreibung': '...',
                        'einheit': 'kg'
                    }
                }
            ]
        }
    """
    try:
        response = requests.get(f"{BACKEND_URL}/warenkorb/user/{user_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Fehler beim Laden des Warenkorbs: {e}")
        return None


def add_to_warenkorb(warenkorb_id: int, produkt_id: int, menge: int, preis_je_einheit: float) -> bool:
    """
    Fügt ein Produkt zum Warenkorb hinzu
    
    Args:
        warenkorb_id: ID des Warenkorbs
        produkt_id: ID des Produkts
        menge: Anzahl
        preis_je_einheit: Preis pro Einheit
    
    Returns:
        True wenn erfolgreich, False bei Fehler
    """
    try:
        response = requests.post(
            f"{BACKEND_URL}/warenkorb/{warenkorb_id}/add",
            params={
                "produkt_id": produkt_id,
                "menge": menge,
                "preis_je_einheit": preis_je_einheit
            }
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Fehler beim Hinzufügen zum Warenkorb: {e}")
        return False


def update_warenkorb_position(position_id: int, menge: int) -> bool:
    """
    Aktualisiert die Menge einer Warenkorb-Position
    
    Args:
        position_id: ID der Warenkorb-Position
        menge: Neue Menge
    
    Returns:
        True wenn erfolgreich, False bei Fehler
    """
    try:
        response = requests.put(
            f"{BACKEND_URL}/warenkorb/position/{position_id}",
            params={"menge": menge}
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Fehler beim Aktualisieren der Position: {e}")
        return False


def remove_from_warenkorb(position_id: int) -> bool:
    """
    Entfernt eine Position aus dem Warenkorb
    
    Args:
        position_id: ID der Warenkorb-Position
    
    Returns:
        True wenn erfolgreich, False bei Fehler
    """
    try:
        response = requests.delete(f"{BACKEND_URL}/warenkorb/position/{position_id}")
        return response.status_code == 200
    except Exception as e:
        print(f"Fehler beim Entfernen aus Warenkorb: {e}")
        return False


def clear_warenkorb(warenkorb_id: int) -> bool:
    """
    Leert den kompletten Warenkorb
    
    Args:
        warenkorb_id: ID des Warenkorbs
    
    Returns:
        True wenn erfolgreich, False bei Fehler
    """
    try:
        response = requests.delete(f"{BACKEND_URL}/warenkorb/{warenkorb_id}/clear")
        return response.status_code == 200
    except Exception as e:
        print(f"Fehler beim Leeren des Warenkorbs: {e}")
        return False


def checkout_warenkorb(warenkorb_id: int, bauer_id: int) -> Optional[Dict]:
    """
    Wandelt Warenkorb in eine Bestellung um (Checkout)
    
    Args:
        warenkorb_id: ID des Warenkorbs
        bauer_id: ID des Bauern (von dem bestellt wird)
    
    Returns:
        Bestellungs-Daten oder None bei Fehler
    """
    try:
        response = requests.post(
            f"{BACKEND_URL}/warenkorb/{warenkorb_id}/checkout",
            params={"bauer_id": bauer_id}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Fehler beim Checkout: {e}")
        return None


def get_gesamtpreis(warenkorb: Dict) -> float:
    """
    Berechnet den Gesamtpreis aus Warenkorb-Daten
    
    Args:
        warenkorb: Warenkorb-Dict von get_warenkorb()
    
    Returns:
        Gesamtpreis
    """
    if not warenkorb or 'positionen' not in warenkorb:
        return 0.0
    
    return sum(
        pos['menge'] * pos['preis_je_einheit'] 
        for pos in warenkorb['positionen']
    )


def format_warenkorb_for_frontend(warenkorb: Dict) -> List[Dict]:
    """
    Konvertiert Backend-Warenkorb-Format zu Frontend-Format
    
    Args:
        warenkorb: Warenkorb von get_warenkorb()
    
    Returns:
        Liste von Items im Frontend-Format
        [
            {
                'proId': 5,
                'position_id': 1,  # Für Updates/Deletes
                'name': 'Bio-Tomaten',
                'preis': 3.50,
                'einheit': 'kg',
                'menge': 2
            }
        ]
    """
    if not warenkorb or 'positionen' not in warenkorb:
        return []
    
    items = []
    for pos in warenkorb['positionen']:
        produkt = pos.get('produkt', {})
        items.append({
            'proId': pos['produkt_id'],
            'position_id': pos['warenkorb_position_id'],  # Wichtig für Updates!
            'name': produkt.get('name', 'Unbekannt'),
            'preis': pos['preis_je_einheit'],
            'einheit': produkt.get('einheit', 'Stk'),
            'menge': pos['menge']
        })
    
    return items


# ========================
# BEISPIEL-NUTZUNG für später:
# ========================
"""
# In warenkorb.py nach Backend-Aktivierung:

import backend.warenkorbFunctions as wf
import backend.logRegAuth as au

def getWarenkorb():
    # Hole User-ID aus Login
    user = au.getUse()
    if not isinstance(user, dict) or 'user_id' not in user:
        # Fallback: Demo-Modus
        return _warenkorb
    
    # Hole Warenkorb aus Datenbank
    warenkorb = wf.get_warenkorb(user['user_id'])
    if warenkorb:
        return wf.format_warenkorb_for_frontend(warenkorb)
    
    return []

def addToWarenkorb(prod, menge=1):
    user = au.getUse()
    if not isinstance(user, dict):
        # Fallback: Demo-Modus
        # ... original code ...
        return
    
    # Hole Warenkorb
    warenkorb = wf.get_warenkorb(user['user_id'])
    if warenkorb:
        wf.add_to_warenkorb(
            warenkorb_id=warenkorb['warenkorb_id'],
            produkt_id=prod.proId,
            menge=menge,
            preis_je_einheit=prod.preis
        )

def removeFromWarenkorb(proId):
    # proId ist jetzt position_id aus format_warenkorb_for_frontend()
    user = au.getUse()
    if isinstance(user, dict):
        wf.remove_from_warenkorb(position_id=proId)
    else:
        # Fallback: Demo-Modus
        # ... original code ...

def checkout_click(e):
    user = au.getUse()
    if isinstance(user, dict):
        warenkorb = wf.get_warenkorb(user['user_id'])
        if warenkorb:
            # TODO: Bauer-ID vom User auswählen lassen
            bauer_id = 1
            bestellung = wf.checkout_warenkorb(
                warenkorb_id=warenkorb['warenkorb_id'],
                bauer_id=bauer_id
            )
            if bestellung:
                # Erfolgreich bestellt!
                pass
"""
