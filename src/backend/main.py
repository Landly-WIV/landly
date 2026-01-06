from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from src.backend import crud, models, schemas, bauernabfrage
from src.backend.db import engine, get_db

# Erstelle alle Tabellen (falls noch nicht vorhanden)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bauernhof API",
    description="API für regionales Bauernhof-Bestellsystem",
    version="1.0.0"
)

# CORS Middleware (für Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Produktion spezifische Origins angeben!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================
# ROOT
# ========================

@app.get("/")
def read_root():
    """API Info"""
    return {
        "message": "Bauernhof API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# ========================
# PRODUKT ENDPOINTS
# ========================

@app.get("/produkte", response_model=List[schemas.Produkt])
def list_produkte(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Alle Produkte abrufen"""
    produkte = crud.get_produkte(db, skip=skip, limit=limit)
    return produkte

@app.get("/produkte/{produkt_id}", response_model=schemas.ProduktDetailed)
def read_produkt(produkt_id: int, db: Session = Depends(get_db)):
    """Ein Produkt mit allen Details"""
    produkt = crud.get_produkt_detailed(db, produkt_id=produkt_id)
    if produkt is None:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")
    return produkt

@app.post("/produkte", response_model=schemas.Produkt, status_code=201)
def create_produkt(produkt: schemas.ProduktCreate, db: Session = Depends(get_db)):
    """Neues Produkt erstellen"""
    return crud.create_produkt(db=db, produkt=produkt)

@app.put("/produkte/{produkt_id}", response_model=schemas.Produkt)
def update_produkt(produkt_id: int, produkt: schemas.ProduktCreate, db: Session = Depends(get_db)):
    """Produkt aktualisieren"""
    updated = crud.update_produkt(db=db, produkt_id=produkt_id, produkt=produkt)
    if updated is None:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")
    return updated

@app.delete("/produkte/{produkt_id}")
def delete_produkt(produkt_id: int, db: Session = Depends(get_db)):
    """Produkt löschen"""
    success = crud.delete_produkt(db=db, produkt_id=produkt_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")
    return {"message": "Produkt gelöscht"}

# ========================
# BAUER ENDPOINTS
# ========================

@app.get("/bauern", response_model=List[schemas.Bauer])
def list_bauern(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Alle Bauern abrufen"""
    return crud.get_bauern(db, skip=skip, limit=limit)

@app.get("/bauern/{bauer_id}", response_model=schemas.Bauer)
def read_bauer(bauer_id: int, db: Session = Depends(get_db)):
    """Ein Bauer nach ID"""
    bauer = crud.get_bauer(db, bauer_id=bauer_id)
    if bauer is None:
        raise HTTPException(status_code=404, detail="Bauer nicht gefunden")
    return bauer

@app.post("/bauern", response_model=schemas.Bauer, status_code=201)
def create_bauer(bauer: schemas.BauerCreate, db: Session = Depends(get_db)):
    """Neuen Bauer erstellen"""
    return crud.create_bauer(db=db, bauer=bauer)

@app.put("/bauern/{bauer_id}", response_model=schemas.Bauer)
def update_bauer(bauer_id: int, bauer: schemas.BauerCreate, db: Session = Depends(get_db)):
    """Bauer aktualisieren"""
    updated = crud.update_bauer(db=db, bauer_id=bauer_id, bauer=bauer)
    if updated is None:
        raise HTTPException(status_code=404, detail="Bauer nicht gefunden")
    return updated

# ========================
# ERWEITERTE BAUERN-SUCHE
# ========================

@app.get("/bauern/search/advanced")
def search_bauern_advanced(
    search: Optional[str] = Query(None, description="Suchbegriff für Firmenname oder Kontaktperson"),
    max_distanz: Optional[float] = Query(None, description="Maximale Entfernung in km"),
    user_lat: Optional[float] = Query(None, description="Breitengrad des Nutzers"),
    user_lon: Optional[float] = Query(None, description="Längengrad des Nutzers"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Erweiterte Bauernsuche mit Text- und Geo-Filter (nutzt bauernabfrage.py)"""
    results = bauernabfrage.search_bauern(
        db=db,
        search=search,
        max_distanz=max_distanz,
        user_lat=user_lat,
        user_lon=user_lon,
        skip=skip,
        limit=limit
    )
    
    # Formatiere Response: [{'bauer': {...}, 'distanz_km': 5.2}]
    return [
        {
            "bauer": bauer,
            "distanz_km": distanz
        } for bauer, distanz in results
    ]

@app.get("/bauern/nearest")
def get_nearest_bauern(
    user_lat: float = Query(..., description="Breitengrad des Nutzers"),
    user_lon: float = Query(..., description="Längengrad des Nutzers"),
    limit: int = Query(10, description="Anzahl der nächsten Bauern"),
    db: Session = Depends(get_db)
):
    """Findet die nächstgelegenen Bauern (nutzt bauernabfrage.py)"""
    results = bauernabfrage.get_nearest_bauern(
        db=db,
        user_lat=user_lat,
        user_lon=user_lon,
        limit=limit
    )
    
    return [
        {
            "bauer": bauer,
            "distanz_km": distanz
        } for bauer, distanz in results
    ]

@app.get("/bauern/{bauer_id}/details", response_model=schemas.Bauer)
def get_bauer_with_details(bauer_id: int, db: Session = Depends(get_db)):
    """Bauer mit allen Produkten und Standorten (nutzt bauernabfrage.py)"""
    bauer = bauernabfrage.get_bauer_with_products(db=db, bauer_id=bauer_id)
    if bauer is None:
        raise HTTPException(status_code=404, detail="Bauer nicht gefunden")
    return bauer

@app.get("/bauern/{bauer_id}/produkte", response_model=List[schemas.Produkt])
def get_produkte_by_bauer(
    bauer_id: int,
    produktart_id: Optional[int] = Query(None, description="Filter nach Produktart"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Alle Produkte eines Bauern (nutzt bauernabfrage.py)"""
    return bauernabfrage.get_produkte_by_bauer(
        db=db,
        bauer_id=bauer_id,
        produktart_id=produktart_id,
        skip=skip,
        limit=limit
    )

@app.get("/bauern/{bauer_id}/standorte", response_model=List[schemas.Standort])
def get_standorte_by_bauer(bauer_id: int, db: Session = Depends(get_db)):
    """Alle Standorte eines Bauern (nutzt bauernabfrage.py)"""
    return bauernabfrage.get_standorte_by_bauer(db=db, bauer_id=bauer_id)

@app.get("/bauern/count")
def count_bauern_endpoint(
    search: Optional[str] = Query(None, description="Suchbegriff für Filterung"),
    db: Session = Depends(get_db)
):
    """Zählt Bauern (für Pagination, nutzt bauernabfrage.py)"""
    count = bauernabfrage.count_bauern(db=db, search=search)
    return {"total": count}

# ========================
# KUNDE ENDPOINTS
# ========================

@app.get("/kunden", response_model=List[schemas.Kunde])
def list_kunden(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Alle Kunden abrufen"""
    return crud.get_kunden(db, skip=skip, limit=limit)

@app.get("/kunden/{kunden_id}", response_model=schemas.Kunde)
def read_kunde(kunden_id: int, db: Session = Depends(get_db)):
    """Ein Kunde nach ID"""
    kunde = crud.get_kunde(db, kunden_id=kunden_id)
    if kunde is None:
        raise HTTPException(status_code=404, detail="Kunde nicht gefunden")
    return kunde

@app.post("/kunden", response_model=schemas.Kunde, status_code=201)
def create_kunde(kunde: schemas.KundeCreate, db: Session = Depends(get_db)):
    """Neuen Kunde erstellen"""
    return crud.create_kunde(db=db, kunde=kunde)

# ========================
# BESTELLUNG ENDPOINTS
# ========================

@app.get("/bestellungen", response_model=List[schemas.Bestellung])
def list_bestellungen(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Alle Bestellungen abrufen"""
    return crud.get_bestellungen(db, skip=skip, limit=limit)

@app.get("/bestellungen/{bestellung_id}", response_model=schemas.BestellungDetailed)
def read_bestellung(bestellung_id: int, db: Session = Depends(get_db)):
    """Eine Bestellung mit allen Details"""
    bestellung = crud.get_bestellung_detailed(db, bestellung_id=bestellung_id)
    if bestellung is None:
        raise HTTPException(status_code=404, detail="Bestellung nicht gefunden")
    return bestellung

@app.post("/bestellungen", response_model=schemas.Bestellung, status_code=201)
def create_bestellung(bestellung: schemas.BestellungCreate, db: Session = Depends(get_db)):
    """Neue Bestellung mit Positionen erstellen"""
    return crud.create_bestellung(db=db, bestellung=bestellung)

# ========================
# PRODUKTART & LABEL ENDPOINTS
# ========================

@app.get("/produktarten", response_model=List[schemas.Produktart])
def list_produktarten(db: Session = Depends(get_db)):
    """Alle Produktarten"""
    return crud.get_produktarten(db)

@app.get("/labels", response_model=List[schemas.Label])
def list_labels(db: Session = Depends(get_db)):
    """Alle Labels"""
    return crud.get_labels(db)

# ========================
# STANDORT ENDPOINTS
# ========================

@app.get("/standorte", response_model=List[schemas.Standort])
def list_standorte(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Alle Standorte"""
    return crud.get_standorte(db, skip=skip, limit=limit)

@app.get("/standorte/{standort_id}", response_model=schemas.Standort)
def read_standort(standort_id: int, db: Session = Depends(get_db)):
    """Ein Standort nach ID"""
    standort = crud.get_standort(db, standort_id=standort_id)
    if standort is None:
        raise HTTPException(status_code=404, detail="Standort nicht gefunden")
    return standort

# ========================
# USER ENDPOINTS
# ========================

@app.get("/users", response_model=List[schemas.User])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Alle User abrufen"""
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Ein User nach ID"""
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User nicht gefunden")
    return user

@app.get("/users/email/{email}", response_model=schemas.User)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    """User nach Email suchen"""
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="User nicht gefunden")
    return user

@app.post("/users", response_model=schemas.User, status_code=201)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Neuen User erstellen (Passwort wird hier NICHT gehasht - nutze /users/register!)"""
    # Prüfe ob Email schon existiert
    existing = crud.get_user_by_email(db, email=user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email bereits registriert")
    return crud.create_user(db=db, user=user)

@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    """User löschen"""
    success = crud.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User nicht gefunden")
    return {"message": "User gelöscht"}

# ========================
# WARENKORB ENDPOINTS
# ========================

@app.get("/warenkorb/user/{user_id}", response_model=schemas.WarenkorbDetailed)
def get_user_warenkorb(user_id: int, db: Session = Depends(get_db)):
    """Aktiven Warenkorb eines Users holen (oder neuen erstellen)"""
    warenkorb = crud.get_warenkorb_by_user(db, user_id=user_id)
    
    if not warenkorb:
        # Erstelle neuen Warenkorb
        warenkorb = crud.create_warenkorb(db, user_id=user_id)
    
    # Hole mit Details
    return crud.get_warenkorb_detailed(db, warenkorb_id=warenkorb.warenkorb_id)

@app.get("/warenkorb/{warenkorb_id}", response_model=schemas.WarenkorbDetailed)
def get_warenkorb(warenkorb_id: int, db: Session = Depends(get_db)):
    """Warenkorb mit allen Positionen"""
    warenkorb = crud.get_warenkorb_detailed(db, warenkorb_id=warenkorb_id)
    if warenkorb is None:
        raise HTTPException(status_code=404, detail="Warenkorb nicht gefunden")
    return warenkorb

@app.post("/warenkorb/{warenkorb_id}/add", response_model=schemas.WarenkorbPosition)
def add_product_to_warenkorb(
    warenkorb_id: int,
    produkt_id: int,
    menge: int,
    preis_je_einheit: float,
    db: Session = Depends(get_db)
):
    """Produkt zum Warenkorb hinzufügen"""
    try:
        position = crud.add_to_warenkorb(
            db=db,
            warenkorb_id=warenkorb_id,
            produkt_id=produkt_id,
            menge=menge,
            preis_je_einheit=preis_je_einheit
        )
        return position
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/warenkorb/position/{position_id}", response_model=schemas.WarenkorbPosition)
def update_warenkorb_position_endpoint(
    position_id: int,
    menge: int,
    db: Session = Depends(get_db)
):
    """Menge einer Position aktualisieren"""
    position = crud.update_warenkorb_position(db, position_id=position_id, menge=menge)
    if position is None:
        raise HTTPException(status_code=404, detail="Position nicht gefunden")
    return position

@app.delete("/warenkorb/position/{position_id}")
def remove_from_warenkorb_endpoint(position_id: int, db: Session = Depends(get_db)):
    """Position aus Warenkorb entfernen"""
    success = crud.remove_from_warenkorb(db, position_id=position_id)
    if not success:
        raise HTTPException(status_code=404, detail="Position nicht gefunden")
    return {"message": "Position entfernt"}

@app.delete("/warenkorb/{warenkorb_id}/clear")
def clear_warenkorb_endpoint(warenkorb_id: int, db: Session = Depends(get_db)):
    """Warenkorb leeren"""
    success = crud.clear_warenkorb(db, warenkorb_id=warenkorb_id)
    return {"message": "Warenkorb geleert"}

@app.post("/warenkorb/{warenkorb_id}/checkout", response_model=schemas.Bestellung)
def checkout_warenkorb(
    warenkorb_id: int,
    bauer_id: int,
    db: Session = Depends(get_db)
):
    """Warenkorb in Bestellung umwandeln (Checkout)"""
    bestellung = crud.warenkorb_to_bestellung(db, warenkorb_id=warenkorb_id, bauer_id=bauer_id)
    if bestellung is None:
        raise HTTPException(status_code=400, detail="Warenkorb ist leer oder User hat keine Kunde-ID")
    return bestellung