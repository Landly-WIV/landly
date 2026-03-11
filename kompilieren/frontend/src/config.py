"""
Zentrale Konfiguration für Landly App
"""
import os

# API Backend URL
# Wird automatisch aus der Umgebungsvariable API_URL gelesen.
# Lokal:  http://localhost:8000
# Render: Im Dashboard API_URL = https://landly-backend.onrender.com eintragen.
API_URL = os.environ.get("API_URL", "http://localhost:8000")


# ========================
# PRODUKT-ICON MAPPING
# ========================
# Neues Produkt? → Einfach 1 Zeile ergänzen.
# Der Key wird im Produktnamen gesucht (Teilstring-Match, case-insensitive).
# Beispiel: "kartoffel" matcht auf "Kartoffel(n)", "Bio-Kartoffeln", etc.

PRODUKT_ICONS = {
    # ──────────────────────────────────────────────────────────────
    # Neues Produkt? → 1 Zeile ergänzen + Unsplash-Link einfügen.
    # "image" = Unsplash-URL für die Produktdetailseite.
    #           None = zeigt stattdessen das Emoji groß an.
    # ──────────────────────────────────────────────────────────────
    # Gemüse / Knollengemüse
    "kartoffel":    {"emoji": "🥔", "color": "#795548", "bg": "#EFEBE9", "image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?q=80&w=1170&auto=format&fit=crop"},  # TODO: Unsplash-Link einfügen
    "rettich":      {"emoji": "🥕", "color": "#E65100", "bg": "#FFF3E0", "image": None},
    "radieschen":   {"emoji": "🥕", "color": "#C62828", "bg": "#FFEBEE", "image": None},
    "rübe":         {"emoji": "🥕", "color": "#E65100", "bg": "#FFF3E0", "image": None},
    "karotte":      {"emoji": "🥕", "color": "#E65100", "bg": "#FFF3E0", "image": None},
    "möhre":        {"emoji": "🥕", "color": "#E65100", "bg": "#FFF3E0", "image": None},
    "sellerie":     {"emoji": "🥬", "color": "#2E7D32", "bg": "#E8F5E9", "image": None},
    "zwiebel":      {"emoji": "🧅", "color": "#795548", "bg": "#EFEBE9", "image": None},
    "knoblauch":    {"emoji": "🧄", "color": "#9E9E9E", "bg": "#F5F5F5", "image": None},
    "ingwer":       {"emoji": "🫚", "color": "#F9A825", "bg": "#FFFDE7", "image": None},
    # Gemüse / Fruchtgemüse
    "tomate":       {"emoji": "🍅", "color": "#C62828", "bg": "#FFEBEE", "image": "https://images.unsplash.com/photo-1582284540020-8acbe03f4924?q=80&w=735&auto=format&fit=crop"},  # TODO: Unsplash-Link einfügen
    "paprika":      {"emoji": "🫑", "color": "#C62828", "bg": "#FFEBEE", "image": None},
    "gurke":        {"emoji": "🥒", "color": "#388E3C", "bg": "#E8F5E9", "image": None},
    "zucchini":     {"emoji": "🥒", "color": "#388E3C", "bg": "#E8F5E9", "image": None},
    "kürbis":       {"emoji": "🎃", "color": "#E65100", "bg": "#FFF3E0", "image": None},
    "aubergine":    {"emoji": "🍆", "color": "#6A1B9A", "bg": "#F3E5F5", "image": None},
    "mais":         {"emoji": "🌽", "color": "#F9A825", "bg": "#FFFDE7", "image": None},
    # Blattgemüse / Salatgemüse
    "salat":        {"emoji": "🥬", "color": "#2E7D32", "bg": "#E8F5E9", "image": "https://plus.unsplash.com/premium_photo-1675237625952-c2e254de1d13?q=80&w=687&auto=format&fit=crop"},  # TODO: Unsplash-Link einfügen
    "spinat":       {"emoji": "🥬", "color": "#1B5E20", "bg": "#E8F5E9", "image": None},
    "kohl":         {"emoji": "🥬", "color": "#2E7D32", "bg": "#E8F5E9", "image": None},
    "mangold":      {"emoji": "🥬", "color": "#2E7D32", "bg": "#E8F5E9", "image": None},
    "brokkoli":     {"emoji": "🥦", "color": "#2E7D32", "bg": "#E8F5E9", "image": None},
    "blumenkohl":   {"emoji": "🥦", "color": "#9E9E9E", "bg": "#F5F5F5", "image": None},
    # Obst
    "apfel":        {"emoji": "🍎", "color": "#C62828", "bg": "#FFEBEE", "image": None},
    "äpfel":        {"emoji": "🍎", "color": "#C62828", "bg": "#FFEBEE", "image": None},
    "birne":        {"emoji": "🍐", "color": "#689F38", "bg": "#F1F8E9", "image": None},
    "erdbeere":     {"emoji": "🍓", "color": "#C62828", "bg": "#FFEBEE", "image": None},
    "himbeere":     {"emoji": "🫐", "color": "#AD1457", "bg": "#FCE4EC", "image": None},
    "heidelbeere":  {"emoji": "🫐", "color": "#283593", "bg": "#E8EAF6", "image": None},
    "kirsche":      {"emoji": "🍒", "color": "#C62828", "bg": "#FFEBEE", "image": None},
    "pflaume":      {"emoji": "🫐", "color": "#6A1B9A", "bg": "#F3E5F5", "image": None},
    "traube":       {"emoji": "🍇", "color": "#6A1B9A", "bg": "#F3E5F5", "image": None},
    "weintraube":   {"emoji": "🍇", "color": "#6A1B9A", "bg": "#F3E5F5", "image": None},
    "orange":       {"emoji": "🍊", "color": "#E65100", "bg": "#FFF3E0", "image": None},
    "zitrone":      {"emoji": "🍋", "color": "#F9A825", "bg": "#FFFDE7", "image": None},
    "banane":       {"emoji": "🍌", "color": "#F9A825", "bg": "#FFFDE7", "image": None},
    "pfirsich":     {"emoji": "🍑", "color": "#E65100", "bg": "#FFF3E0", "image": None},
    "melone":       {"emoji": "🍈", "color": "#689F38", "bg": "#F1F8E9", "image": None},
    "wassermelone": {"emoji": "🍉", "color": "#C62828", "bg": "#FFEBEE", "image": None},
    # Tierprodukte
    "ei":           {"emoji": "🥚", "color": "#F9A825", "bg": "#FFFDE7", "image": None},
    "eier":         {"emoji": "🥚", "color": "#F9A825", "bg": "#FFFDE7", "image": None},
    "milch":        {"emoji": "🥛", "color": "#1565C0", "bg": "#E3F2FD", "image": None},
    "käse":         {"emoji": "🧀", "color": "#F9A825", "bg": "#FFFDE7", "image": None},
    "butter":       {"emoji": "🧈", "color": "#F9A825", "bg": "#FFFDE7", "image": None},
    "joghurt":      {"emoji": "🥛", "color": "#1565C0", "bg": "#E3F2FD", "image": None},
    "quark":        {"emoji": "🥛", "color": "#1565C0", "bg": "#E3F2FD", "image": None},
    "sahne":        {"emoji": "🥛", "color": "#1565C0", "bg": "#E3F2FD", "image": None},
    "fleisch":      {"emoji": "🥩", "color": "#B71C1C", "bg": "#FFEBEE", "image": None},
    "wurst":        {"emoji": "🥩", "color": "#B71C1C", "bg": "#FFEBEE", "image": None},
    "schinken":     {"emoji": "🥩", "color": "#B71C1C", "bg": "#FFEBEE", "image": None},
    "hähnchen":     {"emoji": "🍗", "color": "#E65100", "bg": "#FFF3E0", "image": None},
    "huhn":         {"emoji": "🍗", "color": "#E65100", "bg": "#FFF3E0", "image": None},
    # Getreide / Backwaren
    "brot":         {"emoji": "🍞", "color": "#6D4C41", "bg": "#EFEBE9", "image": None},
    "brötchen":     {"emoji": "🍞", "color": "#6D4C41", "bg": "#EFEBE9", "image": None},
    "mehl":         {"emoji": "🌾", "color": "#F9A825", "bg": "#FFFDE7", "image": None},
    "getreide":     {"emoji": "🌾", "color": "#F9A825", "bg": "#FFFDE7", "image": None},
    "weizen":       {"emoji": "🌾", "color": "#F9A825", "bg": "#FFFDE7", "image": None},
    "hafer":        {"emoji": "🌾", "color": "#F9A825", "bg": "#FFFDE7", "image": None},
    # Sonstige
    "honig":        {"emoji": "🍯", "color": "#FF8F00", "bg": "#FFF8E1", "image": None},
    "marmelade":    {"emoji": "🍓", "color": "#C62828", "bg": "#FFEBEE", "image": None},
    "saft":         {"emoji": "🧃", "color": "#E65100", "bg": "#FFF3E0", "image": None},
    "apfelsaft":    {"emoji": "🧃", "color": "#E65100", "bg": "#FFF3E0", "image": None},
    "kräuter":      {"emoji": "🌿", "color": "#2E7D32", "bg": "#E8F5E9", "image": None},
    "basilikum":    {"emoji": "🌿", "color": "#2E7D32", "bg": "#E8F5E9", "image": None},
    "petersilie":   {"emoji": "🌿", "color": "#2E7D32", "bg": "#E8F5E9", "image": None},
    "nuss":         {"emoji": "🥜", "color": "#795548", "bg": "#EFEBE9", "image": None},
    "nüsse":        {"emoji": "🥜", "color": "#795548", "bg": "#EFEBE9", "image": None},
    "pilz":         {"emoji": "🍄", "color": "#795548", "bg": "#EFEBE9", "image": None},
    "champignon":   {"emoji": "🍄", "color": "#795548", "bg": "#EFEBE9", "image": None},
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
