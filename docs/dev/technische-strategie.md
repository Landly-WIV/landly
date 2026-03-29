# Technische Strategie

Diese Seite dokumentiert die methodische Begründung der technischen Entscheidungen für Landly.
Fokus: Technologie-Stack, Alternativen, Skalierbarkeit, Wartbarkeit, Performance sowie konkrete Herausforderungen mit Workarounds.

---

## 1. Technologie-Stack

| Bereich | Eingesetzte Technologie | Ziel im Projekt |
|---|---|---|
| Frontend | Flet | Schnelle UI-Entwicklung in Python ohne separaten JS-Stack |
| Backend | FastAPI | Klare, performante REST-API mit OpenAPI-Dokumentation |
| Persistenz | SQLite (Entwicklung), PostgreSQL (Produktion) | Einfaches Setup lokal, robuste Datenhaltung in Produktion |
| ORM | SQLAlchemy | Abstraktion zwischen Code und Datenbank, leichter DB-Wechsel |
| Authentifizierung | JWT (python-jose) | Stateless Auth für API und bessere horizontale Skalierung |
| Deployment | Render / Docker | Reproduzierbare Deployments und standardisierte Laufzeit |

---

## 2. Begründung des Stacks mit Alternativen

### Frontend: Flet (statt React/Vue)

- Gewählt, weil das Team durchgehend mit Python arbeiten kann.
- Vorteil für Wartbarkeit: einheitliche Sprache, geringere kognitive Last, weniger Kontextwechsel.
- Vorteil für Time-to-Market: schnelle Prototyping-Zyklen.
- Nachteil gegenüber React/Vue: kleineres Ecosystem und weniger UI-Integrationen.

### Backend: FastAPI (statt Flask/Django REST)

- Gewählt wegen guter Performance (ASGI), klarer Typisierung und automatischer API-Doku.
- Vorteil für Wartbarkeit: Pydantic-Validierung plus Typhinweise reduzieren Fehler an den Schnittstellen.
- Vorteil für Skalierbarkeit: stateless API-Design und guter Betrieb hinter Reverse Proxy.
- Alternative Flask: einfacher Kern, aber mehr manuelle Entscheidungen für Validierung und Dokumentation.
- Alternative Django REST: sehr umfangreich, für das aktuelle Projekt eher Overhead.

### Datenbank: SQLite lokal, PostgreSQL produktiv

- SQLite wurde für lokale Entwicklung gewählt, um Setup-Hürden klein zu halten.
- PostgreSQL ist für Produktion vorgesehen wegen Concurrency, Stabilität und Index-Features.
- Vorteil für Wartbarkeit: SQLAlchemy reduziert Kopplung an ein konkretes DB-System.
- Alternative "nur SQLite": zu begrenzt für parallelere Last und langfristiges Wachstum.

### Auth: JWT (statt serverseitiger Sessions)

- JWT wurde für stateless Auth gewählt.
- Vorteil für Skalierbarkeit: mehrere Backend-Instanzen können ohne Session-Sharing betrieben werden.
- Nachteil: Token-Lifecycle und sichere Speicherung müssen sauber umgesetzt sein.

---

## 3. Bewertungsdimensionen

### Skalierbarkeit

- Backend ist stateless ausgelegt; horizontale Skalierung ist möglich.
- API und Frontend sind getrennt deploybar.
- Datenbankstrategie erlaubt Upgrade von SQLite auf PostgreSQL ohne fachliche Logik neu zu schreiben.
- Indexbasierte Abfragen für häufige Such- und Filteroperationen sind vorgesehen.

### Wartbarkeit

- Klare Modultrennung (Frontend-Seiten, API-Routen, Datenzugriff).
- Typisierte Request/Response-Modelle im Backend.
- Einheitlicher Python-Stack reduziert Einarbeitungsaufwand im Team.
- Konsistente Konfiguration über Umgebungsvariablen.

### Performance

- FastAPI/ASGI für niedrige Latenzen bei API-Aufrufen.
- Datenbank-Indizes für kritische Filterfelder.
- Begrenzung von Listenmengen (Pagination-Ansatz) für stabile Antwortzeiten.
- Trennung von Entwicklung (SQLite) und Produktion (PostgreSQL), damit Lastspitzen sauber abgefangen werden können.

---

## 4. Herausforderungen und konkrete Workarounds

### Herausforderung A: Unterschiedliche Entwicklungsumgebungen (Windows/macOS/Linux)

**Problem:**
- Aktivierung der virtuellen Umgebung und Shell-Verhalten unterscheiden sich je OS.

**Workaround:**
- Dokumentation mit getrennten Befehlen pro Plattform.
- Einheitliche `.env.example` bereitgestellt, um Konfigurationsfehler zu reduzieren.

**Ergebnis:**
- Schnellere, reproduzierbare lokale Setups ohne individuelle Sonderwege.

### Herausforderung B: CORS-Probleme zwischen Frontend und Backend lokal

**Problem:**
- Browser blockiert Requests, wenn Frontend- und Backend-Origin nicht sauber freigegeben sind.

**Workaround:**
- Explizite CORS-Konfiguration im Backend für lokale Entwicklungs-Origins.
- API-URL zentral über Umgebungsvariablen konfiguriert.

**Ergebnis:**
- Stabiler lokaler Entwicklungsfluss mit weniger "funktioniert nur bei mir"-Fehlern.

### Herausforderung C: SQLite-Limits bei parallelem Zugriff

**Problem:**
- Unter höherer Parallelität können Locking-Effekte auftreten.

**Workaround:**
- SQLite nur für lokale Entwicklung nutzen.
- Frühzeitige Kompatibilität zu PostgreSQL über SQLAlchemy sicherstellen.
- Produktionsprofil auf PostgreSQL ausrichten.

**Ergebnis:**
- Gute Developer Experience lokal und tragfähiger Betrieb in Produktion.

### Herausforderung D: API-Integration im Frontend (Token-handling)

**Problem:**
- Fehlende/abgelaufene Tokens führten zu uneinheitlichem Fehlerverhalten.

**Workaround:**
- Zentraler API-Call-Pfad mit einheitlichem Authorization-Header.
- Standardisierte Behandlung von 401/403-Rückgaben (erneuter Login-Flow).

**Ergebnis:**
- Vorhersehbares Auth-Verhalten und weniger supportintensive Edge Cases.

---

## 5. Fazit der technischen Strategie

Der gewählte Stack optimiert die Balance aus schneller Entwicklung, guter Wartbarkeit und skalierbarem Betrieb:

- Flet/FastAPI für hohe Umsetzungsgeschwindigkeit im Team.
- SQLAlchemy für geringe Kopplung und bessere Evolvierbarkeit.
- SQLite lokal und PostgreSQL produktiv als pragmatischer Skalierungspfad.
- Konkrete Workarounds für bekannte Probleme sind dokumentiert und operationalisierbar.
