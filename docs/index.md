# Landly


## 🌾 Projektidee
!!! info "🧭 Projektbeschreibung"
    **Landly** ist eine regionale Onlineplattform, auf der Landwirte ihre Produkte direkt an Kund:innen verkaufen können.  
    Ziel des Projekts ist es, die **regionale Landwirtschaft digital zu vernetzen**, kurze Lieferwege zu fördern und den Zugang zu frischen, lokal produzierten Lebensmitteln zu erleichtern.  

    Über die Plattform können **Landwirte** ihre Produkte (z. B. Obst, Gemüse, Fleisch oder Milchprodukte) einstellen und verwalten, während **Kund:innen** diese in ihrer Umgebung suchen, filtern, bestellen und vor Ort abholen können.  
    Ein integrierter **Administrations- und Supportbereich** sorgt für Systemstabilität, Benutzerverwaltung und technische Unterstützung.  

    Damit wird Landly zu einer Art **„Ebay für Bauern"**, das Landwirte und Konsument:innen digital zusammenbringt und so den regionalen Handel **nachhaltiger, transparenter und moderner** gestaltet.




## 🧭 MoSCoW

!!! success "✅ Must have"
    - Bestellen  
    - Bestellungen verwalten (Anbieter und Kunde)  
    - Umkreissuche  
    - Systemüberwachung  
    - Benutzerverwaltung  
    - Produkt verwalten  
    - Detailsuche (Produktsuche mit Filter – Preis, Art etc.)  
    - Produktdetails (von welchem Hof, Bio/Demeter, etc.)  
    - Login (Kunde und Landwirte)  
    - Registrierung (Kunde und Landwirte)  
    - Bestellübersicht  
    - Standort ändern (PLZ Eingabe)  
    - Profil verwalten  

---

!!! warning "🟡 Should have"
    - Suchfilter (Vegan / Laktose etc.)  
    - FAQ-Bereich  
    - Benachrichtigung bei Bestellung (Kunde und Anbieter)  
    - Labeling der Produkte für die KI  
    - KI-Hilfechat  
    - Favoritenliste (Kunde kann Anbieter oder Produkte merken)

---

!!! note "🔵 Could have"
    - Produkt nicht verfügbar (ausgegraut)  
    - Supportformular (inkl. autom. E-Mail)  
    - Feedbackdatenbank  
    - Statistische Auswertung (Verkäufe)  
    - Umsatzübersicht  
    - Bewertungen / Kommentare  
    - Mehrsprachig (DE / EN)  
    - Darkmode

---

!!! failure "❌ Won't have"
    - Live Support  
    - PayPal-Anbindung  
    - Lieferung als Option  
    - Automatische Preisvorschläge (Medianwert aller Anbieter)  
    - Produktsuche nach Rezept  
    - Social Media Integration


## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

## 🚀 Entwicklung

### Dokumentation lokal starten

```bash
.venv\Scripts\python.exe -m mkdocs serve
```

Die Dokumentation ist dann verfügbar unter: `http://127.0.0.1:8000/`

### Weitere Befehle

* `mkdocs build` - Dokumentation bauen
* `mkdocs -h` - Hilfe anzeigen
