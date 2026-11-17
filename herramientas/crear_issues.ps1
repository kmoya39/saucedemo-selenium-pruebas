# Crea en GitHub Issues un issue por cada caso de prueba de la carpeta casos_prueba.
# Requisitos: GitHub CLI instalado (winget install GitHub.cli) y sesión iniciada (gh auth login).
# Uso, desde la raíz del repositorio:  powershell -ExecutionPolicy Bypass -File herramientas\crear_issues.ps1

$ErrorActionPreference = "Stop"

# Etiquetas para clasificar los casos dentro de GitHub
gh label create "caso de prueba" --color 1D76DB --description "Caso de prueba automatizado con Selenium" --force
gh label create "defecto"        --color D73A4A --description "Defecto encontrado durante la ejecución"  --force

Get-ChildItem -Path "casos_prueba" -Filter "CP-*.md" | Sort-Object Name | ForEach-Object {
    $titulo = (Get-Content $_.FullName -Encoding UTF8 -TotalCount 1).Replace("## ", "")
    Write-Host "Creando issue: $titulo"
    gh issue create --title $titulo --body-file $_.FullName --label "caso de prueba"
}

# Defecto detectado en la ejecución (CP-10)
if (Test-Path "casos_prueba\DEF-01.md") {
    gh issue create --title "DEF-01 El ordenamiento por precio no funciona para problem_user" --body-file "casos_prueba\DEF-01.md" --label "defecto"
}
