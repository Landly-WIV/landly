"""
Debug Script - Prüft die Standorte-Tabelle in der Datenbank
"""
import sys
from pathlib import Path

# Python-Path konfigurieren
ROOT_DIR = Path(__file__).parent
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from backend.db import engine
from sqlalchemy import text

print("=" * 60)
print("🔍 DATENBANK DEBUG")
print("=" * 60)

with engine.connect() as conn:
    # 1. Zeige alle Tabellen mit "standort" im Namen
    print("\n1️⃣ Tabellen mit 'standort' im Namen:")
    result = conn.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name ILIKE '%standort%'
        AND table_schema = 'public'
    """))
    tables = result.fetchall()
    if tables:
        for table in tables:
            print(f"   ✅ {table[0]}")
    else:
        print("   ❌ Keine Tabellen gefunden!")
    
    # 2. Prüfe ob "Standorte" existiert (mit großem S)
    print("\n2️⃣ Prüfe Tabelle 'Standorte':")
    result = conn.execute(text("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'Standorte'
            AND table_schema = 'public'
        )
    """))
    exists = result.scalar()
    
    if exists:
        print("   ✅ Tabelle 'Standorte' existiert")
        
        # Zeige Struktur
        print("\n3️⃣ Spalten in 'Standorte':")
        result = conn.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'Standorte'
            ORDER BY ordinal_position
        """))
        for col in result.fetchall():
            print(f"   - {col[0]}: {col[1]}")
        
        # Zähle Einträge
        print("\n4️⃣ Anzahl Einträge:")
        result = conn.execute(text('SELECT COUNT(*) FROM "Standorte"'))
        count = result.scalar()
        print(f"   📊 {count} Standorte gesamt")
        
        if count > 0:
            # Zeige erste 5 Einträge
            print("\n5️⃣ Erste 5 Standorte:")
            result = conn.execute(text("""
                SELECT standort_id, bezeichnung, bauer_id, 
                       koordinate IS NOT NULL as hat_koordinate,
                       ST_AsText(koordinate) as koordinate_text
                FROM "Standorte"
                LIMIT 5
            """))
            for row in result.fetchall():
                print(f"   ID: {row[0]} | {row[1]} | Bauer: {row[2]}")
                print(f"      Hat Koordinate: {row[3]}")
                if row[4]:
                    print(f"      Koordinate: {row[4]}")
            
            # Zähle mit Koordinaten
            print("\n6️⃣ Standorte mit Koordinaten:")
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM "Standorte" 
                WHERE koordinate IS NOT NULL
            """))
            count_coords = result.scalar()
            print(f"   📍 {count_coords} von {count} haben Koordinaten")
    else:
        print("   ❌ Tabelle 'Standorte' existiert NICHT")
        print("\n   Versuche 'standorte' (klein geschrieben)...")
        
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'standorte'
                AND table_schema = 'public'
            )
        """))
        exists_lower = result.scalar()
        
        if exists_lower:
            print("   ✅ Tabelle 'standorte' (klein) existiert!")
            print("   💡 LÖSUNG: Ändere models.py __tablename__ zurück auf 'standorte'")

print("\n" + "=" * 60)
