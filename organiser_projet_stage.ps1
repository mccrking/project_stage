# Script d'organisation du projet de stage
# Ce script déplace les fichiers de développement/test dans des dossiers d'archives

Write-Host "🚀 Organisation du projet de stage Dashboard Danone..." -ForegroundColor Green

# Déplacer tous les fichiers de test
Write-Host "📁 Déplacement des fichiers de test..." -ForegroundColor Yellow
$testFiles = @(
    "test_*.py"
)

foreach ($pattern in $testFiles) {
    $files = Get-ChildItem -Name $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        if (Test-Path $file) {
            Move-Item $file "archives_dev\tests\" -Force
            Write-Host "  ✅ Déplacé: $file" -ForegroundColor Cyan
        }
    }
}

# Déplacer les rapports d'analyse et fichiers markdown de développement
Write-Host "📊 Déplacement des rapports d'analyse..." -ForegroundColor Yellow
$rapportFiles = @(
    "AI_DASHBOARD_*.md",
    "ALERTS_SYSTEM_*.md",
    "REPORTS_*.md",
    "SETTINGS_SYSTEM_*.md",
    "RAPPORT_*.md",
    "RESUME_*.md",
    "*_ANALYSIS.md",
    "*_SUMMARY.md",
    "*_IMPROVEMENTS.md",
    "status_consistency_report.md",
    "ai_dashboard_improvements_report.md"
)

foreach ($pattern in $rapportFiles) {
    $files = Get-ChildItem -Name $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        if (Test-Path $file) {
            Move-Item $file "archives_dev\rapports_analyses\" -Force
            Write-Host "  ✅ Déplacé: $file" -ForegroundColor Cyan
        }
    }
}

# Déplacer les scripts de développement et fichiers demo
Write-Host "🛠️ Déplacement des scripts de développement..." -ForegroundColor Yellow
$devFiles = @(
    "demo_*.py",
    "dev_server.py",
    "quick_dev.py",
    "debug_*.py",
    "clean_production.py",
    "check_database.py",
    "configure_email_mehdi.py"
)

foreach ($file in $devFiles) {
    if (Test-Path $file) {
        Move-Item $file "archives_dev\scripts_dev\" -Force
        Write-Host "  ✅ Déplacé: $file" -ForegroundColor Cyan
    }
}

# Déplacer les fichiers de backup et configuration exemple
Write-Host "💾 Déplacement des fichiers de backup..." -ForegroundColor Yellow
$backupFiles = @(
    "backup_*.sql",
    "config.example.py"
)

foreach ($file in $backupFiles) {
    if (Test-Path $file) {
        Move-Item $file "archives_dev\fichiers_backup\" -Force
        Write-Host "  ✅ Déplacé: $file" -ForegroundColor Cyan
    }
}

Write-Host "✨ Organisation terminée!" -ForegroundColor Green
Write-Host "📂 Structure finale pour votre encadrant:" -ForegroundColor White
Write-Host "  📁 Fichiers principaux (racine)" -ForegroundColor White
Write-Host "  📁 archives_dev/ (fichiers de développement)" -ForegroundColor Gray
Write-Host "    📁 tests/ (tous les tests)" -ForegroundColor Gray
Write-Host "    📁 rapports_analyses/ (rapports de développement)" -ForegroundColor Gray
Write-Host "    📁 scripts_dev/ (scripts de développement)" -ForegroundColor Gray
Write-Host "    📁 fichiers_backup/ (sauvegardes et exemples)" -ForegroundColor Gray

# Créer un fichier README pour les archives
$readmeContent = @'
# Archives de Développement

Ce dossier contient tous les fichiers de développement, tests, et analyses qui ont été créés pendant le développement du projet mais qui ne sont pas nécessaires pour la présentation finale du stage.

## Structure:

### 📁 tests/
Tous les fichiers de test unitaires et d'intégration (test_*.py)

### 📁 rapports_analyses/
* Rapports d'analyse technique
* Documents de suivi des améliorations
* Analyses des fonctionnalités

### 📁 scripts_dev/
* Scripts de développement et debug
* Fichiers de démonstration
* Scripts de nettoyage et maintenance

### 📁 fichiers_backup/
* Sauvegardes de base de données
* Fichiers de configuration exemple

Ces fichiers peuvent être consultés si nécessaire mais ne font pas partie de la livraison principale du projet.
'@

$readmeContent | Out-File -FilePath "archives_dev\README.md" -Encoding UTF8
Write-Host "📝 README créé dans archives_dev/" -ForegroundColor Green
