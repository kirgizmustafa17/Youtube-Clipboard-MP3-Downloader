import os
import sys
import time
import re
import threading
import subprocess
import shutil
import pystray
from PIL import Image, ImageDraw
import pyperclip
# pyrefly: ignore [missing-import]
from plyer import notification
from i18n import tr

def get_base_dir():
    # If compiled with pyinstaller, use the directory containing the bundled files
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    # Otherwise use the directory of the script
    return os.path.dirname(os.path.abspath(__file__))

def setup_binaries():
    # Sadece klasörün varlığını kontrol eder, indirmeler updater.exe ile yapılacak.
    appdata_dir = os.path.join(os.getenv('APPDATA'), 'YTAudioCatcher', 'bin')
    os.makedirs(appdata_dir, exist_ok=True)
    
    binaries = ['yt-dlp.exe', 'ffmpeg.exe', 'ffprobe.exe', 'deno.exe']
    missing = []
    for bin_name in binaries:
        if not os.path.exists(os.path.join(appdata_dir, bin_name)):
            missing.append(bin_name)
            
    if missing:
        try:
            notification.notify(
                title=tr("MissingFilesTitle"),
                message=tr("MissingFilesMsg"),
                app_name="YT Audio Catcher",
                timeout=10
            )
        except Exception:
            pass
                
    return appdata_dir

def create_image():
    icon_path = os.path.join(get_base_dir(), "icon.ico")
    if os.path.exists(icon_path):
        return Image.open(icon_path)
        
    # Kırmızı arkaplanlı basit bir ikon oluşturur (Eğer icon.ico bulunamazsa)
    image = Image.new('RGB', (64, 64), color=(255, 0, 0))
    dc = ImageDraw.Draw(image)
    # Ortasına beyaz bir kare
    dc.rectangle([16, 16, 48, 48], fill=(255, 255, 255))
    return image

class YtClipboardDownloader:
    def __init__(self):
        self.appdata_dir = setup_binaries()
        self.yt_dlp_path = os.path.join(self.appdata_dir, 'yt-dlp.exe')
        
        # Kullanıcının müzik klasörünün altında Youtube klasörü oluştur
        self.music_dir = os.path.join(os.path.expanduser('~'), 'Music', 'Youtube')
        os.makedirs(self.music_dir, exist_ok=True)
        
        self.last_clipboard = ""
        # YouTube URL'sini yakalamak için basit bir regex
        self.yt_pattern = re.compile(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]+')
        self.running = True
        
    def download_audio(self, url):
        try:
            # Önce videonun adını alalım
            title_cmd = [
                self.yt_dlp_path,
                '--get-title',
                url
            ]
            title_process = subprocess.run(title_cmd, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            title = title_process.stdout.strip()
            if not title:
                title = "Video"
                
            try:
                notification.notify(
                    title=tr("DownloadStartedTitle"),
                    message=tr("DownloadStartedMsg", title=title),
                    app_name="YT Audio Catcher",
                    timeout=3
                )
            except Exception:
                pass
                
            # İndirme komutu (ffmpeg yolunu belirterek)
            download_cmd = [
                self.yt_dlp_path,
                '-f', 'ba',
                '--extract-audio',
                '--audio-format', 'mp3',
                '--audio-quality', '320K',
                '--output', os.path.join(self.music_dir, '%(title)s.%(ext)s'),
                '--ffmpeg-location', self.appdata_dir,
                url
            ]
            
            subprocess.run(download_cmd, creationflags=subprocess.CREATE_NO_WINDOW)
            
            try:
                notification.notify(
                    title=tr("DownloadSuccessTitle"),
                    message=tr("DownloadSuccessMsg", title=title),
                    app_name="YT Audio Catcher",
                    timeout=5
                )
            except Exception:
                pass
                
        except Exception as e:
            try:
                notification.notify(
                    title=tr("DownloadErrorTitle"),
                    message=tr("DownloadErrorMsg", error=str(e)),
                    app_name="YT Audio Catcher",
                    timeout=5
                )
            except Exception:
                pass
            
    def monitor_clipboard(self):
        try:
            notification.notify(
                title=tr("AppRunningTitle"),
                message=tr("AppRunningMsg"),
                app_name="YT Audio Catcher",
                timeout=3
            )
        except Exception:
            pass
            
        while self.running:
            try:
                current_clipboard = pyperclip.paste()
                if current_clipboard != self.last_clipboard:
                    self.last_clipboard = current_clipboard
                    
                    if self.yt_pattern.match(current_clipboard):
                        # İndirme işlemini ayrı bir thread'de başlat
                        threading.Thread(target=self.download_audio, args=(current_clipboard,), daemon=True).start()
                        
            except Exception:
                pass
            time.sleep(1)
            
    def stop(self, icon, item):
        self.running = False
        icon.stop()
        
    def update_app(self, icon, item):
        updater_path = os.path.join(get_base_dir(), 'updater.exe')
        if os.path.exists(updater_path):
            subprocess.Popen([updater_path])

def main():
    app = YtClipboardDownloader()
    
    # Arka plan okuyucu thread'i
    monitor_thread = threading.Thread(target=app.monitor_clipboard, daemon=True)
    monitor_thread.start()
    
    # Sistem tepsisi (System Tray) simgesi
    menu = pystray.Menu(
        pystray.MenuItem(tr("MenuUpdate"), app.update_app),
        pystray.MenuItem(tr("MenuExit"), app.stop)
    )
    icon = pystray.Icon("YT Audio Catcher", create_image(), "YT Audio Catcher", menu)
    icon.run()

if __name__ == '__main__':
    main()
