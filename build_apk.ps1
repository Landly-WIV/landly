# build_apk.ps1 - Baut die Android-APK mit schlanken Dependencies
# Verwendung: .\build_apk.ps1

Write-Host "=== Landly APK Build ===" -ForegroundColor Green

# 1. Sichere originale pyproject.toml
Copy-Item pyproject.toml pyproject.toml.bak
Write-Host "[1/4] pyproject.toml gesichert"

# 2. Ersetze dependencies mit App-only Dependencies
$content = Get-Content pyproject.toml -Raw
$content = $content -replace '(?s)dependencies = \[.*?\]', @'
dependencies = [
    "flet>=0.80.4",
    "flet-map>=0.80.4",
    "requests>=2.32.5",
]
'@
Set-Content pyproject.toml $content
Write-Host "[2/4] Dependencies auf App-only umgestellt"

# 3. APK bauen
Write-Host "[3/4] Baue APK..." -ForegroundColor Yellow
flet build apk
$buildResult = $LASTEXITCODE

# 4. Originale pyproject.toml wiederherstellen
Move-Item pyproject.toml.bak pyproject.toml -Force
Write-Host "[4/4] pyproject.toml wiederhergestellt"

if ($buildResult -eq 0) {
    Write-Host ""
    Write-Host "=== APK erfolgreich gebaut! ===" -ForegroundColor Green
    Write-Host "Datei: build\apk\app-release.apk"
} else {
    Write-Host ""
    Write-Host "=== Build fehlgeschlagen ===" -ForegroundColor Red
}
