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
from plyer import notification

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
        notification.notify(
            title="Eksik Dosyalar",
            message="Lütfen 'YT Audio Catcher Güncelle' kısayoluna tıklayarak ilk kurulumu tamamlayın.",
            app_name="YT Audio Catcher",
            timeout=10
        )
                
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

def is_youtube_link(url):
    # Basit bir regex ile YouTube linki kontrolü
    pattern = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.be|youtube\.com)\/.+$'
    return re.match(pattern, url) is not None

class YTAudioCatcher:
    def __init__(self):
        self.last_downloaded_url = ""
        self.running = True
        self.base_dir = get_base_dir()
        
        # Binaries'i kur ve kullanacağımız dizini al
        self.bin_dir = setup_binaries()
        
        # Varsayılan Music/Youtube dizinini bul ve yoksa oluştur
        self.music_dir = os.path.join(os.path.expanduser("~\\Music"), "Youtube")
        os.makedirs(self.music_dir, exist_ok=True)
        
        # yt-dlp ve ffmpeg artık AppData dizininde yer alacak
        self.ytdlp_path = os.path.join(self.bin_dir, "yt-dlp.exe")
        self.ffmpeg_path = self.bin_dir
        
    def download_audio(self, url):
        try:
            output_template = os.path.join(self.music_dir, "%(title)s.%(ext)s")
            
            # Belirtilen dizinde yt-dlp.exe varsa onu kullan, yoksa sistemdeki yt-dlp'yi kullanmayı dene
            exe_to_run = self.ytdlp_path if os.path.exists(self.ytdlp_path) else "yt-dlp"
            
            command = [
                exe_to_run,
                "-U", # Uygulamayı güncellemeye çalışır (eğer yetkisi varsa)
                "-S", "codec", 
                "-f", "ba",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "320K",
                "--output", output_template,
                "--ffmpeg-location", self.ffmpeg_path,
                url
            ]
            
            # Komut satırı (CMD) penceresinin açılmasını engeller
            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NO_WINDOW
                
            result = subprocess.run(command, capture_output=True, text=True, creationflags=creationflags)
            
            if result.returncode == 0:
                title = "Şarkı"
                # yt-dlp çıktısından dosya adını/şarkı adını ayrıştırmaya çalış
                match = re.search(r'\[ExtractAudio\] Destination:\s*(.+)\.mp3', result.stdout)
                if match:
                    title = os.path.basename(match.group(1))
                
                notification.notify(
                    title="İndirme Tamamlandı",
                    message=f"{title} indirildi.",
                    app_name="YT Audio Catcher",
                    timeout=5
                )
            else:
                notification.notify(
                    title="İndirme Hatası",
                    message="İndirme başarısız oldu, hata detayları için loglara bakınız.",
                    app_name="YT Audio Catcher",
                    timeout=5
                )
                print(f"Hata detayı: {result.stderr}")
        except Exception as e:
            notification.notify(
                title="Uygulama Hatası",
                message=f"Beklenmeyen bir hata oluştu: {str(e)}",
                app_name="YT Audio Catcher",
                timeout=5
            )

    def monitor_clipboard(self):
        while self.running:
            try:
                # pyperclip.paste() panodaki metni döndürür
                current_clipboard = pyperclip.paste().strip()
                # Eğer daha önce indirdiğimiz link değilse ve youtube linki ise
                if current_clipboard != self.last_downloaded_url and is_youtube_link(current_clipboard):
                    self.last_downloaded_url = current_clipboard
                    
                    notification.notify(
                        title="İndirme Başladı",
                        message="YouTube linki algılandı, mp3 indiriliyor...",
                        app_name="YT Audio Catcher",
                        timeout=3
                    )
                    
                    # Ana thread'i (pano kontrolünü) bloklamamak için farklı thread'de indir
                    dl_thread = threading.Thread(target=self.download_audio, args=(current_clipboard,))
                    dl_thread.start()
            except Exception:
                pass
            time.sleep(1)

    def stop(self, icon, item):
        self.running = False
        icon.stop()

    def run(self):
        monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        monitor_thread.start()
        
        menu = pystray.Menu(pystray.MenuItem('Çıkış', self.stop))
        icon = pystray.Icon("YT Audio Catcher", create_image(), "YouTube Downloader", menu)
        icon.run()

if __name__ == '__main__':
    app = YTAudioCatcher()
    app.run()
