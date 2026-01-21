# ⚙️ Setup & Installation

Diese Anleitung beschreibt, wie du das Projekt lokal aufsetzen und starten kannst.

---

## 📋 Voraussetzungen

Stelle sicher, dass folgende Software installiert ist:

| Software | Version | Link |
|----------|---------|------|
| **Python** | 3.10+ | [python.org](https://python.org) |
| **Git** | Latest | [git-scm.com](https://git-scm.com) |
| **VS Code** | Optional | [code.visualstudio.com](https://code.visualstudio.com) |

---

## 🚀 Installation

### 1. Repository klonen

```bash
git clone https://github.com/Landly-WIV/landly.git
cd landly
```

### 2. Virtuelle Umgebung erstellen

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

Falls `requirements.txt` nicht existiert, installiere manuell:

```bash
pip install flet fastapi uvicorn sqlalchemy pydantic python-jose passlib bcrypt
```

---

## 🗄️ Datenbank einrichten

### SQLite (Standard)

Die Datenbank wird automatisch beim ersten Start erstellt:

```bash
python src/backend/db.py
```

### PostgreSQL (Optional, für Produktion)

1. **PostgreSQL installieren**: [postgresql.org](https://www.postgresql.org/)

2. **Datenbank erstellen:**
   ```sql
   CREATE DATABASE landly;
   ```

3. **Connection String anpassen** in `src/backend/db.py`:
   ```python
   DATABASE_URL = "postgresql://user:password@localhost/landly"
   ```

4. **Migrations ausführen:**
   ```bash
   python src/backend/db.py
   ```

---

## ▶️ Projekt starten

### Backend starten

Das Backend läuft auf Port **8000**:

```bash
cd src/backend
python main.py
```

Oder mit **uvicorn**:
```bash
uvicorn src.backend.main:app --reload
```

**API-Dokumentation:**  
→ [http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend starten

Das Frontend wird mit Flet gestartet:

```bash
python src/main.py
```

Die App öffnet sich automatisch im Standardbrowser.

---

## 🧪 Tests ausführen

```bash
pytest tests/
```

Mit Coverage-Report:
```bash
pytest --cov=src tests/
```

---

## 📦 Projektstruktur

```
landly/
├── .venv/                  # Virtuelle Umgebung
├── src/
│   ├── main.py            # Frontend-Einstiegspunkt
│   ├── backend/
│   │   ├── main.py        # Backend-Einstiegspunkt
│   │   ├── db.py          # Datenbank-Setup
│   │   ├── models.py      # SQLAlchemy-Modelle
│   │   ├── crud.py        # CRUD-Operationen
│   │   └── ...
│   ├── content.py         # UI-Inhalte
│   ├── navbar.py          # Navigation
│   └── ...
├── docs/                   # MkDocs-Dokumentation
├── tests/                  # Tests
├── requirements.txt        # Python-Dependencies
├── mkdocs.yml             # MkDocs-Konfiguration
└── README.md
```

---

## 🔧 Entwicklungsumgebung

### VS Code Extensions (empfohlen)

- **Python** (Microsoft)
- **Pylance** (Microsoft)
- **SQLite Viewer**
- **REST Client** (für API-Tests)

### Linting & Formatting

**Black** (Code Formatter):
```bash
pip install black
black src/
```

**Flake8** (Linter):
```bash
pip install flake8
flake8 src/
```

---

## 🐳 Docker (Optional)

### Docker-Container bauen

```bash
docker build -t landly .
```

### Container starten

```bash
docker run -p 8000:8000 landly
```

---

## 🌍 Umgebungsvariablen

Erstelle eine `.env`-Datei im Projektroot:

```env
# Datenbank
DATABASE_URL=sqlite:///./landly.db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App
DEBUG=True
```

---

## 🛠️ Troubleshooting

### Problem: `ModuleNotFoundError`

**Lösung:**  
Stelle sicher, dass die virtuelle Umgebung aktiviert ist und alle Dependencies installiert sind:

```bash
pip install -r requirements.txt
```

### Problem: Datenbank-Fehler

**Lösung:**  
Lösche die Datenbank und erstelle sie neu:

```bash
rm landly.db
python src/backend/db.py
```

### Problem: Port bereits belegt

**Lösung:**  
Ändere den Port in `src/backend/main.py`:

```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Statt 8000
```

---

## 📚 Nächste Schritte

Nach der Installation kannst du:

- **[Logisches Modell](logisches-modell.md)** – Datenmodell verstehen
- **[API-Dokumentation](api.md)** – Backend-Endpunkte erkunden
- **[UML-Diagramme](uml-usecase.md)** – System-Design verstehen

---

## 💡 Tipps

!!! tip "Hot Reload"
    Backend: `uvicorn --reload` aktiviert automatisches Neuladen bei Code-Änderungen.
    
    Frontend: Flet unterstützt Hot Reload nativ.

!!! tip "Debugging"
    Nutze VS Code's Debugger für Python. Konfiguration in `.vscode/launch.json`.
