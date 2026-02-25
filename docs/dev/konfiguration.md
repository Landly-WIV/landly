# ⚙️ Konfiguration

Diese Seite beschreibt die Konfiguration von Landly über Umgebungsvariablen und Config-Dateien.

---

## 📁 .env-Datei

Die Hauptkonfiguration erfolgt über eine `.env`-Datei im Root-Verzeichnis.

### .env erstellen

1. **Vorlage kopieren:**
   ```bash
   cp .env.example .env
   ```

2. **Werte anpassen** (siehe unten)

---

## 🔧 Umgebungsvariablen

### Datenbank

```ini
# SQLite (Entwicklung)
DATABASE_URL=sqlite:///./storage/data/landly.db

# PostgreSQL (Produktion)
# DATABASE_URL=postgresql://user:password@localhost:5432/landly
```

**Beschreibung:**
- Verbindungsstring zur Datenbank
- SQLite für lokale Entwicklung
- PostgreSQL für Produktion

---

### API-Konfiguration

```ini
# API Base URL
API_URL=http://localhost:8000

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:5000,http://localhost:8080

# Debug-Modus
DEBUG=True
```

**Beschreibung:**
- `API_URL`: Basis-URL des Backends
- `CORS_ORIGINS`: Erlaubte Frontend-URLs
- `DEBUG`: Aktiviert Debug-Ausgaben

---

### Authentifizierung

```ini
# JWT Secret Key (NIEMALS in Git committen!)
SECRET_KEY=your-super-secret-key-change-this-in-production

# JWT Algorithm
ALGORITHM=HS256

# Token Expiration (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Beschreibung:**
- `SECRET_KEY`: Geheimer Schlüssel für JWT-Signierung (mindestens 32 Zeichen)
- `ALGORITHM`: Verschlüsselungsalgorithmus
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token-Gültigkeit in Minuten

**Secret Key generieren:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

### E-Mail (optional)

```ini
# E-Mail-Konfiguration (für Benachrichtigungen)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=deine-email@gmail.com
SMTP_PASSWORD=dein-app-passwort
SMTP_FROM=noreply@landly.de
```

**Beschreibung:**
- SMTP-Server für E-Mail-Versand
- Aktuell optional, für zukünftige Features

---

### Externe APIs

```ini
# Google Maps API (für Geolocation)
# GOOGLE_MAPS_API_KEY=your-api-key

# PLZ-Datenbank API
# PLZ_API_URL=https://api.zippopotam.us/de/
```

**Beschreibung:**
- Optional für erweiterte Geo-Funktionen
- Aktuell nutzen wir lokale PLZ-Datenbank

---

### Logging

```ini
# Log Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Log-Datei
LOG_FILE=storage/logs/landly.log
```

---

### Produktion

```ini
# Umgebung
ENVIRONMENT=production

# Render/Deployment
RENDER_EXTERNAL_URL=https://landly.onrender.com

# Sicherheit
HTTPS_ONLY=True
```

---

## 📄 .env.example

Beispiel-Datei für Entwickler (wird in Git committed):

```ini
# === DATENBANK ===
DATABASE_URL=sqlite:///./storage/data/landly.db

# === API ===
API_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:5000
DEBUG=True

# === AUTHENTIFIZIERUNG ===
SECRET_KEY=change-this-to-a-random-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# === E-MAIL (optional) ===
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=
# SMTP_PASSWORD=
# SMTP_FROM=noreply@landly.de

# === LOGGING ===
LOG_LEVEL=INFO
LOG_FILE=storage/logs/landly.log

# === ENVIRONMENT ===
ENVIRONMENT=development
```

---

## 🐍 config.py

Zentrale Konfigurationsdatei in Python:

```python
# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Datenbank
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./storage/data/landly.db")
    
    # API
    API_URL: str = os.getenv("API_URL", "http://localhost:8000")
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    
    # Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:5000").split(",")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "storage/logs/landly.log")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

settings = Settings()
```

**Verwendung:**
```python
from src.config import settings

if settings.DEBUG:
    print("Debug-Modus aktiv")
```

---

## 🔒 Sicherheit

### ⚠️ NIEMALS in Git committen:

- `.env` (steht in `.gitignore`)
- Produktive Secret Keys
- Datenbank-Passwörter
- API-Keys

### ✅ In Git committen:

- `.env.example` (mit Platzhaltern)
- `config.py` (ohne Secrets)

---

## 🌍 Umgebungen

### Entwicklung (Development)

```ini
ENVIRONMENT=development
DEBUG=True
DATABASE_URL=sqlite:///./storage/data/landly.db
API_URL=http://localhost:8000
```

**Aktiviert:**
- Debug-Ausgaben
- Hot-Reload
- Ausführliche Fehlermeldungen
- SQLite-Datenbank

---

### Testing

```ini
ENVIRONMENT=testing
DEBUG=True
DATABASE_URL=sqlite:///./storage/data/test.db
API_URL=http://localhost:8000
```

**Aktiviert:**
- Separate Test-Datenbank
- Schnellere Token-Expiration
- Mock-Services

---

### Produktion (Production)

```ini
ENVIRONMENT=production
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:5432/landly
API_URL=https://api.landly.de
HTTPS_ONLY=True
SECRET_KEY=super-secure-random-key
```

**Aktiviert:**
- PostgreSQL
- HTTPS-Only
- Reduzierte Logging
- Sicherheits-Features

---

## 🔄 Konfiguration neu laden

Nach Änderungen an `.env`:

### Backend neu starten

```bash
# Terminal beenden (Ctrl+C)
python src/backend/main.py
```

### Frontend neu starten

```bash
# Terminal beenden (Ctrl+C)
python src/main.py
```

---

## 📦 Abhängigkeiten

Installiere `python-dotenv` für .env-Support:

```bash
pip install python-dotenv
```

---

## 🧪 Konfiguration testen

Prüfe ob alle Umgebungsvariablen korrekt geladen werden:

```bash
python -c "from src.config import settings; print(settings.DATABASE_URL)"
```

---

## 🐳 Docker-Konfiguration

### docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=${DEBUG}
    env_file:
      - .env
    volumes:
      - ./storage:/app/storage

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=landly
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=landly
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Starten:**
```bash
docker-compose up -d
```

---

## 📋 Konfiguration validieren

Script zum Prüfen der Konfiguration:

```python
# scripts/validate_config.py
from src.config import settings
import sys

def validate():
    errors = []
    
    # Secret Key prüfen
    if settings.SECRET_KEY == "default-secret-key":
        errors.append("❌ SECRET_KEY ist Standard-Wert!")
    
    if len(settings.SECRET_KEY) < 32:
        errors.append("❌ SECRET_KEY ist zu kurz (min. 32 Zeichen)")
    
    # Datenbank prüfen
    if settings.is_production and "sqlite" in settings.DATABASE_URL:
        errors.append("⚠️ SQLite in Produktion nicht empfohlen")
    
    # Debug-Modus
    if settings.is_production and settings.DEBUG:
        errors.append("❌ DEBUG sollte in Produktion False sein")
    
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    else:
        print("✅ Konfiguration ist valide")

if __name__ == "__main__":
    validate()
```

**Ausführen:**
```bash
python scripts/validate_config.py
```

---

## 📖 Weitere Konfigurationen

### requirements.txt

Abhängigkeiten für verschiedene Umgebungen:

```
# requirements.txt (Produktion)
flet==0.24.0
fastapi==0.110.0
uvicorn==0.27.0
sqlalchemy==2.0.25
python-jose==3.3.0
passlib==1.7.4
python-dotenv==1.0.0
```

```
# requirements-dev.txt (Entwicklung)
-r requirements.txt
pytest==7.4.4
black==24.1.0
flake8==7.0.0
mypy==1.8.0
```

---

## 🔗 Weiterführende Links

- [Setup-Anleitung](setup.md)
- [Deployment](deployment.md)
- [Sicherheit](sicherheit.md)

---

## 📞 Hilfe

Bei Problemen mit der Konfiguration:

**Dokumentation:** [docs/dev/setup.md](setup.md)  
**Support:** dev@landly.de  
**Issue Tracker:** GitHub Issues
