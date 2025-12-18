from sqlalchemy.orm import Session, joinedload
from src.backend import models, schemas
from typing import List, Optional

# ========================
# PRODUKT CRUD
# ========================

def get_produkte(db: Session, skip: int = 0, limit: int = 100) -> List[models.Produkt]:
    """Alle Produkte abrufen"""
    return db.query(models.Produkt).offset(skip).limit(limit).all()

def get_produkt(db: Session, produkt_id: int) -> Optional[models.Produkt]:
    """Ein Produkt nach ID"""
    return db.query(models.Produkt).filter(models.Produkt.produkt_id == produkt_id).first()

def get_produkt_detailed(db: Session, produkt_id: int) -> Optional[models.Produkt]:
    """Ein Produkt mit allen Relationships (Bauer, Labels, etc.)"""
    return db.query(models.Produkt)\
        .options(
            joinedload(models.Produkt.bauer),
            joinedload(models.Produkt.produktart),
            joinedload(models.Produkt.labels)
        )\
        .filter(models.Produkt.produkt_id == produkt_id)\
        .first()

def create_produkt(db: Session, produkt: schemas.ProduktCreate) -> models.Produkt:
    """Neues Produkt erstellen"""
    db_produkt = models.Produkt(**produkt.model_dump())
    db.add(db_produkt)
    db.commit()
    db.refresh(db_produkt)
    return db_produkt

def update_produkt(db: Session, produkt_id: int, produkt: schemas.ProduktCreate) -> Optional[models.Produkt]:
    """Produkt aktualisieren"""
    db_produkt = get_produkt(db, produkt_id)
    if db_produkt:
        for key, value in produkt.model_dump(exclude_unset=True).items():
            setattr(db_produkt, key, value)
        db.commit()
        db.refresh(db_produkt)
    return db_produkt

def delete_produkt(db: Session, produkt_id: int) -> bool:
    """Produkt löschen"""
    db_produkt = get_produkt(db, produkt_id)
    if db_produkt:
        db.delete(db_produkt)
        db.commit()
        return True
    return False

# ========================
# BAUER CRUD
# ========================

def get_bauern(db: Session, skip: int = 0, limit: int = 100) -> List[models.Bauer]:
    """Alle Bauern abrufen"""
    return db.query(models.Bauer).offset(skip).limit(limit).all()

def get_bauer(db: Session, bauer_id: int) -> Optional[models.Bauer]:
    """Ein Bauer nach ID"""
    return db.query(models.Bauer).filter(models.Bauer.bauer_id == bauer_id).first()

def create_bauer(db: Session, bauer: schemas.BauerCreate) -> models.Bauer:
    """Neuen Bauer erstellen"""
    db_bauer = models.Bauer(**bauer.model_dump())
    db.add(db_bauer)
    db.commit()
    db.refresh(db_bauer)
    return db_bauer

def update_bauer(db: Session, bauer_id: int, bauer: schemas.BauerCreate) -> Optional[models.Bauer]:
    """Bauer aktualisieren"""
    db_bauer = get_bauer(db, bauer_id)
    if db_bauer:
        for key, value in bauer.model_dump(exclude_unset=True).items():
            setattr(db_bauer, key, value)
        db.commit()
        db.refresh(db_bauer)
    return db_bauer

# ========================
# KUNDE CRUD
# ========================

def get_kunden(db: Session, skip: int = 0, limit: int = 100) -> List[models.Kunde]:
    """Alle Kunden abrufen"""
    return db.query(models.Kunde).offset(skip).limit(limit).all()

def get_kunde(db: Session, kunden_id: int) -> Optional[models.Kunde]:
    """Ein Kunde nach ID"""
    return db.query(models.Kunde).filter(models.Kunde.kunden_id == kunden_id).first()

def create_kunde(db: Session, kunde: schemas.KundeCreate) -> models.Kunde:
    """Neuen Kunde erstellen"""
    db_kunde = models.Kunde(**kunde.model_dump())
    db.add(db_kunde)
    db.commit()
    db.refresh(db_kunde)
    return db_kunde

# ========================
# BESTELLUNG CRUD
# ========================

def get_bestellungen(db: Session, skip: int = 0, limit: int = 100) -> List[models.Bestellung]:
    """Alle Bestellungen abrufen"""
    return db.query(models.Bestellung).offset(skip).limit(limit).all()

def get_bestellung(db: Session, bestellung_id: int) -> Optional[models.Bestellung]:
    """Eine Bestellung nach ID"""
    return db.query(models.Bestellung).filter(models.Bestellung.bestellung_id == bestellung_id).first()

def get_bestellung_detailed(db: Session, bestellung_id: int) -> Optional[models.Bestellung]:
    """Bestellung mit allen Details (Kunde, Bauer, Positionen)"""
    return db.query(models.Bestellung)\
        .options(
            joinedload(models.Bestellung.kunde),
            joinedload(models.Bestellung.bauer),
            joinedload(models.Bestellung.positionen).joinedload(models.Bestellposition.produkt)
        )\
        .filter(models.Bestellung.bestellung_id == bestellung_id)\
        .first()

def create_bestellung(db: Session, bestellung: schemas.BestellungCreate) -> models.Bestellung:
    """Neue Bestellung mit Positionen erstellen"""
    # Bestellung ohne Positionen erstellen
    bestellung_data = bestellung.model_dump(exclude={'positionen'})
    db_bestellung = models.Bestellung(**bestellung_data)
    db.add(db_bestellung)
    db.flush()  # ID generieren ohne zu committen
    
    # Bestellpositionen hinzufügen
    for position in bestellung.positionen:
        db_position = models.Bestellposition(
            **position.model_dump(),
            bestellung_id=db_bestellung.bestellung_id
        )
        db.add(db_position)
    
    db.commit()
    db.refresh(db_bestellung)
    return db_bestellung

# ========================
# PRODUKTART & LABEL CRUD
# ========================

def get_produktarten(db: Session) -> List[models.Produktart]:
    """Alle Produktarten"""
    return db.query(models.Produktart).all()

def get_labels(db: Session) -> List[models.Label]:
    """Alle Labels"""
    return db.query(models.Label).all()

# ========================
# STANDORT CRUD
# ========================

def get_standorte(db: Session, skip: int = 0, limit: int = 100) -> List[models.Standort]:
    """Alle Standorte abrufen"""
    return db.query(models.Standort).offset(skip).limit(limit).all()

def get_standort(db: Session, standort_id: int) -> Optional[models.Standort]:
    """Ein Standort nach ID"""
    return db.query(models.Standort).filter(models.Standort.standort_id == standort_id).first()