uv sync

# Zum Testen
uv run flet main.py
uv run flet run --web main.py
- Backend sollte laufen 
- config.py ist auf lokal gestellt

# Zum Kompilieren
uv run flet build web
uv run flet serve --port 8081 build/web
