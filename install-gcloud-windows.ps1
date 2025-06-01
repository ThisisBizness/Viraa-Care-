# PowerShell script to install Google Cloud SDK on Windows
# Run this as Administrator

Write-Host "🚀 Installing Google Cloud SDK for Windows..." -ForegroundColor Green

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ This script requires Administrator privileges!" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    exit 1
}

# Check if gcloud is already installed
try {
    $gcloudVersion = gcloud --version 2>$null
    if ($gcloudVersion) {
        Write-Host "✅ Google Cloud SDK is already installed!" -ForegroundColor Green
        Write-Host $gcloudVersion
        exit 0
    }
}
catch {
    Write-Host "📦 Google Cloud SDK not found. Installing..." -ForegroundColor Yellow
}

# Download and install Google Cloud SDK
$downloadUrl = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
$installerPath = "$env:TEMP\GoogleCloudSDKInstaller.exe"

Write-Host "⬇️ Downloading Google Cloud SDK installer..." -ForegroundColor Blue
try {
    Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -UseBasicParsing
    Write-Host "✅ Download completed!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to download installer: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "🔧 Running installer..." -ForegroundColor Blue
try {
    Start-Process -FilePath $installerPath -Wait
    Write-Host "✅ Installation completed!" -ForegroundColor Green
}
catch {
    Write-Host "❌ Installation failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Clean up installer
Remove-Item $installerPath -Force -ErrorAction SilentlyContinue

Write-Host "🔄 Please restart your PowerShell session and run:" -ForegroundColor Cyan
Write-Host "gcloud init" -ForegroundColor White
Write-Host "gcloud auth login" -ForegroundColor White
Write-Host "gcloud config set project YOUR_PROJECT_ID" -ForegroundColor White

Write-Host "✨ Installation complete! Google Cloud SDK is ready to use." -ForegroundColor Green 