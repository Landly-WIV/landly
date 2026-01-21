# 🗂️ Logisches Modell

Das logische Datenmodell beschreibt die **Entitäten** und **Beziehungen** des Systems.

---

## 📊 ER-Diagramm

!!! warning "Diagramm einfügen"
    Hier sollte das ER-Diagramm eingefügt werden.  
    Speichere es als `er-diagramm.png` im Ordner `docs/images/` und füge es hier ein:
    
    ```markdown
    ![ER-Diagramm](../images/er-diagramm.png)
    ```

---

## 🏗️ Entitäten

### 1. User (Benutzer)

Repräsentiert sowohl **Kunden** als auch **Landwirte**.

| Attribut | Typ | Beschreibung | Pflicht |
|----------|-----|--------------|---------|
| `id` | Integer | Eindeutige ID | ✅ |
| `email` | String | E-Mail-Adresse (unique) | ✅ |
| `password_hash` | String | Gehashtes Passwort | ✅ |
| `first_name` | String | Vorname | ✅ |
| `last_name` | String | Nachname | ✅ |
| `role` | Enum | Rolle: `customer`, `farmer`, `admin` | ✅ |
| `street` | String | Straße & Hausnummer | ✅ |
| `plz` | String | Postleitzahl | ✅ |
| `city` | String | Stadt | ✅ |
| `phone` | String | Telefonnummer | ❌ |
| `created_at` | DateTime | Erstellungsdatum | ✅ |

**Beziehungen:**

- 1:n zu `Order` (als Kunde)
- 1:1 zu `Farmer` (bei Rolle `farmer`)

---

### 2. Farmer (Landwirt)

Erweiterte Informationen für Landwirte.

| Attribut | Typ | Beschreibung | Pflicht |
|----------|-----|--------------|---------|
| `id` | Integer | Eindeutige ID | ✅ |
| `user_id` | Integer | Referenz zu User | ✅ |
| `farm_name` | String | Name des Hofes | ✅ |
| `description` | Text | Beschreibung des Hofes | ❌ |
| `farm_street` | String | Straße des Hofes | ✅ |
| `farm_plz` | String | PLZ des Hofes | ✅ |
| `farm_city` | String | Stadt des Hofes | ✅ |
| `bio_certified` | Boolean | Bio-Zertifizierung | ❌ |
| `is_approved` | Boolean | Vom Admin freigegeben | ✅ |

**Beziehungen:**

- 1:1 zu `User`
- 1:n zu `Product`

---

### 3. Product (Produkt)

Produkte, die von Landwirten angeboten werden.

| Attribut | Typ | Beschreibung | Pflicht |
|----------|-----|--------------|---------|
| `id` | Integer | Eindeutige ID | ✅ |
| `farmer_id` | Integer | Referenz zu Farmer | ✅ |
| `name` | String | Produktname | ✅ |
| `description` | Text | Produktbeschreibung | ❌ |
| `category` | String | Kategorie (Obst, Gemüse, ...) | ✅ |
| `price` | Float | Preis pro Einheit | ✅ |
| `unit` | String | Einheit (kg, Stück, ...) | ✅ |
| `bio` | Boolean | Bio-Qualität | ❌ |
| `available` | Boolean | Verfügbar | ✅ |
| `created_at` | DateTime | Erstellungsdatum | ✅ |

**Beziehungen:**

- n:1 zu `Farmer`
- n:m zu `Order` (via `OrderItem`)

---

### 4. Order (Bestellung)

Bestellungen von Kunden.

| Attribut | Typ | Beschreibung | Pflicht |
|----------|-----|--------------|---------|
| `id` | Integer | Eindeutige ID | ✅ |
| `customer_id` | Integer | Referenz zu User (Kunde) | ✅ |
| `farmer_id` | Integer | Referenz zu Farmer | ✅ |
| `status` | Enum | Status: `open`, `confirmed`, `picked_up`, `cancelled` | ✅ |
| `total_price` | Float | Gesamtpreis | ✅ |
| `pickup_date` | DateTime | Geplantes Abholdatum | ❌ |
| `created_at` | DateTime | Bestelldatum | ✅ |
| `updated_at` | DateTime | Letzte Änderung | ✅ |

**Beziehungen:**

- n:1 zu `User` (als Kunde)
- n:1 zu `Farmer`
- 1:n zu `OrderItem`

---

### 5. OrderItem (Bestellposition)

Einzelne Produkte innerhalb einer Bestellung.

| Attribut | Typ | Beschreibung | Pflicht |
|----------|-----|--------------|---------|
| `id` | Integer | Eindeutige ID | ✅ |
| `order_id` | Integer | Referenz zu Order | ✅ |
| `product_id` | Integer | Referenz zu Product | ✅ |
| `quantity` | Integer | Menge | ✅ |
| `unit_price` | Float | Preis pro Einheit (zum Zeitpunkt der Bestellung) | ✅ |

**Beziehungen:**

- n:1 zu `Order`
- n:1 zu `Product`

---

## 🔗 Beziehungen

### User ↔ Farmer (1:1)

- Ein **User** mit Rolle `farmer` hat genau ein **Farmer**-Profil
- Ein **Farmer** gehört zu genau einem **User**

### User ↔ Order (1:n)

- Ein **User** (Kunde) kann mehrere **Orders** haben
- Eine **Order** gehört zu genau einem **User**

### Farmer ↔ Product (1:n)

- Ein **Farmer** kann mehrere **Products** anbieten
- Ein **Product** gehört zu genau einem **Farmer**

### Farmer ↔ Order (1:n)

- Ein **Farmer** kann mehrere **Orders** erhalten
- Eine **Order** gehört zu genau einem **Farmer**

### Order ↔ OrderItem (1:n)

- Eine **Order** kann mehrere **OrderItems** enthalten
- Ein **OrderItem** gehört zu genau einer **Order**

### Product ↔ OrderItem (1:n)

- Ein **Product** kann in mehreren **OrderItems** vorkommen
- Ein **OrderItem** referenziert genau ein **Product**

---

## 📈 Kardinalitäten (Übersicht)

```
User (1) ──────── (1) Farmer
  │
  │ (1)
  │
  ├── (n) Order
  │         │
  │         │ (n)
  │         │
  │         └── (1) Farmer
  │                   │
  │                   │ (n)
  │                   │
  │                   └── Product
  │
  └── (n) OrderItem ──── (1) Product
```

---

## 🔑 Primär- und Fremdschlüssel

| Tabelle | Primärschlüssel | Fremdschlüssel |
|---------|-----------------|----------------|
| **User** | `id` | – |
| **Farmer** | `id` | `user_id` → `User.id` |
| **Product** | `id` | `farmer_id` → `Farmer.id` |
| **Order** | `id` | `customer_id` → `User.id`<br>`farmer_id` → `Farmer.id` |
| **OrderItem** | `id` | `order_id` → `Order.id`<br>`product_id` → `Product.id` |

---

## 📝 Beispieldaten

### Beispiel: Bestellung

**Kunde "Max Mustermann"** bestellt bei **"Biohof Schmidt"**:

```
User (id=1, role=customer)
  └── Order (id=1, customer_id=1, farmer_id=2, status=confirmed)
        ├── OrderItem (id=1, product_id=5, quantity=2)  → Bio-Tomaten
        └── OrderItem (id=2, product_id=7, quantity=1)  → Kartoffeln
```

**Farmer "Biohof Schmidt"**:

```
User (id=3, role=farmer)
  └── Farmer (id=2, user_id=3, farm_name="Biohof Schmidt")
        ├── Product (id=5, name="Bio-Tomaten")
        ├── Product (id=7, name="Kartoffeln")
        └── Order (id=1)  ← Bestellung von Max
```

---

## 🎯 Design-Entscheidungen

### Warum keine separate Customer-Tabelle?

- **User** deckt sowohl Kunden als auch Landwirte ab
- Rolle wird über `role`-Attribut unterschieden
- Vermeidet Redundanz und vereinfacht Authentifizierung

### Warum OrderItem als separate Tabelle?

- **N:M-Beziehung** zwischen Order und Product
- Speichert **historische Preise** (wichtig, falls Preise sich ändern)
- Erlaubt mehrere Produkte pro Bestellung

### Warum status als Enum?

- Verhindert inkonsistente Werte
- Erleichtert Filterung und Abfragen
- Klare Definition der möglichen Zustände

---

## 🚀 Nächste Schritte

Siehe auch:

- **[Datenbankschema](datenbankschema.md)** – SQL-Implementierung
- **[UML-Klassendiagramm](uml-klassen.md)** – Objektstruktur im Code
