# Script d'organisation du projet de stage
Write-Host "Organisation du projet de stage Dashboard Danone..." -ForegroundColor Green

# Créer les dossiers s'ils n'existent pas
$folders = @("archives_dev\tests", "archives_dev\rapports_analyses", "archives_dev\scripts_dev", "archives_dev\fichiers_backup")
foreach ($folder in $folders) {
    if (!(Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
    }
}

# Déplacer les fichiers de test
Write-Host "Deplacement des fichiers de test..." -ForegroundColor Yellow
Get-ChildItem -Name "test_*.py" | ForEach-Object {
    if (Test-Path $_) {
        Move-Item $_ "archives_dev\tests\" -Force
        Write-Host "  Deplace: $_" -ForegroundColor Cyan
    }
}

# Déplacer les rapports markdown
Write-Host "Deplacement des rapports d'analyse..." -ForegroundColor Yellow
$rapports = @(
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

foreach ($pattern in $rapports) {
    Get-ChildItem -Name $pattern -ErrorAction SilentlyContinue | ForEach-Object {
        if (Test-Path $_) {
            Move-Item $_ "archives_dev\rapports_analyses\" -Force
            Write-Host "  Deplace: $_" -ForegroundColor Cyan
        }
    }
}

# Déplacer les scripts de dev
Write-Host "Deplacement des scripts de developpement..." -ForegroundColor Yellow
$devScripts = @(
    "demo_*.py",
    "dev_server.py", 
    "quick_dev.py",
    "debug_*.py",
    "clean_production.py",
    "check_database.py",
    "configure_email_mehdi.py"
)

foreach ($script in $devScripts) {
    Get-ChildItem -Name $script -ErrorAction SilentlyContinue | ForEach-Object {
        if (Test-Path $_) {
            Move-Item $_ "archives_dev\scripts_dev\" -Force
            Write-Host "  Deplace: $_" -ForegroundColor Cyan
        }
    }
}

# Déplacer les fichiers backup
Write-Host "Deplacement des fichiers de backup..." -ForegroundColor Yellow
$backups = @("backup_*.sql", "config.example.py")
foreach ($backup in $backups) {
    Get-ChildItem -Name $backup -ErrorAction SilentlyContinue | ForEach-Object {
        if (Test-Path $_) {
            Move-Item $_ "archives_dev\fichiers_backup\" -Force
            Write-Host "  Deplace: $_" -ForegroundColor Cyan
        }
    }
}

Write-Host "Organisation terminee!" -ForegroundColor Green
