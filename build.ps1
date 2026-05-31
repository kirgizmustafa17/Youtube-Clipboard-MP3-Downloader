# This script builds the executables using PyInstaller.
# Ensure you are running this in the project directory.

Write-Host "Building updater.exe..."
.\venv\Scripts\pyinstaller --noconfirm --onefile --windowed --icon="icon.ico" --hidden-import plyer.platforms.win.notification --name "updater" updater.py

Write-Host "Building YtDownloader.exe..."
.\venv\Scripts\pyinstaller --noconfirm --onefile --windowed --icon="icon.ico" --add-data "icon.ico;." --hidden-import plyer.platforms.win.notification --name "YtDownloader" main.py

Write-Host "Build complete. Check the 'dist' folder for YtDownloader.exe and updater.exe."
