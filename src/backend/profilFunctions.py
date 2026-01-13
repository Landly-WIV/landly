"""
Backend-Funktionen für die Profilseite
Holt Daten aus der Datenbank basierend auf User-Login
"""

import requests
from typing import Optional, Dict, List

# Backend URL (später in .env auslagern)
BACKEND_URL = "http://localhost:8000"


def get_user_profile(user_email: str) -> Optional[Dict]:
    """
    Holt User-Profil aus der Datenbank
    
    Args:
        user_email: Email des eingeloggten Users
    
    Returns:
        User-Daten oder None bei Fehler
    """
    try:
        response = requests.get(f"{BACKEND_URL}/users/email/{user_email}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Fehler beim Laden des User-Profils: {e}")
        return None


def get_bauer_profile(bauer_id: int) -> Optional[Dict]:
    """
    Holt komplettes Bauer-Profil mit Details
    
    Args:
        bauer_id: ID des Bauern
    
    Returns:
        Bauer-Daten mit Produkten, Standorten etc.
    """
    try:
        response = requests.get(f"{BACKEND_URL}/bauern/{bauer_id}/details")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Fehler beim Laden des Bauer-Profils: {e}")
        return None


def get_bauer_produkte(bauer_id: int) -> List[Dict]:
    """
    Holt alle Produkte eines Bauern
    
    Args:
        bauer_id: ID des Bauern
    
    Returns:
        Liste von Produkten
    """
    try:
        response = requests.get(f"{BACKEND_URL}/bauern/{bauer_id}/produkte")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Fehler beim Laden der Produkte: {e}")
        return []


def get_bauer_standorte(bauer_id: int) -> List[Dict]:
    """
    Holt alle Standorte eines Bauern
    
    Args:
        bauer_id: ID des Bauern
    
    Returns:
        Liste von Standorten
    """
    try:
        response = requests.get(f"{BACKEND_URL}/bauern/{bauer_id}/standorte")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Fehler beim Laden der Standorte: {e}")
        return []


def get_kunde_bestellungen(kunden_id: int) -> List[Dict]:
    """
    Holt alle Bestellungen eines Kunden
    
    Args:
        kunden_id: ID des Kunden
    
    Returns:
        Liste von Bestellungen
    """
    try:
        response = requests.get(f"{BACKEND_URL}/bestellungen")
        if response.status_code == 200:
            alle_bestellungen = response.json()
            # Filtere nach kunden_id
            return [b for b in alle_bestellungen if b.get('kunden_id') == kunden_id]
        return []
    except Exception as e:
        print(f"Fehler beim Laden der Bestellungen: {e}")
        return []


def get_profil_data(user_email: str) -> Optional[Dict]:
    """
    Zentrale Funktion: Holt alle relevanten Profil-Daten
    basierend auf User-Email und Rolle
    
    Args:
        user_email: Email des eingeloggten Users
    
    Returns:
        Dict mit allen Profil-Daten:
        {
            'user': {...},           # User-Daten
            'rolle': 'bauer|kunde',  # Rolle
            'bauer': {...},          # Falls Bauer
            'produkte': [...],       # Falls Bauer
            'standorte': [...],      # Falls Bauer
            'kunde': {...},          # Falls Kunde
            'bestellungen': [...]    # Falls Kunde
        }
    """
    # 1. Hole User-Daten
    user = get_user_profile(user_email)
    if not user:
        return None
    
    result = {
        'user': user,
        'rolle': user.get('rolle', 'kunde')
    }
    
    # 2. Rolle-spezifische Daten laden
    if user.get('rolle') == 'bauer' and user.get('bauer_id'):
        bauer_id = user['bauer_id']
        result['bauer'] = get_bauer_profile(bauer_id)
        result['produkte'] = get_bauer_produkte(bauer_id)
        result['standorte'] = get_bauer_standorte(bauer_id)
    
    elif user.get('rolle') == 'kunde' and user.get('kunde_id'):
        kunden_id = user['kunde_id']
        try:
            kunde_response = requests.get(f"{BACKEND_URL}/kunden/{kunden_id}")
            if kunde_response.status_code == 200:
                result['kunde'] = kunde_response.json()
        except:
            pass
        result['bestellungen'] = get_kunde_bestellungen(kunden_id)
    
    return result


# ========================
# BEISPIEL-NUTZUNG für später:
# ========================
"""
# In content.py nach erfolgreicher Authentifizierung:

from backend import profilFunctions as pf

def profilPage(site):
    user_email = au.getUse()  # "test@example.com"
    
    # Hole alle Profil-Daten aus Datenbank
    profil_daten = pf.get_profil_data(user_email)
    
    if profil_daten:
        if profil_daten['rolle'] == 'bauer':
            # Zeige Hofseite mit echten Daten
            bauer = profil_daten['bauer']
            produkte = profil_daten['produkte']
            return bauSit_mit_echten_daten(bauer, produkte, site)
        
        elif profil_daten['rolle'] == 'kunde':
            # Zeige Kundenprofil mit Bestellhistorie
            kunde = profil_daten['kunde']
            bestellungen = profil_daten['bestellungen']
            return kundenProfil(kunde, bestellungen, site)
    
    # Fallback: Zeige Dummy-Daten
    return profilPage_dummy(site)
"""
