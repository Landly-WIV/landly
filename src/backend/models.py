from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from src.backend.db import Base
from datetime import datetime

# ========================
# JUNCTION TABLES (Many-to-Many)
# ========================

produkt_label = Table(
    'produkt_label',
    Base.metadata,
    Column('produkt_id', Integer, ForeignKey('produkte.produkt_id')),
    Column('label_id', Integer, ForeignKey('labels.label_id'))
)

produkt_standort = Table(
    'produkt_standort',
    Base.metadata,
    Column('produkt_id', Integer, ForeignKey('produkte.produkt_id')),
    Column('standort_id', Integer, ForeignKey('standorte.standort_id'))
)

# ========================
# MODELS
# ========================

class Ort(Base):
    __tablename__ = 'ort'
    
    ort_id = Column(Integer, primary_key=True, index=True)
    plz = Column(Integer)
    ortsname = Column(String(20))
    
    # Relationships
    bauern = relationship("Bauer", back_populates="ort")
    standorte = relationship("Standort", back_populates="ort")


class Bauer(Base):
    __tablename__ = 'bauern'
    
    bauer_id = Column(Integer, primary_key=True, index=True)
    firmenname = Column(String(30))
    kontaktperson = Column(String(20))
    straße = Column(String(20))
    hausnr = Column(Integer)
    ort_id = Column(Integer, ForeignKey('ort.ort_id'))
    telefon = Column(Integer)
    email = Column(String(50))
    
    # Relationships
    ort = relationship("Ort", back_populates="bauern")
    produkte = relationship("Produkt", back_populates="bauer")
    bestellungen = relationship("Bestellung", back_populates="bauer")
    standorte = relationship("Standort", back_populates="bauer")
    user = relationship("User", foreign_keys="User.bauer_id")


class Kunde(Base):
    __tablename__ = 'kunden'
    
    kunden_id = Column(Integer, primary_key=True, index=True)
    vorname = Column(String(50))
    nachname = Column(String(50))
    email = Column(String(50))
    
    # Relationships
    bestellungen = relationship("Bestellung", back_populates="kunde")


class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    passwort_hash = Column(String(255), nullable=False)
    rolle = Column(String(20), default='kunde')  # 'kunde', 'bauer', 'admin'
    erstellt_am = Column(DateTime, default=datetime.now)
    aktiv = Column(Integer, default=1)  # 1 = aktiv, 0 = deaktiviert
    
    # Optional: Verknüpfung zu Kunde/Bauer
    kunde_id = Column(Integer, ForeignKey('kunden.kunden_id'), nullable=True)
    bauer_id = Column(Integer, ForeignKey('bauern.bauer_id'), nullable=True)
    
    # Relationships
    warenkörbe = relationship("Warenkorb", back_populates="user")


class Produktart(Base):
    __tablename__ = 'produktart'
    
    produktart_id = Column(Integer, primary_key=True, index=True)
    bezeichnung = Column(String(50))
    
    # Relationships
    produkte = relationship("Produkt", back_populates="produktart")


class Label(Base):
    __tablename__ = 'labels'
    
    label_id = Column(Integer, primary_key=True, index=True)
    bezeichnung = Column(String(50))
    
    # Relationships
    produkte = relationship("Produkt", secondary=produkt_label, back_populates="labels")


class Produkt(Base):
    __tablename__ = 'produkte'
    
    produkt_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    beschreibung = Column(String(50))
    preis = Column(Float)
    einheit = Column(String(10))
    bauern_id = Column(Integer, ForeignKey('bauern.bauer_id'))
    produktart_id = Column(Integer, ForeignKey('produktart.produktart_id'))
    
    # Relationships
    bauer = relationship("Bauer", back_populates="produkte")
    produktart = relationship("Produktart", back_populates="produkte")
    labels = relationship("Label", secondary=produkt_label, back_populates="produkte")
    standorte = relationship("Standort", secondary=produkt_standort, back_populates="produkte")
    bestellpositionen = relationship("Bestellposition", back_populates="produkt")


class Standort(Base):
    __tablename__ = 'standorte'
    
    standort_id = Column(Integer, primary_key=True, index=True)
    bauer_id = Column(Integer, ForeignKey('bauern.bauer_id'))
    bezeichnung = Column(String(50))
    adresse = Column(String(50))
    ort_id = Column(Integer, ForeignKey('ort.ort_id'))
    koordinate = Column(Geography('POINT', srid=4326))  # PostGIS Geography Type
    
    # Relationships
    bauer = relationship("Bauer", back_populates="standorte")
    ort = relationship("Ort", back_populates="standorte")
    produkte = relationship("Produkt", secondary=produkt_standort, back_populates="standorte")


class Bestellung(Base):
    __tablename__ = 'bestellungen'
    
    bestellung_id = Column(Integer, primary_key=True, index=True)
    kunden_id = Column(Integer, ForeignKey('kunden.kunden_id'))
    bauer_id = Column(Integer, ForeignKey('bauern.bauer_id'))
    datum = Column(Date)
    
    # Relationships
    kunde = relationship("Kunde", back_populates="bestellungen")
    bauer = relationship("Bauer", back_populates="bestellungen")
    positionen = relationship("Bestellposition", back_populates="bestellung")


class Bestellposition(Base):
    __tablename__ = 'bestellposition'
    
    bestellposs_id = Column(Integer, primary_key=True, index=True)
    bestellung_id = Column(Integer, ForeignKey('bestellungen.bestellung_id'))
    produkt_id = Column(Integer, ForeignKey('produkte.produkt_id'))
    menge = Column(Integer)
    preis_je_einheit = Column(Float)
    
    # Relationships
    bestellung = relationship("Bestellung", back_populates="positionen")
    produkt = relationship("Produkt", back_populates="bestellpositionen")


class Warenkorb(Base):
    __tablename__ = 'warenkorb'
    
    warenkorb_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    erstellt_am = Column(DateTime, default=datetime.now)
    aktualisiert_am = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    status = Column(String(20), default='offen')  # 'offen', 'bestellt', 'abgebrochen'
    
    # Relationships
    user = relationship("User", back_populates="warenkörbe")
    positionen = relationship("WarenkorbPosition", back_populates="warenkorb", cascade="all, delete-orphan")


class WarenkorbPosition(Base):
    __tablename__ = 'warenkorb_position'
    
    warenkorb_position_id = Column(Integer, primary_key=True, index=True)
    warenkorb_id = Column(Integer, ForeignKey('warenkorb.warenkorb_id'))
    produkt_id = Column(Integer, ForeignKey('produkte.produkt_id'))
    menge = Column(Integer)
    preis_je_einheit = Column(Float)
    
    # Relationships
    warenkorb = relationship("Warenkorb", back_populates="positionen")
    produkt = relationship("Produkt")