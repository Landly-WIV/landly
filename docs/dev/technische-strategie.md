# 🎯 Technische Strategie

Diese Seite dokumentiert die technischen Entscheidungen, Überlegungen und Strategien hinter Landly.

---

## 🛠️ Technologie-Stack

### Übersicht

| Komponente | Technologie | Version |
|------------|-------------|---------|
| **Frontend** | Flet | 0.24.x |
| **Backend** | FastAPI | 0.110.x |
| **Datenbank** | SQLite / PostgreSQL | - |
| **ORM** | SQLAlchemy | 2.0.x |
| **Auth** | JWT (python-jose) | 3.3.x |
| **Deployment** | Docker, Render | - |
| **Dokumentation** | MkDocs Material | 9.x |

---

## 💡 Technologie-Begründungen

### Warum Flet?

Flet wurde als Frontend-Framework gewählt aus folgenden Gründen:

✅ **Python-basiert**
- Einheitliche Sprache für Frontend und Backend
- Keine separate JavaScript-Entwicklung nötig
- Geringerer Einarbeitungsaufwand für das Team

✅ **Cross-Platform**
- Ein Codebase für Desktop, Web und Mobile
- Native Kompilierung für verschiedene Plattformen möglich
- Schnellere Entwicklung durch Code-Wiederverwendung

✅ **Schnelle Prototyping**
- Einfache UI-Komponenten
- Hot-Reload für schnelle Iterationen
- Gute Dokumentation und Community

✅ **Moderne UI**
- Material Design out-of-the-box
- Responsive Layouts
- Ansprechende visuelle Komponenten

**Nachteile (bewusst in Kauf genommen):**
- Kleinere Community als React/Vue
- Weniger Drittanbieter-Bibliotheken
- Neueres Framework (höheres Risiko für Breaking Changes)

---

### Warum FastAPI?

FastAPI ist die ideale Wahl für moderne Python-APIs:

✅ **Performance**
- Eines der schnellsten Python-Frameworks (basiert auf Starlette/ASGI)
- Asynchrone Verarbeitung
- Geeignet für hohe Last

✅ **Automatische API-Dokumentation**
- Swagger UI und ReDoc out-of-the-box
- OpenAPI-Standard
- Erleichtert Frontend-Integration und Testing

✅ **Type Safety**
- Pydantic für Datenvalidierung
- Type Hints für bessere IDE-Unterstützung
- Weniger Runtime-Fehler

✅ **Modern und Developer-Friendly**
- Einfache Dependency Injection
- Intuitive Routing-Syntax
- Hervorragende Dokumentation

**Alternative Frameworks (abgelehnt):**
- **Django REST Framework**: Zu umfangreich für unsere Anforderungen
- **Flask**: Weniger moderne Features, keine automatische Validierung
- **Node.js + Express**: Würde andere Programmiersprache erfordern

---

### Warum SQLite → PostgreSQL?

**Entwicklung: SQLite**

✅ Einfaches Setup ohne zusätzliche Services
✅ Datei-basiert, keine Konfiguration nötig
✅ Perfekt für lokale Entwicklung und Testing

**Produktion: PostgreSQL**

✅ Bessere Performance bei vielen gleichzeitigen Zugriffen
✅ Bessere Transaktionssicherheit
✅ Erweiterte Features (JSON, Full-Text-Search)
✅ Skalierbar für Wachstum

**Migration:**
Dank SQLAlchemy ORM ist der Wechsel ohne Code-Änderungen möglich.

---

## 🏗️ Architektur-Entscheidungen

### Client-Server-Architektur

Wir nutzen eine klassische **2-Tier-Architektur**:

```
Frontend (Flet) ←→ Backend (FastAPI) ←→ Datenbank
```

**Vorteile:**
- Klare Trennung von Verantwortlichkeiten
- Frontend und Backend können unabhängig entwickelt werden
- Einfache Wartbarkeit und Testbarkeit
- Backend ist wiederverwendbar (z.B. für mobile App)

**Alternative (abgelehnt):**
- **Monolith**: Weniger flexibel, schwerer skalierbar
- **Microservices**: Zu komplex für Projektgröße

---

### RESTful API

Kommunikation zwischen Frontend und Backend erfolgt über **REST-API** mit JSON.

**Vorteile:**
- Standardisiert und weit verbreitet
- Einfach zu verstehen und zu nutzen
- Gute Tool-Unterstützung (Swagger, Postman)
- Stateless (einfacher zu skalieren)

**Alternative (abgelehnt):**
- **GraphQL**: Zu komplex für einfache CRUD-Operationen
- **gRPC**: Weniger zugänglich, schwieriger zu debuggen

---

### JWT-basierte Authentifizierung

Token-basierte Auth mit **JSON Web Tokens (JWT)**.

**Vorteile:**
- Stateless (Server muss keine Sessions speichern)
- Skalierbar
- Kann Benutzerinformationen enthalten
- Standard-Lösung für moderne APIs

**Alternative (abgelehnt):**
- **Session-based Auth**: Weniger skalierbar, erfordert Server-State
- **OAuth2**: Zu komplex für internes System

---

## 🎨 Design-Patterns

### Backend: Repository Pattern

Datenbank-Zugriffe werden über **Repository-Klassen** abstrahiert:

```python
class ProductRepository:
    def get_all(self, filters: dict) -> List[Product]:
        pass
    
    def get_by_id(self, id: int) -> Product:
        pass
    
    def create(self, data: ProductCreate) -> Product:
        pass
```

**Vorteile:**
- Trennung von Business-Logik und Datenzugriff
- Einfach testbar (Mock-Repositories)
- Datenbankwechsel ohne Änderung der Business-Logik

---

### Frontend: Page-Based Architecture

Jede Seite ist eine eigene Python-Datei mit eigenem State:

```
src/
  ├── landingpage.py
  ├── products.py
  ├── warenkorb.py
  └── navbar.py
```

**Vorteile:**
- Übersichtliche Struktur
- Einfaches Routing
- Komponenten-Wiederverwendung

---

### Dependency Injection

FastAPI nutzt DI für saubere Abhängigkeiten:

```python
@app.get("/products")
def get_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pass
```

**Vorteile:**
- Testbarkeit (Dependencies können gemockt werden)
- Sauberer Code ohne globale Variablen
- Automatische Validierung

---

## 🔒 Sicherheit

### Passwort-Hashing

Passwörter werden mit **bcrypt** gehasht:

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

✅ Kein Plaintext speichern
✅ Salt automatisch
✅ Brute-Force-resistent

---

### SQL-Injection-Schutz

SQLAlchemy ORM schützt automatisch vor SQL-Injection:

```python
# Sicher
products = db.query(Product).filter(Product.name == user_input).all()

# NICHT verwenden
db.execute(f"SELECT * FROM products WHERE name = '{user_input}'")
```

---

### CORS-Configuration

Cross-Origin Resource Sharing wird für Frontend-Zugriff konfiguriert:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],  # Flet-Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📈 Skalierbarkeit

### Horizontale Skalierung

Das Backend ist **stateless** und kann horizontal skaliert werden:

```
Load Balancer
    ↓
[Backend 1] [Backend 2] [Backend 3]
    ↓           ↓           ↓
    PostgreSQL (Single Instance)
```

---

### Datenbank-Optimierung

Wichtige Indizes sind definiert:

```sql
CREATE INDEX idx_products_plz ON products(plz);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_orders_customer ON orders(customer_id);
```

---

### Caching (zukünftig)

Für häufig abgerufene Daten kann **Redis** als Cache eingesetzt werden:

```python
# Zukünftig möglich
@cache(expire=300)  # 5 Minuten Cache
def get_products_by_plz(plz: str):
    pass
```

---

## 🧪 Wartbarkeit

### Code-Standards

- **PEP 8** für Python-Code
- **Type Hints** überall verwenden
- **Docstrings** für alle Funktionen
- **Kommentare** für komplexe Logik

---

### Testing-Strategie

```
tests/
  ├── unit/          # Einzelne Funktionen
  ├── integration/   # API-Tests
  └── e2e/           # End-to-End (Frontend → Backend)
```

**Tools:**
- `pytest` für Unit-Tests
- `pytest-asyncio` für async Tests
- `httpx` für API-Tests

---

### CI/CD Pipeline

```yaml
# GitHub Actions Workflow
1. Code Push
2. Linting (flake8, black)
3. Type Checking (mypy)
4. Unit Tests
5. Integration Tests
6. Build Docker Image
7. Deploy to Render
```

---

## ⚡ Performance

### Angestrebte Metriken

| Metrik | Zielwert |
|--------|----------|
| API Response Time | < 200ms |
| Produktsuche (25km) | < 500ms |
| Seiten-Load (Frontend) | < 2s |
| Gleichzeitige Benutzer | 100+ |

---

### Optimierungen

✅ **Datenbank-Indizes** für schnelle Suche
✅ **Lazy Loading** für große Datenmengen
✅ **Pagination** für Listen (max. 50 Einträge)
✅ **Asynchrone API-Calls** im Backend
✅ **Connection Pooling** für Datenbank

---

## 🚧 Herausforderungen & Lösungen

### 1. Umkreissuche nach PLZ

**Problem:**
SQLite hat keine native Geo-Suche.

**Lösung:**
- PLZ-Datenbank mit Koordinaten importieren
- Haversine-Formel für Distanzberechnung
- Vorab-Filterung nach PLZ-Präfix

```python
def calculate_distance(lat1, lon1, lat2, lon2) -> float:
    # Haversine-Formel
    pass
```

---

### 2. Flet Web-Performance

**Problem:**
Flet Web ist langsamer als Desktop-Version.

**Lösung:**
- Lazy Loading für Produktlisten
- Virtuelle Scrolling-Container
- Bilder komprimieren
- Minimale State-Updates

---

### 3. Authentifizierung in Flet

**Problem:**
Flet hat keine native Auth-Lösung.

**Lösung:**
- JWT-Token in `page.client_storage` speichern
- Token bei jedem API-Call im Header mitschicken
- Automatisches Refresh bei Ablauf

```python
def make_api_call(endpoint: str):
    token = page.client_storage.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, headers=headers)
    return response.json()
```

---

## 🔮 Zukünftige Erweiterungen

Technologien und Features, die später hinzugefügt werden könnten:

### Phase 2
- [ ] Redis für Caching
- [ ] Elasticsearch für erweiterte Suche
- [ ] WebSockets für Live-Updates (Bestellungen)
- [ ] Mobile Apps (iOS/Android via Flet build)

### Phase 3
- [ ] Payment-Integration (Stripe)
- [ ] E-Mail-Versand (SendGrid)
- [ ] Image-Upload und CDN
- [ ] Analytics & Monitoring (Sentry)

---

## 📚 Ressourcen & Dokumentation

### Offizielle Docs
- [Flet Dokumentation](https://flet.dev/docs/)
- [FastAPI Dokumentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Dokumentation](https://docs.sqlalchemy.org/)

### Tutorials & Guides
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [Python Type Hints](https://realpython.com/python-type-checking/)

---

## 🤝 Team-Entscheidungen

Alle technischen Entscheidungen werden im Team diskutiert und dokumentiert:

| Datum | Entscheidung | Begründung |
|-------|--------------|------------|
| 2025-10-15 | Flet als Frontend | Python-only Stack gewünscht |
| 2025-10-20 | FastAPI statt Flask | Moderne Features, Auto-Docs |
| 2025-11-05 | JWT-Auth | Stateless, skalierbar |
| 2026-01-10 | PostgreSQL für Produktion | Bessere Performance |

---

## 📞 Technische Ansprechpartner

Bei technischen Fragen:

- **Backend**: Lucas
- **Frontend**: [Name]
- **Datenbank**: [Name]
- **Deployment**: [Name]
