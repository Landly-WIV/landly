from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn

app = FastAPI()

# CORS für lokale Entwicklung
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporäre Dummy-Daten (später aus DB)
DUMMY_PRODUCTS = [
    {
        "id": 1,
        "name": "Bio-Gemüse",
        "beschreibung": "Frisch geerntetes Bio-Gemüse von lokalen Bauern.",
        "preis": 2.50,
        "einheit": "kg",
        "bauer_id": 1,
        "kategorie": "Gemüse"
    },
    {
        "id": 2,
        "name": "Bio-Obst",
        "beschreibung": "Frisch geerntetes Bio-Obst von lokalen Bauern.",
        "preis": 1.50,
        "einheit": "kg",
        "bauer_id": 2,
        "kategorie": "Obst"
    }
]

DUMMY_FARMERS = [
    {
        "id": 1,
        "name": "Birkenhof Schmidt",
        "adresse": "Dorfstraße 23, 12345 Grünwald",
        "oeffnungszeiten": "Mo-Fr: 8:00-18:00\nSa: 8:00-14:00\nSo: Geschlossen",
        "telefon": "+49 123 456789",
        "email": "info@birkenhof-schmidt.de",
        "distanz": 12.5
    }
]

@app.get("/")
async def root():
    """Willkommensnachricht"""
    return {"message": "Willkommen zur Landwirtschafts-App API!"}

@app.get("/api/products")
async def get_products(
    search: Optional[str] = None,
    kategorie: Optional[str] = None,
    limit: int = 100
):
    """
    Alle Produkte abrufen mit optionaler Suche
    
    - search: Suchbegriff für Name
    - kategorie: Filtere nach Kategorie
    - limit: Max. Anzahl Ergebnisse
    """
    products = DUMMY_PRODUCTS
    
    # Suche nach Name
    if search:
        products = [p for p in products 
                   if search.lower() in p["name"].lower()]
    
    # Filter nach Kategorie
    if kategorie:
        products = [p for p in products 
                   if p["kategorie"].lower() == kategorie.lower()]
    
    return products[:limit]

@app.get("/api/products/{product_id}")
async def get_product(product_id: int):
    """Ein spezifisches Produkt abrufen"""
    product = next((p for p in DUMMY_PRODUCTS if p["id"] == product_id), None)
    
    if not product:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden")
    
    return product

@app.get("/api/farmers")
async def get_farmers(
    search: Optional[str] = None,
    max_distanz: Optional[float] = None
):
    """
    Alle Bauern abrufen mit optionaler Suche
    
    - search: Suchbegriff für Name
    - max_distanz: Maximale Entfernung in km
    """
    farmers = DUMMY_FARMERS
    
    # Suche nach Name
    if search:
        farmers = [f for f in farmers 
                  if search.lower() in f["name"].lower()]
    
    # Filter nach Distanz
    if max_distanz:
        farmers = [f for f in farmers 
                  if f["distanz"] <= max_distanz]
    
    return farmers

@app.get("/api/farmers/{farmer_id}")
async def get_farmer(farmer_id: int):
    """Ein spezifischer Bauer abrufen"""
    farmer = next((f for f in DUMMY_FARMERS if f["id"] == farmer_id), None)
    
    if not farmer:
        raise HTTPException(status_code=404, detail="Bauer nicht gefunden")
    
    return farmer

@app.get("/api/farmers/{farmer_id}/products")
async def get_farmer_products(farmer_id: int):
    """Alle Produkte eines Bauern"""
    products = [p for p in DUMMY_PRODUCTS if p["bauer_id"] == farmer_id]
    return products

if __name__ == "__main__":
    # Server starten
    uvicorn.run(app, host="127.0.0.1", port=8000)

