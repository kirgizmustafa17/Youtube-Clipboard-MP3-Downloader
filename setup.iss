[Setup]
AppName=YtDownloader
AppVersion=1.0
DefaultDirName={userappdata}\YtClipboardDownloader
DefaultGroupName=YtDownloader
OutputDir=.\dist
OutputBaseFilename=YtDownloader_Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
SetupIconFile=icon.ico

[Files]
Source: "dist\YtDownloader.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\updater.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\YtDownloader"; Filename: "{app}\YtDownloader.exe"
Name: "{group}\YtDownloader Güncelle"; Filename: "{app}\updater.exe"
Name: "{userdesktop}\YtDownloader"; Filename: "{app}\YtDownloader.exe"; Tasks: desktopicon
Name: "{userdesktop}\YtDownloader Güncelle"; Filename: "{app}\updater.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Masaüstü kısayollarını oluştur"; GroupDescription: "Ek Kısayollar:"

[Run]
Filename: "{app}\updater.exe"; Description: "Gerekli altyapı dosyalarını indir (yt-dlp, ffmpeg, deno)"; Flags: postinstall nowait
