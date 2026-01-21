from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from src.backend.db import Base
from datetime import datetime

# ========================
# JUNCTION TABLES (Many-to-Many)
# ========================

produkt_label = Table(
    'Produkt_Label',
    Base.metadata,
    Column('produkt_id', Integer, ForeignKey('Produkte.produkt_id')),
    Column('label_id', Integer, ForeignKey('Labels.label_id'))
)

produkt_standort = Table(
    'Produkt_Standort',
    Base.metadata,
    Column('produkt_id', Integer, ForeignKey('Produkte.produkt_id')),
    Column('standort_id', Integer, ForeignKey('Standorte.standort_id'))
)

# ========================
# MODELS
# ========================

class Ort(Base):
    __tablename__ = 'Ort'
    
    ort_id = Column(Integer, primary_key=True, index=True)
    plz = Column(Integer)
    ortsname = Column(String(20))
    
    # Relationships
    bauern = relationship("Bauer", back_populates="ort")
    standorte = relationship("Standort", back_populates="ort")


class Bauer(Base):
    __tablename__ = 'Bauern'
    
    bauer_id = Column(Integer, primary_key=True, index=True)
    firmenname = Column(String(30))
    kontaktperson = Column(String(20))
    straße = Column(String(20))
    hausnr = Column(Integer)
    ort_id = Column(Integer, ForeignKey('Ort.ort_id'))
    telefon = Column(Integer)
    email = Column(String(50))
    
    # Relationships
    ort = relationship("Ort", back_populates="bauern")
    produkte = relationship("Produkt", back_populates="bauer")
    bestellungen = relationship("Bestellung", back_populates="bauer")
    standorte = relationship("Standort", back_populates="bauer")
    user = relationship("User", foreign_keys="User.bauer_id")


class Kunde(Base):
    __tablename__ = 'Kunden'
    
    kunden_id = Column(Integer, primary_key=True, index=True)
    vorname = Column(String(50))
    nachname = Column(String(50))
    email = Column(String(50))
    
    # Relationships
    bestellungen = relationship("Bestellung", back_populates="kunde")


class User(Base):
    __tablename__ = 'Users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    passwort_hash = Column(String(255), nullable=False)
    rolle = Column(String(20), default='kunde')  # 'kunde', 'bauer', 'admin'
    erstellt_am = Column(DateTime, default=datetime.now)
    aktiv = Column(Integer, default=1)  # 1 = aktiv, 0 = deaktiviert
    
    # Optional: Verknüpfung zu Kunde/Bauer
    kunde_id = Column(Integer, ForeignKey('Kunden.kunden_id'), nullable=True)
    bauer_id = Column(Integer, ForeignKey('Bauern.bauer_id'), nullable=True)
    
    # Relationships
    warenkörbe = relationship("Warenkorb", back_populates="user")


class Produktart(Base):
    __tablename__ = 'Produktart'
    
    produktart_id = Column(Integer, primary_key=True, index=True)
    bezeichnung = Column(String(50))
    
    # Relationships
    produkte = relationship("Produkt", back_populates="produktart")


class Label(Base):
    __tablename__ = 'Labels'
    
    label_id = Column(Integer, primary_key=True, index=True)
    bezeichnung = Column(String(50))
    
    # Relationships
    produkte = relationship("Produkt", secondary=produkt_label, back_populates="labels")


class Produkt(Base):
    __tablename__ = 'Produkte'
    
    produkt_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    beschreibung = Column(String(50))
    preis = Column(Float)
    einheit = Column(String(10))
    bauern_id = Column(Integer, ForeignKey('Bauern.bauer_id'))
    produktart_id = Column(Integer, ForeignKey('Produktart.produktart_id'))
    
    # Relationships
    bauer = relationship("Bauer", back_populates="produkte")
    produktart = relationship("Produktart", back_populates="produkte")
    labels = relationship("Label", secondary=produkt_label, back_populates="produkte")
    standorte = relationship("Standort", secondary=produkt_standort, back_populates="produkte")
    bestellpositionen = relationship("Bestellposition", back_populates="produkt")


class Standort(Base):
    __tablename__ = 'Standorte'
    
    standort_id = Column(Integer, primary_key=True, index=True)
    bauer_id = Column(Integer, ForeignKey('Bauern.bauer_id'))
    bezeichnung = Column(String(50))
    adresse = Column(String(50))
    ort_id = Column(Integer, ForeignKey('Ort.ort_id'))
    koordinate = Column(Geography('POINT', srid=4326))  # PostGIS Geography Type
    
    # Relationships
    bauer = relationship("Bauer", back_populates="standorte")
    ort = relationship("Ort", back_populates="standorte")
    produkte = relationship("Produkt", secondary=produkt_standort, back_populates="standorte")


class Bestellung(Base):
    __tablename__ = 'Bestellungen'
    
    bestellung_id = Column(Integer, primary_key=True, index=True)
    kunden_id = Column(Integer, ForeignKey('Kunden.kunden_id'))
    bauer_id = Column(Integer, ForeignKey('Bauern.bauer_id'))
    datum = Column(Date)
    
    # Relationships
    kunde = relationship("Kunde", back_populates="bestellungen")
    bauer = relationship("Bauer", back_populates="bestellungen")
    positionen = relationship("Bestellposition", back_populates="bestellung")


class Bestellposition(Base):
    __tablename__ = 'Bestellposition'
    
    bestellposs_id = Column(Integer, primary_key=True, index=True)
    bestellung_id = Column(Integer, ForeignKey('Bestellungen.bestellung_id'))
    produkt_id = Column(Integer, ForeignKey('Produkte.produkt_id'))
    menge = Column(Integer)
    preis_je_einheit = Column(Float)
    
    # Relationships
    bestellung = relationship("Bestellung", back_populates="positionen")
    produkt = relationship("Produkt", back_populates="bestellpositionen")


class Warenkorb(Base):
    __tablename__ = 'Warenkorb'
    
    warenkorb_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    erstellt_am = Column(DateTime, default=datetime.now)
    aktualisiert_am = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    status = Column(String(20), default='offen')  # 'offen', 'bestellt', 'abgebrochen'
    
    # Relationships
    user = relationship("User", back_populates="warenkörbe")
    positionen = relationship("WarenkorbPosition", back_populates="warenkorb", cascade="all, delete-orphan")


class WarenkorbPosition(Base):
    __tablename__ = 'Warenkorb_Position'
    
    warenkorb_position_id = Column(Integer, primary_key=True, index=True)
    warenkorb_id = Column(Integer, ForeignKey('Warenkorb.warenkorb_id'))
    produkt_id = Column(Integer, ForeignKey('Produkte.produkt_id'))
    menge = Column(Integer)
    preis_je_einheit = Column(Float)
    
    # Relationships
    warenkorb = relationship("Warenkorb", back_populates="positionen")
    produkt = relationship("Produkt")