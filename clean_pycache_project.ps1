#!/usr/bin/env pwsh
# -*- coding: utf-8 -*-
# Project cache cleanup script - for development projects, excluding virtual environments
# Function: Cleans __pycache__ folders and .pyc files in project code, but keeps virtual environments

param(
    [string]$Path = ".",
    [switch]$Verbose
)

# Set console encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "🧹 Project Python Cache Cleaner" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray
Write-Host "📝 Note: Only cleans project code cache, keeps virtual environments" -ForegroundColor Yellow
Write-Host ""

# Get absolute path
$TargetPath = Resolve-Path $Path -ErrorAction SilentlyContinue
if (-not $TargetPath) {
    Write-Host "❌ Path does not exist: $Path" -ForegroundColor Red
    exit 1
}

Write-Host "📁 Scanning path: $TargetPath" -ForegroundColor Green
Write-Host ""

# Statistics variables
$CacheDirectories = 0
$PycFiles = 0
$TotalSize = 0

# Virtual environment directory patterns
$VenvPatterns = @(
    ".venv",
    "venv", 
    ".env",
    "env",
    ".virtualenv",
    "virtualenv",
    "__pycache__"
)

try {
    # Find all __pycache__ directories (excluding virtual environments)
    Write-Host "🔍 Searching for project __pycache__ directories..." -ForegroundColor Yellow
    
    $AllPycacheDirs = Get-ChildItem -Path $TargetPath -Recurse -Directory -Name "__pycache__" -ErrorAction SilentlyContinue
    
    # Filter out directories in virtual environments
    $PycacheDirs = $AllPycacheDirs | Where-Object {
        $dirPath = Join-Path $TargetPath $_
        $relativePath = $_.Replace('\', '/')
        
        # Check if in virtual environment directory
        $isInVenv = $false
        foreach ($pattern in $VenvPatterns[0..5]) {  # Exclude __pycache__ itself
            if ($relativePath -match "[\\/]$pattern[\\/]" -or $relativePath -match "^$pattern[\\/]") {
                $isInVenv = $true
                break
            }
        }
        
        return -not $isInVenv
    }
    
    if ($PycacheDirs) {
        foreach ($Dir in $PycacheDirs) {
            $FullPath = Join-Path $TargetPath $Dir
            
            # Calculate directory size
            try {
                $DirSize = (Get-ChildItem -Path $FullPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
                if ($DirSize) {
                    $TotalSize += $DirSize
                }
            } catch {
                $DirSize = 0
            }
            
            if ($Verbose) {
                $SizeStr = if ($DirSize -gt 0) { " ({0:N2} KB)" -f ($DirSize / 1KB) } else { "" }
                Write-Host "  📂 $FullPath$SizeStr" -ForegroundColor Gray
            }
            
            # Delete directory
            try {
                Remove-Item -Path $FullPath -Recurse -Force
                if ($Verbose) {
                    Write-Host "  ✅ Deleted: $FullPath" -ForegroundColor Green
                }
            } catch {
                Write-Host "  ❌ Deletion failed: $FullPath - $($_.Exception.Message)" -ForegroundColor Red
            }
            
            $CacheDirectories++
        }
    }
    
    # Find all .pyc files (excluding virtual environments)
    Write-Host "🔍 Searching for project .pyc files..." -ForegroundColor Yellow
    
    $AllPycFiles = Get-ChildItem -Path $TargetPath -Recurse -File -Filter "*.pyc" -ErrorAction SilentlyContinue
    
    # Filter out files in virtual environments
    $PycFiles_List = $AllPycFiles | Where-Object {
        $relativePath = $_.FullName.Replace($TargetPath, "").Replace('\', '/')
        
        # Check if in virtual environment directory
        $isInVenv = $false
        foreach ($pattern in $VenvPatterns[0..5]) {  # Exclude __pycache__ itself
            if ($relativePath -match "[\\/]$pattern[\\/]") {
                $isInVenv = $true
                break
            }
        }
        
        return -not $isInVenv
    }
    
    if ($PycFiles_List) {
        foreach ($File in $PycFiles_List) {
            $FileSize = $File.Length
            $TotalSize += $FileSize
            
            if ($Verbose) {
                $SizeStr = " ({0:N2} KB)" -f ($FileSize / 1KB)
                Write-Host "  📄 $($File.FullName)$SizeStr" -ForegroundColor Gray
            }
            
            # Delete file
            try {
                Remove-Item -Path $File.FullName -Force
                if ($Verbose) {
                    Write-Host "  ✅ Deleted: $($File.FullName)" -ForegroundColor Green
                }
            } catch {
                Write-Host "  ❌ Deletion failed: $($File.FullName) - $($_.Exception.Message)" -ForegroundColor Red
            }
            
            $PycFiles++
        }
    }
    
    # Display statistics
    Write-Host ""
    Write-Host "📊 Cleanup statistics:" -ForegroundColor Cyan
    Write-Host "  Project __pycache__ directories: $CacheDirectories" -ForegroundColor White
    Write-Host "  Project .pyc files: $PycFiles" -ForegroundColor White
    
    if ($TotalSize -gt 0) {
        $SizeStr = if ($TotalSize -gt 1MB) {
            "{0:N2} MB" -f ($TotalSize / 1MB)
        } elseif ($TotalSize -gt 1KB) {
            "{0:N2} KB" -f ($TotalSize / 1KB)
        } else {
            "$TotalSize bytes"
        }
        Write-Host "  Freed up space: $SizeStr" -ForegroundColor White
    }
    
    Write-Host ""
    if ($CacheDirectories -gt 0 -or $PycFiles -gt 0) {
        Write-Host "✅ Project cache cleanup completed!" -ForegroundColor Green
        Write-Host "ℹ️  Virtual environment cache has been preserved" -ForegroundColor Blue
    } else {
        Write-Host "ℹ️  No project cache files found for cleanup" -ForegroundColor Blue
    }

} catch {
    Write-Host ""
    Write-Host "❌ An error occurred during cleanup: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 Script execution completed" -ForegroundColor Cyan
