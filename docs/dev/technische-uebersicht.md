# 👨‍💻 Entwickler-Dokumentation

Willkommen zur **technischen Dokumentation** von Landly!

Diese Dokumentation richtet sich an Entwickler:innen, die am Projekt arbeiten oder das System verstehen möchten.

---

## 🎯 Übersicht

Landly ist eine **regionale Onlineplattform** zur Vernetzung von Landwirten und Kund:innen.

Die Anwendung folgt einer **Client-Server-Architektur**:

- **Frontend**: Flet (Python-basiertes UI-Framework)
- **Backend**: FastAPI (REST-API)
- **Datenbank**: SQLite (Entwicklung) / PostgreSQL (Produktion)

---

## 📚 Dokumentationsbereiche

### Technische Grundlagen

- **[Technische Übersicht](technische-uebersicht.md)** – Architektur, Technologien, Entscheidungen
- **[Setup & Installation](setup.md)** – Projekt aufsetzen und lokal starten

### Datenmodellierung

- **[Logisches Modell](logisches-modell.md)** – Entitäten, Beziehungen, ER-Diagramm
- **[Datenbankschema](datenbankschema.md)** – Tabellenstruktur und SQL-Schema

### UML-Diagramme

- **[Use-Case-Diagramm](uml-usecase.md)** – Akteure und Anwendungsfälle
- **[Klassendiagramm](uml-klassen.md)** – Objektstruktur und Beziehungen
- **[Sequenzdiagramme](uml-sequenz.md)** – Ablauf wichtiger Prozesse

### Backend & API

- **[API-Dokumentation](api.md)** – REST-Endpunkte und Verwendung
- **[Backend-Logik](backend-logik.md)** – Wichtige Module und Funktionen
- **[Authentifizierung](authentifizierung.md)** – JWT, Rollen, Sicherheit

### Frontend

- **[Frontend-Struktur](frontend-struktur.md)** – Flet-Aufbau und Navigation
- **[UI-Komponenten](ui-komponenten.md)** – Wiederverwendbare Komponenten

---

## 🚀 Schnellstart für Entwickler

### 1. Repository klonen

```bash
git clone https://github.com/Landly-WIV/landly.git
cd landly
```

### 2. Virtuelle Umgebung erstellen

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. Datenbank initialisieren

```bash
python src/backend/db.py
```

### 5. Backend starten

```bash
python src/backend/main.py
```

### 6. Frontend starten

```bash
python src/main.py
```

Mehr Details: [Setup & Installation](setup.md)

---

## 🛠️ Entwicklungstools

| Tool | Zweck |
|------|-------|
| **VS Code** | IDE |
| **Git** | Versionskontrolle |
| **pytest** | Testing |
| **SQLAlchemy** | ORM |
| **Pydantic** | Datenvalidierung |
| **MkDocs** | Dokumentation |

---

## 📖 Coding Standards

### Python (PEP 8)

- **Einrückung**: 4 Leerzeichen
- **Zeilenlänge**: Max. 120 Zeichen
- **Naming**:
  - Funktionen/Variablen: `snake_case`
  - Klassen: `PascalCase`
  - Konstanten: `UPPER_CASE`

### Kommentare

```python
def get_products_in_radius(plz: str, radius_km: int):
    """
    Sucht Produkte in einem bestimmten Umkreis.
    
    Args:
        plz: Postleitzahl des Suchstandorts
        radius_km: Suchradius in Kilometern
    
    Returns:
        Liste von Produkten
    """
    pass
```

---

## 🧪 Testing

Tests werden mit **pytest** durchgeführt:

```bash
pytest tests/
```

Mehr dazu: [Testing](testing.md) (TODO)

---

## 📦 Deployment

Das Projekt wird über **GitHub Actions** automatisch deployed:

1. Commit → GitHub
2. CI/CD Pipeline läuft
3. Tests werden ausgeführt
4. Bei Erfolg: Deployment

Mehr dazu: [Deployment](deployment.md) (TODO)

---

## 🤝 Beitragen

Interessiert am Projekt mitzuarbeiten?

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/mein-feature`)
3. Committe deine Änderungen (`git commit -m 'Add some feature'`)
4. Pushe den Branch (`git push origin feature/mein-feature`)
5. Erstelle einen Pull Request

---

## 📞 Kontakt

**Projektteam:**

- Lucas – [GitHub](https://github.com/lucas)
- [Weitere Teammitglieder einfügen]

**Repository:**  
[https://github.com/Landly-WIV/landly](https://github.com/Landly-WIV/landly)
