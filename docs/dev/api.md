# 🔌 API-Dokumentation

Diese Seite dokumentiert alle REST-API-Endpunkte des Landly-Backends.

---

## 📍 Base URL

```
http://localhost:8000/api
```

---

## 🔐 Authentifizierung

Die meisten Endpunkte erfordern eine **JWT-Token-Authentifizierung**.

### Token erhalten

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "customer"
  }
}
```

### Token verwenden

Füge den Token in den Authorization-Header ein:

```
Authorization: Bearer <access_token>
```

---

## 👤 Auth-Endpunkte

### POST /auth/register

Registriert einen neuen Benutzer.

**Request Body:**
```json
{
  "email": "max@example.com",
  "password": "SecurePass123",
  "first_name": "Max",
  "last_name": "Mustermann",
  "role": "customer",
  "street": "Hauptstraße 1",
  "plz": "12345",
  "city": "Musterstadt",
  "phone": "+49 123 456789"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "max@example.com",
  "first_name": "Max",
  "last_name": "Mustermann",
  "role": "customer"
}
```

---

### POST /auth/login

Meldet einen Benutzer an.

**Request Body:**
```json
{
  "email": "max@example.com",
  "password": "SecurePass123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "max@example.com",
    "role": "customer"
  }
}
```

---

## 🌾 Product-Endpunkte

### GET /products

Gibt alle verfügbaren Produkte zurück.

**Query Parameter:**
- `plz` (optional): Postleitzahl für Umkreissuche
- `radius` (optional): Suchradius in km (Standard: 50)
- `category` (optional): Produktkategorie filtern
- `bio` (optional): Nur Bio-Produkte (true/false)
- `available` (optional): Nur verfügbare Produkte (true/false)

**Request:**
```
GET /products?plz=12345&radius=25&category=Gemüse&bio=true
```

**Response:** `200 OK`
```json
{
  "products": [
    {
      "id": 1,
      "farmer_id": 5,
      "farmer_name": "Hof Müller",
      "name": "Bio-Tomaten",
      "description": "Frische Tomaten aus biologischem Anbau",
      "category": "Gemüse",
      "price": 3.50,
      "unit": "kg",
      "bio": true,
      "available": true,
      "distance_km": 12.5,
      "farm_address": {
        "street": "Feldweg 10",
        "plz": "12347",
        "city": "Landdorf"
      }
    }
  ],
  "total": 1
}
```

---

### GET /products/{product_id}

Gibt Details zu einem einzelnen Produkt zurück.

**Response:** `200 OK`
```json
{
  "id": 1,
  "farmer_id": 5,
  "farmer": {
    "id": 5,
    "farm_name": "Hof Müller",
    "description": "Familiengeführter Bio-Hof seit 1950",
    "bio_certified": true,
    "farm_address": {
      "street": "Feldweg 10",
      "plz": "12347",
      "city": "Landdorf"
    }
  },
  "name": "Bio-Tomaten",
  "description": "Frische Tomaten aus biologischem Anbau",
  "category": "Gemüse",
  "price": 3.50,
  "unit": "kg",
  "bio": true,
  "available": true,
  "created_at": "2026-01-15T10:30:00"
}
```

---

### POST /products

Erstellt ein neues Produkt (nur für Landwirte).

**Authentifizierung:** Erforderlich (Farmer)

**Request Body:**
```json
{
  "name": "Bio-Kartoffeln",
  "description": "Frische Kartoffeln vom Feld",
  "category": "Gemüse",
  "price": 2.50,
  "unit": "kg",
  "bio": true,
  "available": true
}
```

**Response:** `201 Created`

---

### PUT /products/{product_id}

Aktualisiert ein bestehendes Produkt (nur eigene Produkte).

**Authentifizierung:** Erforderlich (Farmer)

**Request Body:**
```json
{
  "price": 2.80,
  "available": false
}
```

**Response:** `200 OK`

---

### DELETE /products/{product_id}

Löscht ein Produkt (nur eigene Produkte).

**Authentifizierung:** Erforderlich (Farmer)

**Response:** `204 No Content`

---

## 🛒 Order-Endpunkte

### GET /orders

Gibt alle Bestellungen des angemeldeten Benutzers zurück.

**Authentifizierung:** Erforderlich

**Response:** `200 OK`
```json
{
  "orders": [
    {
      "id": 1,
      "customer_id": 1,
      "farmer_id": 5,
      "farmer_name": "Hof Müller",
      "status": "confirmed",
      "total_price": 15.50,
      "pickup_date": "2026-02-28T14:00:00",
      "created_at": "2026-02-25T10:30:00",
      "items": [
        {
          "product_name": "Bio-Tomaten",
          "quantity": 2,
          "unit_price": 3.50,
          "unit": "kg"
        },
        {
          "product_name": "Bio-Gurken",
          "quantity": 3,
          "unit_price": 2.80,
          "unit": "Stück"
        }
      ]
    }
  ],
  "total": 1
}
```

---

### POST /orders

Erstellt eine neue Bestellung.

**Authentifizierung:** Erforderlich (Customer)

**Request Body:**
```json
{
  "farmer_id": 5,
  "pickup_date": "2026-02-28T14:00:00",
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 3
    }
  ]
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "status": "open",
  "total_price": 15.50,
  "message": "Bestellung erfolgreich erstellt"
}
```

---

### GET /orders/{order_id}

Gibt Details zu einer Bestellung zurück.

**Authentifizierung:** Erforderlich

**Response:** `200 OK`

---

### PUT /orders/{order_id}/status

Ändert den Status einer Bestellung (nur Landwirt).

**Authentifizierung:** Erforderlich (Farmer)

**Request Body:**
```json
{
  "status": "confirmed"
}
```

**Mögliche Status:**
- `open` - Bestellung eingegangen
- `confirmed` - Vom Landwirt bestätigt
- `picked_up` - Abgeholt
- `cancelled` - Storniert

**Response:** `200 OK`

---

## 🚜 Farmer-Endpunkte

### POST /farmers

Registriert einen Landwirt (erweiterte Registrierung).

**Authentifizierung:** Erforderlich (User mit role="farmer")

**Request Body:**
```json
{
  "farm_name": "Hof Müller",
  "description": "Familiengeführter Bio-Hof seit 1950",
  "farm_street": "Feldweg 10",
  "farm_plz": "12347",
  "farm_city": "Landdorf",
  "bio_certified": true
}
```

**Response:** `201 Created`

---

### GET /farmers/{farmer_id}

Gibt Informationen zu einem Landwirt zurück.

**Response:** `200 OK`
```json
{
  "id": 5,
  "farm_name": "Hof Müller",
  "description": "Familiengeführter Bio-Hof seit 1950",
  "bio_certified": true,
  "is_approved": true,
  "farm_address": {
    "street": "Feldweg 10",
    "plz": "12347",
    "city": "Landdorf"
  },
  "products_count": 15
}
```

---

### GET /farmers/{farmer_id}/products

Gibt alle Produkte eines Landwirts zurück.

**Response:** `200 OK`

---

## 👤 User-Endpunkte

### GET /users/me

Gibt den aktuell angemeldeten Benutzer zurück.

**Authentifizierung:** Erforderlich

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "max@example.com",
  "first_name": "Max",
  "last_name": "Mustermann",
  "role": "customer",
  "street": "Hauptstraße 1",
  "plz": "12345",
  "city": "Musterstadt",
  "phone": "+49 123 456789",
  "created_at": "2026-01-01T12:00:00"
}
```

---

### PUT /users/me

Aktualisiert das eigene Profil.

**Authentifizierung:** Erforderlich

**Request Body:**
```json
{
  "first_name": "Maximilian",
  "phone": "+49 123 999999"
}
```

**Response:** `200 OK`

---

## 🔍 Search-Endpunkte

### GET /search

Umkreissuche nach PLZ.

**Query Parameter:**
- `plz` (required): Postleitzahl
- `radius` (optional): Radius in km (Standard: 50)
- `query` (optional): Suchbegriff

**Request:**
```
GET /search?plz=12345&radius=25&query=tomaten
```

**Response:** `200 OK`
```json
{
  "results": {
    "products": [...],
    "farmers": [...]
  }
}
```

---

## ⚠️ Error Responses

Alle Fehler folgen diesem Format:

```json
{
  "detail": "Fehlerbeschreibung",
  "status_code": 400
}
```

### Häufige Status Codes

| Code | Bedeutung |
|------|-----------|
| `200` | Erfolgreich |
| `201` | Erstellt |
| `204` | Kein Inhalt (erfolgreiches Löschen) |
| `400` | Ungültige Anfrage |
| `401` | Nicht authentifiziert |
| `403` | Keine Berechtigung |
| `404` | Nicht gefunden |
| `422` | Validierungsfehler |
| `500` | Serverfehler |

---

## 🧪 API testen

### Mit cURL

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}'

# Produkte abrufen
curl -X GET "http://localhost:8000/api/products?plz=12345" \
  -H "Authorization: Bearer <token>"
```

### Mit Python (requests)

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={"email": "test@example.com", "password": "test123"}
)
token = response.json()["access_token"]

# Produkte abrufen
headers = {"Authorization": f"Bearer {token}"}
products = requests.get(
    "http://localhost:8000/api/products?plz=12345",
    headers=headers
)
print(products.json())
```

---

## 📖 Interaktive API-Dokumentation

FastAPI generiert automatisch eine interaktive API-Dokumentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔗 Weiterführende Links

- [Backend-Entwicklung](backend-logik.md)
- [Authentifizierung](authentifizierung.md)
- [Datenbankschema](datenbankschema.md)
