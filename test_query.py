"""
Test-Script - Direkt SQL Query für Standorte
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from backend.db import engine
from sqlalchemy import text

print("🧪 Teste SQL Query für Standorte...")

with engine.connect() as conn:
    # Der exakte Query aus der Funktion
    result = conn.execute(text("""
        SELECT 
            s.standort_id,
            s.bezeichnung,
            s.adresse,
            s.bauer_id,
            b.firmenname,
            ST_AsText(s.koordinate) as koordinate_text
        FROM "Standorte" s
        LEFT JOIN bauern b ON s.bauer_id = b.bauer_id
        WHERE s.koordinate IS NOT NULL
        AND b.bauer_id IS NOT NULL
    """))
    
    rows = result.fetchall()
    print(f"✅ {len(rows)} Standorte gefunden:\n")
    
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Bezeichnung: {row[1]}")
        print(f"Adresse: {row[2]}")
        print(f"Bauer ID: {row[3]}")
        print(f"Firmenname: {row[4]}")
        print(f"Koordinate: {row[5]}")
        
        # Parse Koordinaten
        if row[5]:
            coords = row[5].replace('POINT(', '').replace(')', '')
            lon, lat = coords.split()
            print(f"  -> Lat: {lat}, Lon: {lon}")
        print()
