# ⚙️ Installation & Quick Start

Diese Anleitung ermöglicht es, Landly **ohne Rückfragen** auf einem lokalen System zu starten.

---

## 📋 Voraussetzungen

### Laufzeitumgebungen

| Software | Minimale Version | Empfohlene Version | Download |
|----------|------------------|-------------------|----------|
| **Python** | 3.10 | 3.11+ | [python.org](https://www.python.org/downloads/) |
| **Git** | 2.30+ | Latest | [git-scm.com](https://git-scm.com/downloads) |
| **pip** | 23.0+ | Latest | (mit Python installiert) |

!!! tip "Python-Version prüfen"
    ```bash
    python --version
    # oder
    python3 --version
    ```

---

### Datenbanksysteme

**Entwicklung:** SQLite (keine Installation nötig)
- Wird automatisch mit Python installiert
- Datei-basiert, keine Konfiguration erforderlich

**Produktion (optional):** PostgreSQL
- Version 13+
- [postgresql.org/download](https://www.postgresql.org/download/)

!!! info "SQLite vs. PostgreSQL"
    Für **lokale Entwicklung** reicht SQLite vollkommen aus. PostgreSQL wird nur für das Production-Deployment benötigt.

---

### Sonstige Abhängigkeiten

**Alle Python-Pakete** sind in `requirements.txt` definiert:

- **Flet** (0.24.x) - Frontend-Framework
- **FastAPI** (0.110.x) - Backend-Framework
- **Uvicorn** (0.27.x) - ASGI-Server
- **SQLAlchemy** (2.0.x) - ORM
- **Pydantic** (2.0.x) - Datenvalidierung
- **python-jose** (3.3.x) - JWT-Authentifizierung
- **passlib** (1.7.x) - Passwort-Hashing
- **python-dotenv** (1.0.x) - Umgebungsvariablen

Diese werden automatisch im nächsten Schritt installiert.

---

## 🚀 Schritt-für-Schritt-Anleitung

### Schritt 1: Repository klonen

```bash
git clone https://github.com/[ORGANIZATION]/landly.git
cd landly
```

!!! note "GitHub URL anpassen"
    Ersetze `[ORGANIZATION]` durch euren GitHub-Organisationsnamen.

---

### Schritt 2: Virtuelle Umgebung erstellen

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

!!! success "Aktivierung erfolgreich"
    Der Prompt sollte jetzt `(.venv)` am Anfang zeigen.

---

### Schritt 3: Abhängigkeiten installieren

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Erwartete Dauer:** 1-3 Minuten

!!! tip "Bei Fehlern"
    Falls Fehler auftreten, versuche:
    ```bash
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    ```

---

### Schritt 4: Umgebungsvariablen konfigurieren

Kopiere die Beispiel-Konfiguration:

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
```

Öffne `.env` in einem Texteditor und **passe mindestens** den `SECRET_KEY` an:

```bash
# WICHTIG: Neuen Secret Key generieren!
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Kopiere den generierten Key in die `.env`-Datei bei `SECRET_KEY=...`

!!! warning "Sicherheit"
    Der Secret Key muss **geheim** bleiben und darf **nie** in Git committed werden!

---

### Schritt 5: Datenbank initialisieren

```bash
python src/backend/db.py
```

**Erwartete Ausgabe:**
```
Database initialized successfully!
Tables created.
```

Die Datenbankdatei wird erstellt unter: `storage/data/landly.db`

---

### Schritt 6: Backend starten

**Terminal 1 - Backend:**
```bash
python src/backend/main.py
```

**Erwartete Ausgabe:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

!!! success "Backend läuft"
    API ist erreichbar unter: [http://localhost:8000](http://localhost:8000)  
    API-Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Schritt 7: Frontend starten

**Terminal 2 - Frontend** (neues Terminal öffnen!):

```bash
# Virtuelle Umgebung aktivieren
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac

# Frontend starten
python src/main.py
```

Die Flet-App öffnet sich automatisch im Browser oder als Desktop-Anwendung.

!!! success "Fertig! 🎉"
    Landly läuft jetzt lokal und ist einsatzbereit.

---

## 🔧 Konfiguration

### .env-Datei

Die `.env`-Datei im Projektroot enthält alle wichtigen Konfigurationsparameter.

#### Relevante Parameter

##### Datenbank

```ini
DATABASE_URL=sqlite:///./storage/data/landly.db
```

**Beschreibung:** Verbindungsstring zur Datenbank  
**Standard:** SQLite-Datei im `storage/`-Ordner  
**Produktion:** `postgresql://user:password@host:5432/landly`

---

##### API-Server

```ini
API_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:5000,http://localhost:8080
DEBUG=True
```

- **API_URL**: Backend-Adresse (für Frontend-Zugriff)
- **CORS_ORIGINS**: Erlaubte Frontend-URLs (Komma-getrennt)
- **DEBUG**: Aktiviert Debug-Ausgaben (nur in Entwicklung!)

---

##### Authentifizierung

```ini
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

- **SECRET_KEY**: ⚠️ **WICHTIGSTER PARAMETER!** Geheimer Schlüssel für JWT-Signierung  
  - Mindestens 32 Zeichen
  - Niemals in Git committen
  - In Produktion: Zufällig generiert und sicher gespeichert
  
- **ALGORITHM**: Verschlüsselungsalgorithmus (Standard: HS256)

- **ACCESS_TOKEN_EXPIRE_MINUTES**: Token-Gültigkeit in Minuten

---

##### Logging

```ini
LOG_LEVEL=INFO
LOG_FILE=storage/logs/landly.log
```

- **LOG_LEVEL**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **LOG_FILE**: Pfad zur Log-Datei

---

##### Umgebung

```ini
ENVIRONMENT=development
```

**Optionen:**
- `development` - Entwicklung (SQLite, Debug aktiv)
- `testing` - Tests (separate Test-DB)
- `production` - Produktion (PostgreSQL, Debug aus)

---

### Sicherheitshinweise

!!! danger "NIEMALS in Git committen"
    - `.env`-Datei (steht in `.gitignore`)
    - Secret Keys
    - Passwörter
    - API-Keys
    - Produktive Zugangsdaten

!!! warning "Secret Key generieren"
    ```bash
    # Sicheren Key generieren
    python -c "import secrets; print(secrets.token_urlsafe(32))"
    
    # Oder in Python
    import secrets
    secrets.token_urlsafe(32)
    ```

!!! danger "Produktion"
    In Produktion:
    - `DEBUG=False` setzen
    - Starken Secret Key verwenden
    - PostgreSQL statt SQLite
    - HTTPS aktivieren
    - CORS_ORIGINS einschränken

---

### Konfiguration validieren

Prüfe, ob alle Einstellungen korrekt geladen werden:

```bash
python -c "from src.config import settings; print(f'Database: {settings.DATABASE_URL}'); print(f'Environment: {settings.ENVIRONMENT}')"
```

---

## 🧪 Testen der Installation

### 1. Backend-API testen

Öffne im Browser: [http://localhost:8000/docs](http://localhost:8000/docs)

Dort findest du die interaktive API-Dokumentation (Swagger UI).

**Teste einen Endpunkt:**
1. Öffne `/api/products` (GET)
2. Klicke "Try it out"
3. Klicke "Execute"
4. Erwartete Antwort: `200 OK` mit leerer Produktliste

---

### 2. Frontend testen

1. **Registrierung**: Erstelle einen Test-Account
2. **Login**: Melde dich an
3. **Produktsuche**: Gebe eine PLZ ein (z.B. 12345)

**Oder nutze Test-Accounts:**

| Rolle | E-Mail | Passwort |
|-------|--------|----------|
| Kunde | kunde@landly.de | Test123! |
| Landwirt | landwirt@landly.de | Test123! |
| Admin | admin@landly.de | Admin123! |

---

### 3. Testdaten laden (optional)

Falls vorhanden, lade Beispieldaten:

```bash
python scripts/load_testdata.py
```

Dies erstellt Demo-Produkte, Höfe und Bestellungen zum Testen.

---

## 🐛 Troubleshooting

### Problem: `ModuleNotFoundError`

**Lösung:**
```bash
# Prüfe, ob virtuelle Umgebung aktiv ist
# Sollte (.venv) im Prompt zeigen

# Abhängigkeiten neu installieren
pip install -r requirements.txt
```

---

### Problem: Port bereits belegt (8000)

**Lösung:**

**Option 1:** Anderen Port verwenden
```python
# In src/backend/main.py ändern
uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Option 2:** Prozess beenden
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID [PID] /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

---

### Problem: Datenbank-Fehler

**Lösung:**
```bash
# Datenbank löschen und neu erstellen
rm storage/data/landly.db
python src/backend/db.py
```

---

### Problem: "Permission denied" beim Aktivieren (.ps1)

**Lösung (Windows PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

---

### Problem: Frontend öffnet sich nicht

**Lösung:**
```bash
# Web-Version explizit starten
flet run --web src/main.py
```

---

## 📚 Nächste Schritte

Nach erfolgreicher Installation:

- **[Test-Accounts & Demo-Daten](dev/testdaten.md)** - Vordefinierte Test-Accounts nutzen
- **[API-Dokumentation](dev/api.md)** - Backend-Endpunkte erkunden
- **[Technische Strategie](dev/technische-strategie.md)** - Technologieentscheidungen und Workarounds verstehen
- **[User-Dokumentation](user/einfuehrung.md)** - Anwendung aus User-Sicht kennenlernen

---

## 💡 Tipps

!!! tip "Hot Reload"
    - **Backend**: Uvicorn erkennt Code-Änderungen automatisch (mit `--reload`)
    - **Frontend**: Flet unterstützt Hot Reload nativ

!!! tip "Mehrere Terminals"
    Nutze separate Terminals für Backend und Frontend, damit du beide Logs gleichzeitig siehst.

!!! tip "IDE Setup"
    **VS Code Extensions:**
    - Python (Microsoft)
    - Pylance
    - SQLite Viewer
    - REST Client

!!! tip "Dokumentation lokal"
    Starte die Dokumentation lokal:
    ```bash
    mkdocs serve
    ```
    Öffne: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📞 Support

Bei Problemen:

- **Dokumentation**: Siehe [Technische Strategie](dev/technische-strategie.md)
- **Issues**: GitHub Issues erstellen
- **E-Mail**: dev@landly.de
