# 🏛️ Klassendiagramm

Das Klassendiagramm zeigt die **Objektstruktur** des Systems und deren **Beziehungen**.

---

## 📊 Klassendiagramm

!!! warning "Diagramm einfügen"
    Hier sollte das Klassendiagramm eingefügt werden.  
    Speichere es als `klassendiagramm.png` im Ordner `docs/images/` und füge es hier ein:
    
    ```markdown
    ![Klassendiagramm](../images/klassendiagramm.png)
    ```

---

## 🏗️ Klassen

### User

Repräsentiert einen Benutzer (Kunde, Landwirt oder Admin).

```python
class User:
    + id: int
    + email: str
    + password_hash: str
    + first_name: str
    + last_name: str
    + role: UserRole
    + street: str
    + plz: str
    + city: str
    + phone: str
    + created_at: DateTime
    
    + login(email: str, password: str): bool
    + logout(): void
    + update_profile(data: dict): void
```

**Beziehungen:**

- 1:1 → `Farmer` (wenn role = "farmer")
- 1:n → `Order` (als customer)

---

### Farmer

Erweiterte Informationen für Landwirte.

```python
class Farmer:
    + id: int
    + user_id: int
    + farm_name: str
    + description: str
    + farm_street: str
    + farm_plz: str
    + farm_city: str
    + bio_certified: bool
    + is_approved: bool
    
    + create_product(data: dict): Product
    + get_products(): List[Product]
    + get_orders(): List[Order]
    + confirm_order(order_id: int): void
```

**Beziehungen:**

- 1:1 → `User`
- 1:n → `Product`
- 1:n → `Order`

---

### Product

Ein Produkt, das von einem Landwirt angeboten wird.

```python
class Product:
    + id: int
    + farmer_id: int
    + name: str
    + description: str
    + category: str
    + price: float
    + unit: str
    + bio: bool
    + available: bool
    + created_at: DateTime
    
    + update(data: dict): void
    + delete(): void
    + set_availability(available: bool): void
```

**Beziehungen:**

- n:1 → `Farmer`
- n:m → `Order` (via `OrderItem`)

---

### Order

Eine Bestellung eines Kunden bei einem Landwirt.

```python
class Order:
    + id: int
    + customer_id: int
    + farmer_id: int
    + status: OrderStatus
    + total_price: float
    + pickup_date: DateTime
    + created_at: DateTime
    + updated_at: DateTime
    
    + add_item(product: Product, quantity: int): void
    + calculate_total(): float
    + confirm(): void
    + cancel(): void
    + mark_picked_up(): void
```

**Beziehungen:**

- n:1 → `User` (als customer)
- n:1 → `Farmer`
- 1:n → `OrderItem`

---

### OrderItem

Eine einzelne Position innerhalb einer Bestellung.

```python
class OrderItem:
    + id: int
    + order_id: int
    + product_id: int
    + quantity: int
    + unit_price: float
    
    + get_subtotal(): float
```

**Beziehungen:**

- n:1 → `Order`
- n:1 → `Product`

---

### Cart (Warenkorb)

Temporärer Speicher für Produkte vor der Bestellung.

```python
class Cart:
    + user_id: int
    + items: List[CartItem]
    
    + add_item(product: Product, quantity: int): void
    + remove_item(product_id: int): void
    + update_quantity(product_id: int, quantity: int): void
    + get_total(): float
    + clear(): void
    + checkout(): Order
```

**Beziehungen:**

- 1:1 → `User`
- 1:n → `CartItem`

---

## 🔗 Beziehungen

### Assoziationen

```
User ────── (1:1) ────── Farmer
  │
  │ (1:n)
  │
  └── Order ────── (n:1) ────── Farmer
        │                         │
        │ (1:n)                   │ (1:n)
        │                         │
    OrderItem ─── (n:1) ──── Product
```

### Vererbung

!!! note "Keine Vererbung"
    In diesem Modell wird keine Vererbung verwendet. `User` deckt alle Benutzertypen über das `role`-Attribut ab.

### Aggregation / Komposition

- **Order** → **OrderItem**: Komposition (OrderItem kann nicht ohne Order existieren)
- **Cart** → **CartItem**: Komposition
- **Farmer** → **Product**: Aggregation (Product existiert unabhängig)

---

## 📋 Enumerationen

### UserRole

```python
class UserRole(Enum):
    CUSTOMER = "customer"
    FARMER = "farmer"
    ADMIN = "admin"
```

### OrderStatus

```python
class OrderStatus(Enum):
    OPEN = "open"
    CONFIRMED = "confirmed"
    PICKED_UP = "picked_up"
    CANCELLED = "cancelled"
```

### ProductCategory

```python
class ProductCategory(Enum):
    FRUIT = "Obst"
    VEGETABLE = "Gemüse"
    MEAT = "Fleisch"
    DAIRY = "Milchprodukte"
    EGGS = "Eier"
    OTHER = "Sonstiges"
```

---

## 🎯 Design-Patterns

### Repository Pattern

Datenzugriff wird über Repository-Klassen gekapselt:

```python
class UserRepository:
    + find_by_id(id: int): User
    + find_by_email(email: str): User
    + save(user: User): void
    + delete(id: int): void
```

### Service Layer

Business-Logik in Service-Klassen:

```python
class OrderService:
    + create_order(cart: Cart): Order
    + confirm_order(order_id: int): void
    + cancel_order(order_id: int): void
```

---

## 🔐 Sicherheit

### Authentifizierung

```python
class AuthService:
    + login(email: str, password: str): Token
    + logout(token: Token): void
    + validate_token(token: Token): bool
    + hash_password(password: str): str
    + verify_password(password: str, hash: str): bool
```

---

## 🚀 Nächste Schritte

Siehe auch:

- **[Logisches Modell](logisches-modell.md)** – Datenmodell
- **[Sequenzdiagramme](uml-sequenz.md)** – Ablaufbeschreibungen
- **[API-Dokumentation](api.md)** – REST-Endpunkte
