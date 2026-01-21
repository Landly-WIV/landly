import sys
from pathlib import Path

# Füge das Root-Verzeichnis zum Python-Pfad hinzu
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.backend.db import engine
from src.backend.models import Base

# Versuche die Models zu laden
try:
    print("✅ Models erfolgreich geladen!")
    print(f"📊 Tabellen: {Base.metadata.tables.keys()}")
except Exception as e:
    print(f"❌ Fehler: {e}") 

# In test_db.py hinzufügen:
from src.backend.schemas import Produkt, ProduktCreate

print("✅ Schemas erfolgreich geladen!")