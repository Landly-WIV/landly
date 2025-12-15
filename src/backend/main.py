from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
from db import engine, get_db

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