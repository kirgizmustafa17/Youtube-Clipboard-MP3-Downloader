[Setup]
AppName=YT Audio Catcher
AppVersion=1.1.0
DefaultDirName={userappdata}\YTAudioCatcher
DefaultGroupName=YT Audio Catcher
OutputDir=.\dist
OutputBaseFilename=YTAudioCatcher_Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
SetupIconFile=icon.ico

[Files]
Source: "dist\YTAudioCatcher.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\updater.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\YT Audio Catcher"; Filename: "{app}\YTAudioCatcher.exe"
Name: "{group}\YT Audio Catcher Güncelle"; Filename: "{app}\updater.exe"
Name: "{userdesktop}\YT Audio Catcher"; Filename: "{app}\YTAudioCatcher.exe"; Tasks: desktopicon
Name: "{userdesktop}\YT Audio Catcher Güncelle"; Filename: "{app}\updater.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Masaüstü kısayollarını oluştur"; GroupDescription: "Ek Kısayollar:"

[Run]
Filename: "{app}\updater.exe"; Description: "Gerekli altyapı dosyalarını indir (yt-dlp, ffmpeg, deno)"; Flags: postinstall nowait
