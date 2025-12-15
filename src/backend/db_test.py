from db import engine
from models import Base

# Versuche die Models zu laden
try:
    print("✅ Models erfolgreich geladen!")
    print(f"📊 Tabellen: {Base.metadata.tables.keys()}")
except Exception as e:
    print(f"❌ Fehler: {e}") 

# In test_db.py hinzufügen:
from schemas import Produkt, ProduktCreate

print("✅ Schemas erfolgreich geladen!")