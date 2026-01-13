# 🔌 Backend-Integration Guide für Profilseite

## Status Quo

✅ **Backend ist komplett implementiert**
- FastAPI Server mit allen Endpoints
- PostgreSQL Datenbank (NeonDB)
- User-, Bauer-, Kunde-Management
- Produkte, Standorte, Bestellungen

⚠️ **Frontend nutzt aktuell Dummy-Daten**
- Login ist im Demo-Modus (keine echte Authentifizierung)
- Profilseite zeigt statische Daten

## 🎯 Integration in 3 Schritten

### **Schritt 1: Backend starten**

```powershell
# Terminal 1: FastAPI Backend
cd "c:\Programmieren WIV\github repo\landly"
uv run uvicorn src.backend.main:app --reload --host localhost --port 8000
```

Teste ob Backend läuft:
```powershell
# In neuem Terminal oder Browser
curl http://localhost:8000
# Oder öffne: http://localhost:8000/docs (Swagger UI)
```

### **Schritt 2: Authentifizierung aktivieren**

**In `src/backend/logRegAuth.py`:**

```python
# Aktuell:
def setLog(useNam):
    global _log, _user
    _log = True
    _user = useNam  # Nur Username als String

# Später mit Backend:
import backend.profilFunctions as pf

def setLog(email, password):
    """Login mit echtem Backend"""
    # 1. Hole User aus DB
    user_data = pf.get_user_profile(email)
    
    if user_data:
        # 2. Prüfe Passwort (mit bcrypt wenn auth.py aktiviert)
        # from backend import auth
        # if auth.verify_password(password, user_data['passwort_hash']):
        
        # 3. Speichere User-Daten
        global _log, _user
        _log = True
        _user = user_data  # Jetzt komplettes User-Objekt mit rolle, bauer_id etc.
        return True
    
    return False

def getUse():
    """Gibt jetzt komplettes User-Objekt zurück"""
    return _user
```

### **Schritt 3: Profilseite mit echten Daten**

**In `src/content.py`:**

```python
import backend.profilFunctions as pf

def profilPage(site):
    """Profilseite mit Backend-Integration"""
    
    # Hole User-Daten
    user = au.getUse()  # Jetzt Dict statt String
    
    if isinstance(user, str):
        # Fallback für Demo-Modus
        return profilPage_demo(site, user)
    
    # Hole alle Profil-Daten aus Datenbank
    user_email = user.get('email')
    profil_daten = pf.get_profil_data(user_email)
    
    if not profil_daten:
        # Fehler beim Laden
        return error_page("Profil konnte nicht geladen werden")
    
    # Je nach Rolle: Bauer oder Kunde
    if profil_daten['rolle'] == 'bauer':
        return profilPage_bauer(site, profil_daten)
    else:
        return profilPage_kunde(site, profil_daten)


def profilPage_bauer(site, profil_daten):
    """Hofseite mit echten Daten aus Datenbank"""
    bauer = profil_daten['bauer']
    produkte = profil_daten['produkte']
    standorte = profil_daten['standorte']
    
    # Nutze echte Daten statt Dummy-Werte:
    hofname = bauer.get('firmenname', 'Hof Sonnenblume')
    telefon = bauer.get('telefon', '+49 123 456789')
    email = bauer.get('email', 'info@hof.de')
    
    # Baue Produkt-Kacheln aus DB-Daten
    product_tiles = []
    for prod in produkte[:6]:  # Max 6 Produkte
        tile = create_product_tile(
            name=prod['name'],
            emoji=get_emoji_for_produktart(prod['produktart_id']),
            site=site
        )
        product_tiles.append(tile)
    
    # ... Rest der Profilseite mit echten Daten
```

## 📋 Datenbank-Struktur

### **User-Tabelle**
```python
user = {
    'user_id': 1,
    'email': 'bauer@hof.de',
    'rolle': 'bauer',  # 'bauer' | 'kunde' | 'admin'
    'bauer_id': 5,     # Falls Bauer
    'kunde_id': None,  # Falls Kunde
    'aktiv': 1
}
```

### **Bauer-Tabelle**
```python
bauer = {
    'bauer_id': 5,
    'firmenname': 'Hof Sonnenblume',
    'kontaktperson': 'Max Müller',
    'straße': 'Dorfstr.',
    'hausnr': 23,
    'ort_id': 1,
    'telefon': 123456789,
    'email': 'info@sonnenblume.de'
}
```

### **Produkt-Tabelle**
```python
produkt = {
    'produkt_id': 10,
    'name': 'Bio-Tomaten',
    'beschreibung': 'Frisch geerntet',
    'preis': 3.50,
    'einheit': 'kg',
    'bauern_id': 5,
    'produktart_id': 1  # 1=Gemüse, 2=Obst, etc.
}
```

## 🔄 Migration: Demo → Echt

### Phase 1: Parallel-Betrieb (empfohlen)
```python
def profilPage(site):
    user = au.getUse()
    
    # Prüfe ob Backend läuft
    try:
        if isinstance(user, dict) and 'email' in user:
            # Backend-Modus
            return profilPage_mit_backend(site, user)
    except:
        pass
    
    # Fallback: Demo-Modus
    return profilPage_demo(site, user)
```

### Phase 2: Volle Integration
- auth.py aktivieren (Passwort-Hashing mit bcrypt)
- Session-Management mit JWT-Tokens
- Fehlerbehandlung bei DB-Ausfällen

## 🧪 Testing

### 1. Backend testen
```powershell
# API Docs öffnen
start http://localhost:8000/docs

# Test-Requests
curl http://localhost:8000/bauern/1
curl http://localhost:8000/bauern/1/produkte
```

### 2. Integration testen
```python
# In Python-Console
from src.backend import profilFunctions as pf

# Test User-Profil
user = pf.get_user_profile("test@example.com")
print(user)

# Test Bauer-Daten
profil = pf.get_profil_data("bauer@hof.de")
print(profil['bauer'])
print(profil['produkte'])
```

## 📝 Nächste Schritte

1. ✅ Backend läuft (FastAPI auf Port 8000)
2. ✅ Datenbank ist verbunden (NeonDB)
3. ⏳ Test-Daten in DB einfügen (INSERT Statements)
4. ⏳ Authentifizierung mit echtem Passwort-Hashing
5. ⏳ Frontend mit Backend verbinden
6. ⏳ Session-Management implementieren

## 💡 Tipp

Starte mit einem Test-User in der Datenbank:

```sql
-- User erstellen
INSERT INTO users (email, passwort_hash, rolle, bauer_id)
VALUES ('test@sonnenblume.de', 'dummy_hash', 'bauer', 1);

-- Bauer erstellen
INSERT INTO bauern (firmenname, email, telefon)
VALUES ('Hof Sonnenblume', 'info@sonnenblume.de', 123456789);

-- Produkte hinzufügen
INSERT INTO produkte (name, preis, einheit, bauern_id, produktart_id)
VALUES ('Bio-Tomaten', 3.50, 'kg', 1, 1);
```

Dann kannst du testen ob `profilFunctions.py` die Daten richtig abholt!
