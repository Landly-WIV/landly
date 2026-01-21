# 👥 Use-Case-Diagramm

Das Use-Case-Diagramm zeigt die **Akteure** und **Anwendungsfälle** des Systems.

---

## 🎭 Akteure

| Akteur | Beschreibung |
|--------|--------------|
| **Kunde** | Sucht Produkte, erstellt Bestellungen |
| **Landwirt** | Verwaltet Produkte und Bestellungen |
| **Administrator** | Verwaltet System und Benutzer |
| **System** | Automatisierte Prozesse (z. B. Benachrichtigungen) |

---

## 📊 Use-Case-Diagramm

!!! warning "Diagramm einfügen"
    Hier sollte das Use-Case-Diagramm eingefügt werden.  
    Speichere es als `usecase-diagramm.png` im Ordner `docs/images/` und füge es hier ein:
    
    ```markdown
    ![Use-Case-Diagramm](../images/usecase-diagramm.png)
    ```

---

## 🔄 Anwendungsfälle

### Kunde

#### UC-01: Registrieren

**Akteur:** Kunde  
**Beschreibung:** Kunde erstellt ein neues Konto  
**Vorbedingung:** Keine  
**Ablauf:**

1. Kunde öffnet Registrierungsformular
2. Kunde gibt Daten ein (E-Mail, Passwort, Name, Adresse)
3. System validiert Eingaben
4. System erstellt Konto
5. System sendet Bestätigungsmail

**Nachbedingung:** Kunde ist registriert und kann sich einloggen

---

#### UC-02: Einloggen

**Akteur:** Kunde, Landwirt  
**Beschreibung:** Benutzer meldet sich im System an  
**Vorbedingung:** Benutzer ist registriert  
**Ablauf:**

1. Benutzer öffnet Login-Seite
2. Benutzer gibt E-Mail und Passwort ein
3. System validiert Anmeldedaten
4. System erstellt Session
5. Benutzer wird zur Startseite weitergeleitet

**Nachbedingung:** Benutzer ist eingeloggt

---

#### UC-03: Produkte suchen

**Akteur:** Kunde  
**Beschreibung:** Kunde sucht Produkte in der Umgebung  
**Vorbedingung:** Kunde ist eingeloggt (optional)  
**Ablauf:**

1. Kunde gibt PLZ ein
2. System zeigt Produkte im Umkreis an
3. Kunde wendet Filter an (optional)
4. System aktualisiert Ergebnisse

**Nachbedingung:** Kunde sieht relevante Produkte

---

#### UC-04: Produktdetails anzeigen

**Akteur:** Kunde  
**Beschreibung:** Kunde öffnet Detailseite eines Produkts  
**Vorbedingung:** Produkt existiert  
**Ablauf:**

1. Kunde klickt auf Produkt
2. System zeigt Produktdetails (Name, Preis, Herkunft, etc.)
3. Kunde sieht Hofprofil des Anbieters

**Nachbedingung:** Kunde hat Produktinformationen

---

#### UC-05: Produkt in Warenkorb legen

**Akteur:** Kunde  
**Beschreibung:** Kunde fügt Produkt zum Warenkorb hinzu  
**Vorbedingung:** Kunde ist eingeloggt  
**Ablauf:**

1. Kunde wählt Produkt aus
2. Kunde gibt Menge ein
3. Kunde klickt "In den Warenkorb"
4. System fügt Produkt zu Warenkorb hinzu

**Nachbedingung:** Produkt ist im Warenkorb

---

#### UC-06: Bestellung aufgeben

**Akteur:** Kunde  
**Beschreibung:** Kunde schließt Bestellung ab  
**Vorbedingung:** Warenkorb ist nicht leer  
**Ablauf:**

1. Kunde öffnet Warenkorb
2. Kunde prüft Produkte
3. Kunde klickt "Zur Kasse"
4. System erstellt Bestellung
5. System sendet Bestätigung per E-Mail

**Nachbedingung:** Bestellung ist erstellt

---

#### UC-07: Bestellungen anzeigen

**Akteur:** Kunde  
**Beschreibung:** Kunde sieht seine Bestellungen  
**Vorbedingung:** Kunde ist eingeloggt  
**Ablauf:**

1. Kunde öffnet "Meine Bestellungen"
2. System zeigt alle Bestellungen mit Status

**Nachbedingung:** Kunde kennt seine Bestellungen

---

#### UC-08: Bestellung stornieren

**Akteur:** Kunde  
**Beschreibung:** Kunde storniert eine Bestellung  
**Vorbedingung:** Bestellung ist noch nicht abgeholt  
**Ablauf:**

1. Kunde öffnet Bestellung
2. Kunde klickt "Stornieren"
3. System ändert Status auf "storniert"
4. System benachrichtigt Landwirt

**Nachbedingung:** Bestellung ist storniert

---

#### UC-09: Profil verwalten

**Akteur:** Kunde, Landwirt  
**Beschreibung:** Benutzer bearbeitet seine Daten  
**Vorbedingung:** Benutzer ist eingeloggt  
**Ablauf:**

1. Benutzer öffnet "Mein Profil"
2. Benutzer ändert Daten
3. Benutzer speichert
4. System aktualisiert Profil

**Nachbedingung:** Profil ist aktualisiert

---

### Landwirt

#### UC-10: Als Landwirt registrieren

**Akteur:** Landwirt  
**Beschreibung:** Landwirt erstellt ein Hofprofil  
**Vorbedingung:** Keine  
**Ablauf:**

1. Landwirt öffnet Registrierung
2. Landwirt gibt Hofdaten ein
3. System validiert Eingaben
4. System erstellt Konto (Status: inaktiv)
5. Administrator muss Konto freischalten

**Nachbedingung:** Landwirt wartet auf Freischaltung

---

#### UC-11: Produkt anlegen

**Akteur:** Landwirt  
**Beschreibung:** Landwirt fügt ein neues Produkt hinzu  
**Vorbedingung:** Landwirt ist eingeloggt und freigeschaltet  
**Ablauf:**

1. Landwirt öffnet "Produkte verwalten"
2. Landwirt klickt "Neues Produkt"
3. Landwirt gibt Produktdaten ein
4. Landwirt speichert
5. System erstellt Produkt

**Nachbedingung:** Produkt ist verfügbar

---

#### UC-12: Produkt bearbeiten

**Akteur:** Landwirt  
**Beschreibung:** Landwirt ändert Produktinformationen  
**Vorbedingung:** Produkt existiert  
**Ablauf:**

1. Landwirt öffnet Produkt
2. Landwirt ändert Daten (Preis, Verfügbarkeit, etc.)
3. Landwirt speichert
4. System aktualisiert Produkt

**Nachbedingung:** Produkt ist aktualisiert

---

#### UC-13: Produkt löschen

**Akteur:** Landwirt  
**Beschreibung:** Landwirt entfernt ein Produkt  
**Vorbedingung:** Produkt existiert und ist nicht in offenen Bestellungen  
**Ablauf:**

1. Landwirt öffnet Produkt
2. Landwirt klickt "Löschen"
3. System bestätigt Löschung
4. System entfernt Produkt

**Nachbedingung:** Produkt ist gelöscht

---

#### UC-14: Bestellungen einsehen

**Akteur:** Landwirt  
**Beschreibung:** Landwirt sieht eingehende Bestellungen  
**Vorbedingung:** Landwirt ist eingeloggt  
**Ablauf:**

1. Landwirt öffnet "Bestellungen"
2. System zeigt alle Bestellungen für diesen Hof

**Nachbedingung:** Landwirt kennt seine Bestellungen

---

#### UC-15: Bestellung bestätigen

**Akteur:** Landwirt  
**Beschreibung:** Landwirt bestätigt eine Bestellung  
**Vorbedingung:** Bestellung ist offen  
**Ablauf:**

1. Landwirt öffnet Bestellung
2. Landwirt prüft Verfügbarkeit
3. Landwirt klickt "Bestätigen"
4. System ändert Status auf "bestätigt"
5. System benachrichtigt Kunde

**Nachbedingung:** Bestellung ist bestätigt

---

### Administrator

#### UC-16: Benutzerverwaltung

**Akteur:** Administrator  
**Beschreibung:** Admin verwaltet Benutzerkonten  
**Vorbedingung:** Admin ist eingeloggt  
**Ablauf:**

1. Admin öffnet Benutzerverwaltung
2. Admin sieht alle Benutzer
3. Admin kann Benutzer aktivieren/deaktivieren/löschen

**Nachbedingung:** Benutzer sind verwaltet

---

#### UC-17: Landwirt freischalten

**Akteur:** Administrator  
**Beschreibung:** Admin schaltet Landwirt-Konto frei  
**Vorbedingung:** Landwirt hat sich registriert  
**Ablauf:**

1. Admin öffnet "Freischaltungen"
2. Admin prüft Landwirt-Profil
3. Admin klickt "Freischalten"
4. System aktiviert Konto
5. System benachrichtigt Landwirt

**Nachbedingung:** Landwirt kann Produkte anlegen

---

#### UC-18: Systemüberwachung

**Akteur:** Administrator  
**Beschreibung:** Admin überwacht System-Performance  
**Vorbedingung:** Admin ist eingeloggt  
**Ablauf:**

1. Admin öffnet Dashboard
2. System zeigt Kennzahlen (Benutzer, Bestellungen, Fehler)

**Nachbedingung:** Admin kennt Systemzustand

---

## 🎯 Use-Case-Prioritäten

| Use-Case | Priorität (MoSCoW) |
|----------|-------------------|
| UC-02: Einloggen | **Must** |
| UC-03: Produkte suchen | **Must** |
| UC-06: Bestellung aufgeben | **Must** |
| UC-11: Produkt anlegen | **Must** |
| UC-14: Bestellungen einsehen | **Must** |
| UC-15: Bestellung bestätigen | **Must** |
| UC-17: Landwirt freischalten | **Must** |
| UC-08: Bestellung stornieren | Should |
| UC-13: Produkt löschen | Should |
| UC-18: Systemüberwachung | Should |

---

## 🚀 Nächste Schritte

Siehe auch:

- **[Sequenzdiagramme](uml-sequenz.md)** – Detaillierte Ablaufbeschreibungen
- **[Klassendiagramm](uml-klassen.md)** – Systemstruktur
