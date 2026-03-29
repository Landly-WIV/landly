# Technische Strategie

Diese Seite dokumentiert die methodische Begründung der technischen Entscheidungen fur Landly.
Fokus: Technologie-Stack, Alternativen, Skalierbarkeit, Wartbarkeit, Performance sowie konkrete Herausforderungen mit Workarounds.

---

## 1. Technologie-Stack

| Bereich | Eingesetzte Technologie | Ziel im Projekt |
|---|---|---|
| Frontend | Flet | Schnelle UI-Entwicklung in Python ohne separaten JS-Stack |
| Backend | FastAPI | Klare, performante REST-API mit OpenAPI-Dokumentation |
| Persistenz | SQLite (Entwicklung), PostgreSQL (Produktion) | Einfaches Setup lokal, robuste Datenhaltung in Produktion |
| ORM | SQLAlchemy | Abstraktion zwischen Code und Datenbank, leichter DB-Wechsel |
| Authentifizierung | JWT (python-jose) | Stateless Auth fur API und bessere horizontale Skalierung |
| Deployment | Render / Docker | Reproduzierbare Deployments und standardisierte Laufzeit |

---

## 2. Begrundung des Stacks mit Alternativen

### Frontend: Flet (statt React/Vue)

- Gewahlt, weil das Team durchgehend mit Python arbeiten kann.
- Vorteil fur Wartbarkeit: einheitliche Sprache, geringere kognitive Last, weniger Kontextwechsel.
- Vorteil fur Time-to-Market: schnelle Prototyping-Zyklen.
- Nachteil gegenuber React/Vue: kleineres Ecosystem und weniger UI-Integrationen.

### Backend: FastAPI (statt Flask/Django REST)

- Gewahlt wegen guter Performance (ASGI), klarer Typisierung und automatischer API-Doku.
- Vorteil fur Wartbarkeit: Pydantic-Validierung plus Typhinweise reduzieren Fehler an den Schnittstellen.
- Vorteil fur Skalierbarkeit: stateless API-Design und guter Betrieb hinter Reverse Proxy.
- Alternative Flask: einfacher Kern, aber mehr manuelle Entscheidungen fur Validierung und Dokumentation.
- Alternative Django REST: sehr umfangreich, fur das aktuelle Projekt eher overhead.

### Datenbank: SQLite lokal, PostgreSQL produktiv

- SQLite wurde fur lokale Entwicklung gewahlt, um Setup-Hurden klein zu halten.
- PostgreSQL ist fur Produktion vorgesehen wegen Concurrency, Stabilitat und Index-Features.
- Vorteil fur Wartbarkeit: SQLAlchemy reduziert Kopplung an ein konkretes DB-System.
- Alternative "nur SQLite": zu begrenzt fur parallelere Last und langfristiges Wachstum.

### Auth: JWT (statt serverseitiger Sessions)

- JWT wurde fur stateless Auth gewahlt.
- Vorteil fur Skalierbarkeit: mehrere Backend-Instanzen konnen ohne Session-Sharing betrieben werden.
- Nachteil: Token-Lifecycle und sichere Speicherung mussen sauber umgesetzt sein.

---

## 3. Bewertungsdimensionen

### Skalierbarkeit

- Backend ist stateless ausgelegt; horizontale Skalierung ist moglich.
- API und Frontend sind getrennt deploybar.
- Datenbankstrategie erlaubt Upgrade von SQLite auf PostgreSQL ohne fachliche Logik neu zu schreiben.
- Indexbasierte Abfragen fur haufige Such- und Filteroperationen sind vorgesehen.

### Wartbarkeit

- Klare Modultrennung (Frontend-Seiten, API-Routen, Datenzugriff).
- Typisierte Request/Response-Modelle im Backend.
- Einheitlicher Python-Stack reduziert Einarbeitungsaufwand im Team.
- Konsistente Konfiguration uber Umgebungsvariablen.

### Performance

- FastAPI/ASGI fur niedrige Latenzen bei API-Aufrufen.
- Datenbank-Indizes fur kritische Filterfelder.
- Begrenzung von Listenmengen (Pagination-Ansatz) fur stabile Antwortzeiten.
- Trennung von Entwicklung (SQLite) und Produktion (PostgreSQL), damit Lastspitzen sauber abgefangen werden konnen.

---

## 4. Herausforderungen und konkrete Workarounds

### Herausforderung A: Unterschiedliche Entwicklungsumgebungen (Windows/macOS/Linux)

Problem:
- Aktivierung der virtuellen Umgebung und Shell-Verhalten unterscheiden sich je OS.

Workaround:
- Dokumentation mit getrennten Befehlen pro Plattform.
- Einheitliche `.env.example` bereitgestellt, um Konfigurationsfehler zu reduzieren.

Ergebnis:
- Schnellere, reproduzierbare lokale Setups ohne individuelle Sonderwege.

### Herausforderung B: CORS-Probleme zwischen Frontend und Backend lokal

Problem:
- Browser blockiert Requests, wenn Frontend- und Backend-Origin nicht sauber freigegeben sind.

Workaround:
- Explizite CORS-Konfiguration im Backend fur lokale Entwicklungs-Origins.
- API-URL zentral uber Umgebungsvariablen konfiguriert.

Ergebnis:
- Stabiler lokaler Entwicklungsfluss mit weniger "funktioniert nur bei mir"-Fehlern.

### Herausforderung C: SQLite-Limits bei parallelem Zugriff

Problem:
- Unter hoherer Parallelitat konnen Locking-Effekte auftreten.

Workaround:
- SQLite nur fur lokale Entwicklung nutzen.
- Fruhzeitige Kompatibilitat zu PostgreSQL uber SQLAlchemy sicherstellen.
- Produktionsprofil auf PostgreSQL ausrichten.

Ergebnis:
- Gute Developer Experience lokal und tragfahiger Betrieb in Produktion.

### Herausforderung D: API-Integration im Frontend (Token-handling)

Problem:
- Fehlende/abgelaufene Tokens fuhrten zu uneinheitlichem Fehlerverhalten.

Workaround:
- Zentraler API-Call-Pfad mit einheitlichem Authorization-Header.
- Standardisierte Behandlung von 401/403-Ruckgaben (erneuter Login-Flow).

Ergebnis:
- Vorhersehbares Auth-Verhalten und weniger supportintensive Edge Cases.

---

## 5. Fazit der technischen Strategie

Der gewahlte Stack optimiert die Balance aus schneller Entwicklung, guter Wartbarkeit und skalierbarem Betrieb:

- Flet/FastAPI fur hohe Umsetzungsgeschwindigkeit im Team.
- SQLAlchemy fur geringe Kopplung und bessere Evolvierbarkeit.
- SQLite lokal und PostgreSQL produktiv als pragmatischer Skalierungspfad.
- Konkrete Workarounds fur bekannte Probleme sind dokumentiert und operationalisierbar.
