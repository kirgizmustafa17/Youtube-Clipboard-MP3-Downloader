# release.ps1
# Bu script, dist klasöründeki güncel .exe dosyalarından release çıktılarını hazırlar.

Write-Host "========================================="
Write-Host "   YT Audio Catcher Release Hazirlayici  "
Write-Host "========================================="

# 1. Portable Sürüm İçin ZIP Oluşturma
$zipPath = "dist\YTAudioCatcher.zip"
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

Write-Host "`n[1/2] Portable ZIP dosyasi hazirlaniyor..."
if ((Test-Path "dist\YTAudioCatcher.exe") -and (Test-Path "dist\updater.exe")) {
    Compress-Archive -Path "dist\YTAudioCatcher.exe", "dist\updater.exe" -DestinationPath $zipPath -Force
    Write-Host "Basarili: $zipPath olusturuldu." -ForegroundColor Green
} else {
    Write-Host "HATA: dist klasöründe YTAudioCatcher.exe veya updater.exe bulunamadi!" -ForegroundColor Red
    Write-Host "Lütfen önce 'build.ps1' calistirip dosyalari derleyin." -ForegroundColor Yellow
    exit 1
}

# 2. Inno Setup ile Setup.exe Derleme
Write-Host "`n[2/2] Setup dosyasi (Inno Setup) derleniyor..."

# Inno Setup Compiler'in (ISCC.exe) olasi yollari
$iscc_paths = @(
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe",
    "C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
    "C:\Program Files\Inno Setup 5\ISCC.exe"
)

$iscc = $null
foreach ($path in $iscc_paths) {
    if (Test-Path $path) {
        $iscc = $path
        break
    }
}

if ($iscc) {
    # ISCC.exe ile komut satirindan sessiz derleme
    $process = Start-Process -FilePath $iscc -ArgumentList "`"setup.iss`"" -Wait -NoNewWindow -PassThru
    if ($process.ExitCode -eq 0) {
        Write-Host "Basarili: dist\YTAudioCatcher_Setup.exe olusturuldu." -ForegroundColor Green
    } else {
        Write-Host "HATA: Setup derlenirken bir sorun olustu. (Hata Kodu: $($process.ExitCode))" -ForegroundColor Red
    }
} else {
    Write-Host "UYARI: Sisteminizde Inno Setup Compiler (ISCC.exe) bulunamadi!" -ForegroundColor Yellow
    Write-Host "Setup dosyasi olusturulamadi. Lütfen Inno Setup'in kurulu oldugundan emin olun." -ForegroundColor Yellow
}

Write-Host "`nRelease dosyalari dist\ klasöründe hazir!" -ForegroundColor Cyan
Write-Host "========================================="
