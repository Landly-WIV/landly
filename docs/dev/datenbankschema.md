# 🗄️ Datenbankschema

Diese Seite beschreibt das physische Datenbankschema von Landly.

---

## 📊 Übersicht

Das Datenbankschema basiert auf dem **[Logischen Modell](logisches-modell.md)** und wird mit **SQLAlchemy** als ORM implementiert.

---

## 🗂️ Tabellen

### users

Speichert alle Benutzer (Kunden, Landwirte, Admins).

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- 'customer', 'farmer', 'admin'
    street VARCHAR(255) NOT NULL,
    plz VARCHAR(10) NOT NULL,
    city VARCHAR(100) NOT NULL,
    phone VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

### farmers

Erweiterte Informationen für Landwirte.

```sql
CREATE TABLE farmers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    farm_name VARCHAR(255) NOT NULL,
    description TEXT,
    farm_street VARCHAR(255) NOT NULL,
    farm_plz VARCHAR(10) NOT NULL,
    farm_city VARCHAR(100) NOT NULL,
    bio_certified BOOLEAN DEFAULT FALSE,
    is_approved BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

### products

Produkte der Landwirte.

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(50) NOT NULL,  -- 'kg', 'Stück', etc.
    bio BOOLEAN DEFAULT FALSE,
    available BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (farmer_id) REFERENCES farmers(id) ON DELETE CASCADE
);
```

---

### orders

Bestellungen.

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    farmer_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'open',  -- 'open', 'confirmed', 'picked_up', 'cancelled'
    total_price DECIMAL(10, 2) NOT NULL,
    pickup_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (farmer_id) REFERENCES farmers(id) ON DELETE CASCADE
);
```

---

### order_items

Einzelne Positionen innerhalb einer Bestellung.

```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,  -- Preis zum Zeitpunkt der Bestellung
    
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
);
```

---

## 🔍 Indizes

Für bessere Performance werden folgende Indizes angelegt:

```sql
-- Suche nach E-Mail (Login)
CREATE INDEX idx_users_email ON users(email);

-- Suche nach PLZ (Umkreissuche)
CREATE INDEX idx_farmers_plz ON farmers(farm_plz);

-- Produktsuche nach Kategorie
CREATE INDEX idx_products_category ON products(category);

-- Produktsuche nach Verfügbarkeit
CREATE INDEX idx_products_available ON products(available);

-- Bestellungen eines Kunden
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Bestellungen eines Landwirts
CREATE INDEX idx_orders_farmer ON orders(farmer_id);

-- Bestellungen nach Status
CREATE INDEX idx_orders_status ON orders(status);
```

---

## 🔐 Constraints

### Foreign Keys

Alle Fremdschlüssel-Beziehungen sind mit **CASCADE** oder **RESTRICT** definiert:

- **ON DELETE CASCADE**: Wenn der Eltern-Datensatz gelöscht wird, werden auch die Kinder gelöscht
- **ON DELETE RESTRICT**: Verhindert Löschen, wenn noch abhängige Datensätze existieren

### Unique Constraints

- `users.email` – E-Mail muss eindeutig sein
- `farmers.user_id` – Ein User kann nur ein Farmer-Profil haben

---

## 📝 Beispiel-Queries

### Alle Produkte eines Landwirts

```sql
SELECT p.*, f.farm_name 
FROM products p
JOIN farmers f ON p.farmer_id = f.id
WHERE f.id = ?;
```

### Produkte im Umkreis (vereinfacht)

```sql
SELECT p.*, f.farm_name, f.farm_plz, f.farm_city
FROM products p
JOIN farmers f ON p.farmer_id = f.id
WHERE p.available = TRUE
  AND f.farm_plz LIKE '12%'  -- Vereinfachte PLZ-Suche
ORDER BY f.farm_plz;
```

### Bestellungen eines Kunden

```sql
SELECT o.*, f.farm_name
FROM orders o
JOIN farmers f ON o.farmer_id = f.id
WHERE o.customer_id = ?
ORDER BY o.created_at DESC;
```

---

## 🚀 SQLAlchemy-Modelle

Die Implementierung erfolgt mit SQLAlchemy ORM:

Siehe: `src/backend/models.py`

---

## 📚 Nächste Schritte

Siehe auch:

- **[Logisches Modell](logisches-modell.md)** – Konzeptuelle Ebene
- **[Setup & Installation](setup.md)** – Datenbank initialisieren
