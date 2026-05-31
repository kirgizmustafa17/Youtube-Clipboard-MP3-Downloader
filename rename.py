import os

files_to_update = ['main.py', 'updater.py', 'setup.iss', 'build.ps1']

replacements = [
    # setup.iss
    ('AppName=YtDownloader', 'AppName=YT Audio Catcher'),
    ('DefaultGroupName=YtDownloader', 'DefaultGroupName=YT Audio Catcher'),
    ('OutputBaseFilename=YtDownloader_Setup', 'OutputBaseFilename=YTAudioCatcher_Setup'),
    ('YtDownloader_Setup', 'YTAudioCatcher_Setup'),
    ('dist\\YtDownloader.exe', 'dist\\YTAudioCatcher.exe'),
    ('YtDownloader.exe', 'YTAudioCatcher.exe'),
    ('YtDownloader Güncelle', 'YT Audio Catcher Güncelle'),
    ('YtDownloader', 'YT Audio Catcher'),
    ('YtClipboardDownloader', 'YTAudioCatcher'),
    
    # build.ps1
    ('--name "YtDownloader"', '--name "YTAudioCatcher"'),
]

for filepath in files_to_update:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")
