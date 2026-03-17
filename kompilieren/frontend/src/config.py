"""
Zentrale Konfiguration für Landly App
"""

# API Backend URL
# Für Produktion (Render):
API_URL = "https://landly-ex2r.onrender.com"

# Für lokale Entwicklung auskommentieren:
# API_URL = "http://localhost:8000"


# ========================
# PRODUKT-ICON MAPPING
# ========================
# Aktueller Stand der Produktdatenbank.
# Der Key wird im Produktnamen gesucht (Teilstring-Match, case-insensitive).

PRODUKT_ICONS = {
    "tomate":            {"emoji": "🍅", "color": "#C62828", "bg": "#FFEBEE", "image": "https://images.unsplash.com/photo-1582284540020-8acbe03f4924?q=80&w=735&auto=format&fit=crop"},
    "salat":             {"emoji": "🥬", "color": "#2E7D32", "bg": "#E8F5E9", "image": "https://plus.unsplash.com/premium_photo-1675237625952-c2e254de1d13?q=80&w=687&auto=format&fit=crop"},
    "kartoffel":         {"emoji": "🥔", "color": "#795548", "bg": "#EFEBE9", "image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?q=80&w=1170&auto=format&fit=crop"},
    "rinderhack":        {"emoji": "🥩", "color": "#B71C1C", "bg": "#FFEBEE", "image": "https://plus.unsplash.com/premium_photo-1670357599582-de7232e949a0?q=80&w=687&auto=format&fit=crop"},
    "brokkoli":          {"emoji": "🥦", "color": "#2E7D32", "bg": "#E8F5E9", "image": "https://images.unsplash.com/photo-1583663848850-46af132dc08e?q=80&w=735&auto=format&fit=crop"},
    "milch":             {"emoji": "🥛", "color": "#1565C0", "bg": "#E3F2FD", "image": "https://images.unsplash.com/photo-1550583724-b2692b85b150?q=80&w=687&auto=format&fit=crop"},
    "schweinekotelett":  {"emoji": "🥩", "color": "#AD1457", "bg": "#FCE4EC", "image": "https://plus.unsplash.com/premium_photo-1723532472260-4843b8a7992a?q=80&w=1157&auto=format&fit=crop"},
    "karotten":          {"emoji": "🥕", "color": "#E65100", "bg": "#FFF3E0", "image": "https://plus.unsplash.com/premium_photo-1661870839207-d668a9857cb4?q=80&w=687&auto=format&fit=crop"},
    "birnen":            {"emoji": "🍐", "color": "#689F38", "bg": "#F1F8E9", "image": "https://images.unsplash.com/photo-1696426506268-00a41b06b956?q=80&w=687&auto=format&fit=crop"},
    "äpfel":             {"emoji": "🍎", "color": "#C62828", "bg": "#FFEBEE", "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?q=80&w=1074&auto=format&fit=crop"},
}

# Fallback wenn kein Produktname matcht
_PRODUKT_ICON_FALLBACK = {"emoji": "🧺", "color": "#4CAF50", "bg": "#E8F5E9", "image": None}


def getProIco(produktName):
    """
    Gibt Icon-Daten (emoji, color, bg) für einen Produktnamen zurück.
    Sucht per Teilstring-Match im Produktnamen (case-insensitive).
    Neues Produkt? → Einfach 1 Zeile in PRODUKT_ICONS ergänzen.
    """
    if not produktName:
        return _PRODUKT_ICON_FALLBACK

    name = produktName.lower()
    for key, val in PRODUKT_ICONS.items():
        if key in name:
            return val
    return _PRODUKT_ICON_FALLBACK
