#!/usr/bin/env pwsh
# Simplified Python cache cleanup script

Write-Host "🧹 Cleaning Python cache..." -ForegroundColor Cyan

$count = 0

# Delete all __pycache__ directories
Get-ChildItem -Path . -Recurse -Directory -Name "__pycache__" -ErrorAction SilentlyContinue | ForEach-Object {
    $path = Join-Path (Get-Location) $_
    Write-Host "Deleting: $path" -ForegroundColor Gray
    Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
    $count++
}

# Delete all .pyc files
Get-ChildItem -Path . -Recurse -File -Filter "*.pyc" -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "Deleting: $($_.FullName)" -ForegroundColor Gray
    Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
    $count++
}

if ($count -gt 0) {
    Write-Host "✅ Cleanup complete! Deleted $count cache items" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No cache files found to clean" -ForegroundColor Blue
}
