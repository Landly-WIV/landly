from sqlalchemy.orm import Session, joinedload
from src.backend import models, schemas
from typing import List, Optional

# ========================
# PRODUKT CRUD
# ========================

def get_produkte(db: Session, skip: int = 0, limit: int = 100) -> List[models.Produkt]:
    """Alle Produkte mit Bauer und Produktart abrufen"""
    return db.query(models.Produkt)\
        .options(
            joinedload(models.Produkt.bauer),
            joinedload(models.Produkt.produktart)
        )\
        .offset(skip).limit(limit).all()

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

def get_standorte_mit_koordinaten(db: Session) -> List[dict]:
    """
    Holt alle Standorte mit ihren Koordinaten für die Kartenanzeige.
    Extrahiert lat/lon aus dem PostGIS geography-Feld.
    
    Returns:
        Liste von Dictionaries mit standort_id, bezeichnung, lat, lon, bauer_info
    """
    from sqlalchemy import func, text
    from geoalchemy2.functions import ST_AsText
    
    # Query mit ST_AsText um die Koordinaten als Text zu bekommen
    # Format: "POINT(longitude latitude)"
    results = db.query(
        models.Standort.standort_id,
        models.Standort.bezeichnung,
        models.Standort.adresse,
        models.Standort.bauer_id,
        models.Bauer.firmenname,
        func.ST_AsText(models.Standort.koordinate).label('koordinate_text')
    ).outerjoin(  # LEFT JOIN - zeigt auch Standorte ohne Bauer
        models.Bauer, models.Standort.bauer_id == models.Bauer.bauer_id
    ).filter(
        models.Standort.koordinate.isnot(None)  # Nur Standorte mit Koordinaten
    ).all()
    
    standorte = []
    for row in results:
        # Parse "POINT(lon lat)" String
        # Beispiel: "POINT(11.0781 49.4522)"
        if row.koordinate_text:
            try:
                # Entferne "POINT(" und ")"
                coords = row.koordinate_text.replace('POINT(', '').replace(')', '')
                lon, lat = coords.split()
                
                standorte.append({
                    'standort_id': row.standort_id,
                    'bezeichnung': row.bezeichnung or f'Standort {row.standort_id}',
                    'adresse': row.adresse or 'Keine Adresse',
                    'bauer_id': row.bauer_id,
                    'firmenname': row.firmenname or f'Hof #{row.bauer_id}' if row.bauer_id else 'Unbekannter Hof',
                    'lat': float(lat),
                    'lon': float(lon)
                })
            except Exception as e:
                print(f"⚠️ Warnung: Konnte Koordinaten nicht parsen für Standort {row.standort_id}: {e}")
                continue
    
    return standorte

# ========================
# USER CRUD
# ========================

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Alle User abrufen"""
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Ein User nach ID"""
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """User nach Email suchen"""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Neuen User erstellen (Passwort muss bereits gehasht sein!)"""
    db_user = models.User(
        email=user.email,
        passwort_hash=user.passwort,  # Wird von auth.py gehasht übergeben
        rolle=user.rolle,
        kunde_id=user.kunde_id,
        bauer_id=user.bauer_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_data: dict) -> Optional[models.User]:
    """User aktualisieren"""
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user_data.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """User löschen"""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# ========================
# WARENKORB CRUD
# ========================

def get_warenkorb_by_user(db: Session, user_id: int) -> Optional[models.Warenkorb]:
    """Aktiven Warenkorb eines Users holen (Status 'offen')"""
    return db.query(models.Warenkorb)\
        .filter(models.Warenkorb.user_id == user_id)\
        .filter(models.Warenkorb.status == 'offen')\
        .first()

def get_warenkorb_detailed(db: Session, warenkorb_id: int) -> Optional[models.Warenkorb]:
    """Warenkorb mit allen Positionen und Produkten"""
    return db.query(models.Warenkorb)\
        .options(
            joinedload(models.Warenkorb.positionen).joinedload(models.WarenkorbPosition.produkt)
        )\
        .filter(models.Warenkorb.warenkorb_id == warenkorb_id)\
        .first()

def create_warenkorb(db: Session, user_id: int) -> models.Warenkorb:
    """Neuen leeren Warenkorb für User erstellen"""
    db_warenkorb = models.Warenkorb(
        user_id=user_id,
        status='offen'
    )
    db.add(db_warenkorb)
    db.commit()
    db.refresh(db_warenkorb)
    return db_warenkorb

def add_to_warenkorb(
    db: Session,
    warenkorb_id: int,
    produkt_id: int,
    menge: int,
    preis_je_einheit: float
) -> models.WarenkorbPosition:
    """Produkt zum Warenkorb hinzufügen"""
    # Prüfe ob Produkt schon im Warenkorb
    existing = db.query(models.WarenkorbPosition)\
        .filter(models.WarenkorbPosition.warenkorb_id == warenkorb_id)\
        .filter(models.WarenkorbPosition.produkt_id == produkt_id)\
        .first()
    
    if existing:
        # Menge erhöhen
        existing.menge += menge
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Neue Position erstellen
        db_position = models.WarenkorbPosition(
            warenkorb_id=warenkorb_id,
            produkt_id=produkt_id,
            menge=menge,
            preis_je_einheit=preis_je_einheit
        )
        db.add(db_position)
        db.commit()
        db.refresh(db_position)
        return db_position

def remove_from_warenkorb(db: Session, position_id: int) -> bool:
    """Position aus Warenkorb entfernen"""
    position = db.query(models.WarenkorbPosition)\
        .filter(models.WarenkorbPosition.warenkorb_position_id == position_id)\
        .first()
    if position:
        db.delete(position)
        db.commit()
        return True
    return False

def update_warenkorb_position(
    db: Session,
    position_id: int,
    menge: int
) -> Optional[models.WarenkorbPosition]:
    """Menge einer Warenkorb-Position aktualisieren"""
    position = db.query(models.WarenkorbPosition)\
        .filter(models.WarenkorbPosition.warenkorb_position_id == position_id)\
        .first()
    if position:
        position.menge = menge
        db.commit()
        db.refresh(position)
    return position

def clear_warenkorb(db: Session, warenkorb_id: int) -> bool:
    """Alle Positionen aus Warenkorb entfernen"""
    db.query(models.WarenkorbPosition)\
        .filter(models.WarenkorbPosition.warenkorb_id == warenkorb_id)\
        .delete()
    db.commit()
    return True

def warenkorb_to_bestellung(db: Session, warenkorb_id: int, bauer_id: int) -> Optional[models.Bestellung]:
    """Warenkorb in Bestellung umwandeln"""
    warenkorb = get_warenkorb_detailed(db, warenkorb_id)
    if not warenkorb or not warenkorb.positionen:
        return None
    
    # Hole User-Daten
    user = get_user(db, warenkorb.user_id)
    if not user or not user.kunde_id:
        return None
    
    # Erstelle Bestellung
    from datetime import date
    db_bestellung = models.Bestellung(
        kunden_id=user.kunde_id,
        bauer_id=bauer_id,
        datum=date.today()
    )
    db.add(db_bestellung)
    db.flush()
    
    # Kopiere Positionen
    for position in warenkorb.positionen:
        db_position = models.Bestellposition(
            bestellung_id=db_bestellung.bestellung_id,
            produkt_id=position.produkt_id,
            menge=position.menge,
            preis_je_einheit=position.preis_je_einheit
        )
        db.add(db_position)
    
    # Warenkorb auf 'bestellt' setzen
    warenkorb.status = 'bestellt'
    
    db.commit()
    db.refresh(db_bestellung)
    return db_bestellung