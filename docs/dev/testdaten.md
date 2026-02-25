# 🧪 Test-Accounts & Demo-Daten

Diese Seite enthält Test-Accounts und Beispieldaten zum Ausprobieren der Plattform.

---

## 🔐 Test-Accounts

Nutze diese vorgefertigten Accounts zum Testen:

### 👤 Kunde

**E-Mail:** `kunde@landly.de`  
**Passwort:** `Test123!`

**Profil:**
- Name: Anna Kundin
- Adresse: Musterstraße 10, 12345 Berlin
- Rolle: Customer

**Was testen:**
- Produkte suchen
- Warenkorb füllen
- Bestellung aufgeben
- Bestellungen ansehen

---

### 🚜 Landwirt

**E-Mail:** `landwirt@landly.de`  
**Passwort:** `Test123!`

**Profil:**
- Name: Bauer Schmidt
- Hof: Bio-Hof Schmidt
- Adresse: Feldweg 5, 12347 Landdorf
- Rolle: Farmer
- Bio-Zertifiziert: Ja

**Was testen:**
- Produkte anlegen
- Produkte verwalten
- Bestellungen einsehen
- Bestellungen bestätigen
- Hofprofil bearbeiten

---

### 👨‍💼 Administrator

**E-Mail:** `admin@landly.de`  
**Passwort:** `Admin123!`

**Profil:**
- Name: Max Admin
- Rolle: Admin

**Was testen:**
- Benutzerverwaltung
- Landwirte freischalten
- Systemüberwachung
- Support-Anfragen

---

## 📦 Beispiel-Produkte

Die Datenbank enthält folgende Test-Produkte:

### Bio-Hof Schmidt (Landdorf, 12347)

| Produkt | Kategorie | Preis | Einheit | Bio |
|---------|-----------|-------|---------|-----|
| Bio-Tomaten | Gemüse | 3,50 € | kg | ✅ |
| Bio-Gurken | Gemüse | 2,80 € | Stück | ✅ |
| Kartoffeln | Gemüse | 2,00 € | kg | ✅ |
| Eier (Freiland) | Tierprodukte | 4,50 € | 10er | ✅ |
| Milch | Milchprodukte | 1,20 € | L | ✅ |

---

### Obstgut Müller (Obstdorf, 12340)

| Produkt | Kategorie | Preis | Einheit | Bio |
|---------|-----------|-------|---------|-----|
| Äpfel Elstar | Obst | 2,50 € | kg | ❌ |
| Birnen | Obst | 3,00 € | kg | ❌ |
| Erdbeeren | Obst | 5,50 € | 500g | ✅ |
| Himbeeren | Obst | 6,00 € | 250g | ✅ |
| Apfelsaft | Getränke | 3,50 € | L | ❌ |

---

### Gemüsehof Weber (Grünstadt, 12355)

| Produkt | Kategorie | Preis | Einheit | Bio |
|---------|-----------|-------|---------|-----|
| Karotten | Gemüse | 1,80 € | kg | ✅ |
| Zucchini | Gemüse | 2,20 € | kg | ✅ |
| Salat (Kopf) | Gemüse | 1,50 € | Stück | ✅ |
| Paprika | Gemüse | 4,00 € | kg | ✅ |
| Kürbis | Gemüse | 2,50 € | kg | ✅ |

---

## 🗺️ Test-Szenarien

### Szenario 1: Kunde bestellt Produkte

**Ziel:** Kompletten Bestellprozess durchlaufen

**Schritte:**
1. Als Kunde einloggen (`kunde@landly.de`)
2. PLZ eingeben: `12345`
3. Produkte im Umkreis suchen
4. Filter anwenden (z.B. nur Bio)
5. 2-3 Produkte in den Warenkorb legen
6. Zur Kasse gehen
7. Abholtermin wählen
8. Bestellung abschicken
9. Bestellbestätigung prüfen

**Erwartetes Ergebnis:**
- Bestellung wird erstellt
- Status: "Offen"
- Bestellung in "Meine Bestellungen" sichtbar

---

### Szenario 2: Landwirt bestätigt Bestellung

**Ziel:** Bestellverwaltung aus Landwirt-Sicht testen

**Schritte:**
1. Als Landwirt einloggen (`landwirt@landly.de`)
2. Zu "Meine Bestellungen" navigieren
3. Offene Bestellung auswählen
4. Bestelldetails prüfen
5. Bestellung bestätigen
6. Status auf "Bestätigt" setzen

**Erwartetes Ergebnis:**
- Bestellstatus ändert sich
- Kunde sieht aktualisierte Bestellung

---

### Szenario 3: Landwirt legt neues Produkt an

**Ziel:** Produktverwaltung testen

**Schritte:**
1. Als Landwirt einloggen
2. Zu "Meine Produkte" navigieren
3. "Neues Produkt" klicken
4. Formular ausfüllen:
   - Name: "Bio-Brokkoli"
   - Kategorie: "Gemüse"
   - Preis: 3,20
   - Einheit: "kg"
   - Bio: Ja
   - Verfügbar: Ja
5. Produkt speichern
6. Prüfen ob Produkt in Liste erscheint

**Erwartetes Ergebnis:**
- Produkt wird erstellt
- In der Produktliste sichtbar
- Bei Suche auffindbar

---

### Szenario 4: Umkreissuche mit verschiedenen Radien

**Ziel:** Suchfunktion testen

**Test-Cases:**

| PLZ | Radius | Erwartete Treffer |
|-----|--------|-------------------|
| 12345 | 10 km | 0-2 Höfe |
| 12345 | 25 km | 3-5 Höfe |
| 12345 | 50 km | Alle Höfe |
| 99999 | 50 km | Keine Treffer |

**Schritte:**
1. PLZ und Radius eingeben
2. Suchen klicken
3. Anzahl der Ergebnisse prüfen
4. Entfernung zu jedem Hof prüfen

---

### Szenario 5: Filter anwenden

**Ziel:** Such-Filter testen

**Test-Cases:**

| Filter | Erwartetes Ergebnis |
|--------|---------------------|
| Kategorie: "Obst" | Nur Obst-Produkte |
| Kategorie: "Gemüse" | Nur Gemüse-Produkte |
| Nur Bio | Nur Bio-zertifizierte Produkte |
| Preis: 0-3€ | Produkte bis 3€ |
| Verfügbar: Ja | Nur verfügbare Produkte |

---

## 📊 Beispiel-Datensätze

### SQL-Dump (SQLite)

Die Testdaten können mit folgendem Script geladen werden:

```bash
python scripts/load_testdata.py
```

Oder manuell:

```sql
-- Kunde
INSERT INTO users (email, password_hash, first_name, last_name, role, street, plz, city, phone)
VALUES ('kunde@landly.de', '$2b$12$...', 'Anna', 'Kundin', 'customer', 'Musterstraße 10', '12345', 'Berlin', '+49 30 123456');

-- Landwirt
INSERT INTO users (email, password_hash, first_name, last_name, role, street, plz, city, phone)
VALUES ('landwirt@landly.de', '$2b$12$...', 'Hans', 'Schmidt', 'farmer', 'Feldweg 5', '12347', 'Landdorf', '+49 33 789012');

INSERT INTO farmers (user_id, farm_name, description, farm_street, farm_plz, farm_city, bio_certified, is_approved)
VALUES (2, 'Bio-Hof Schmidt', 'Familiengeführter Bio-Hof seit 1950', 'Feldweg 5', '12347', 'Landdorf', 1, 1);

-- Produkte
INSERT INTO products (farmer_id, name, description, category, price, unit, bio, available)
VALUES 
  (1, 'Bio-Tomaten', 'Frische Tomaten aus biologischem Anbau', 'Gemüse', 3.50, 'kg', 1, 1),
  (1, 'Bio-Gurken', 'Knackige Gurken vom Feld', 'Gemüse', 2.80, 'Stück', 1, 1),
  (1, 'Kartoffeln', 'Mehlig kochende Kartoffeln', 'Gemüse', 2.00, 'kg', 1, 1);
```

---

## 🎭 Demo-Modus

Für Präsentationen gibt es einen **Demo-Modus**:

```python
# In config.py
DEMO_MODE = True
```

**Aktiviert folgende Features:**
- Vorgefüllte Formulare
- Beispiel-Daten werden automatisch geladen
- Keine E-Mail-Validierung
- Verkürzte Session-Timeout
- Schnellere Animation

---

## 🧹 Daten zurücksetzen

Um die Testdaten zurückzusetzen:

```bash
# Datenbank löschen
rm storage/data/landly.db

# Neu initialisieren
python src/backend/db.py

# Testdaten laden
python scripts/load_testdata.py
```

---

## 📝 Eigene Test-Accounts erstellen

Du kannst auch eigene Test-Accounts über die Registrierung anlegen:

**Tipps:**
- Nutze temporäre E-Mail-Adressen (z.B. von temp-mail.org)
- Verwende einfache Passwörter (nur für Tests!)
- Lege mehrere Höfe mit unterschiedlichen PLZ an
- Erstelle vielfältige Produktkategorien

---

## 🐛 Test-Daten für Bug-Reports

Bei Bug-Reports bitte diese Infos angeben:

```
Account: kunde@landly.de
Aktion: Produktsuche
PLZ: 12345
Radius: 25 km
Filter: Bio = true
Erwartetes Ergebnis: 5 Produkte
Tatsächliches Ergebnis: 0 Produkte
Fehler: [Screenshot/Fehlermeldung]
```

---

## 📞 Support

Bei Problemen mit Test-Accounts:

**E-Mail:** dev@landly.de  
**Slack:** #testing-channel
