from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional, List
from datetime import date

# ========================
# ORT SCHEMAS
# ========================

class OrtBase(BaseModel):
    plz: Optional[int] = None
    ortsname: Optional[str] = None

class OrtCreate(OrtBase):
    pass

class Ort(OrtBase):
    ort_id: int
    
    class Config:
        from_attributes = True

# ========================
# BAUER SCHEMAS
# ========================

class BauerBase(BaseModel):
    firmenname: Optional[str] = None
    kontaktperson: Optional[str] = None
    straße: Optional[str] = None
    hausnr: Optional[int] = None
    ort_id: Optional[int] = None
    telefon: Optional[int] = None
    email: Optional[str] = None

class BauerCreate(BauerBase):
    pass

class Bauer(BauerBase):
    bauer_id: int
    
    class Config:
        from_attributes = True

# ========================
# KUNDE SCHEMAS
# ========================

class KundeBase(BaseModel):
    vorname: Optional[str] = None
    nachname: Optional[str] = None
    email: Optional[EmailStr] = None

class KundeCreate(KundeBase):
    pass

class Kunde(KundeBase):
    kunden_id: int
    
    class Config:
        from_attributes = True

# ========================
# PRODUKTART SCHEMAS
# ========================

class ProduktartBase(BaseModel):
    bezeichnung: Optional[str] = None

class ProduktartCreate(ProduktartBase):
    pass

class Produktart(ProduktartBase):
    produktart_id: int
    
    class Config:
        from_attributes = True

# ========================
# LABEL SCHEMAS
# ========================

class LabelBase(BaseModel):
    bezeichnung: Optional[str] = None

class LabelCreate(LabelBase):
    pass

class Label(LabelBase):
    label_id: int
    
    class Config:
        from_attributes = True

# ========================
# PRODUKT SCHEMAS
# ========================

class ProduktBase(BaseModel):
    name: Optional[str] = None
    beschreibung: Optional[str] = None
    preis: Optional[float] = None
    einheit: Optional[str] = None
    bauern_id: Optional[int] = None
    produktart_id: Optional[int] = None

class ProduktCreate(ProduktBase):
    pass

class Produkt(ProduktBase):
    produkt_id: int
    
    class Config:
        from_attributes = True

# Mit Relationships (für detaillierte Ansichten)
class ProduktDetailed(Produkt):
    bauer: Optional[Bauer] = None
    produktart: Optional[Produktart] = None
    labels: List[Label] = []
    
    class Config:
        from_attributes = True

# ========================
# STANDORT SCHEMAS
# ========================

class StandortBase(BaseModel):
    bauer_id: Optional[int] = None
    bezeichnung: Optional[str] = None
    adresse: Optional[str] = None
    ort_id: Optional[int] = None
    # koordinate wird später separat behandelt (GeoJSON)

class StandortCreate(StandortBase):
    pass

class Standort(StandortBase):
    standort_id: int
    
    class Config:
        from_attributes = True

# ========================
# BESTELLUNG SCHEMAS
# ========================

class BestellpositionBase(BaseModel):
    produkt_id: Optional[int] = None
    menge: Optional[int] = None
    preis_je_einheit: Optional[float] = None

class BestellpositionCreate(BestellpositionBase):
    pass

class Bestellposition(BestellpositionBase):
    bestellposs_id: int
    bestellung_id: int
    
    class Config:
        from_attributes = True

class BestellpositionDetailed(Bestellposition):
    produkt: Optional[Produkt] = None
    
    class Config:
        from_attributes = True

class BestellungBase(BaseModel):
    kunden_id: Optional[int] = None
    bauer_id: Optional[int] = None
    datum: Optional[date] = None

class BestellungCreate(BestellungBase):
    positionen: List[BestellpositionCreate] = []

class Bestellung(BestellungBase):
    bestellung_id: int
    
    class Config:
        from_attributes = True

class BestellungDetailed(Bestellung):
    kunde: Optional[Kunde] = None
    bauer: Optional[Bauer] = None
    positionen: List[BestellpositionDetailed] = []
    
    class Config:
        from_attributes = True