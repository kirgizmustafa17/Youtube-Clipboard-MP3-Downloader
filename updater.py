import os
import sys
import urllib.request
import zipfile
import shutil
import tempfile
import threading
import tkinter as tk
from tkinter import ttk
from plyer import notification
from i18n import tr

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

class UpdaterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(tr("UpdateTitle"))
        self.geometry("400x150")
        self.resizable(False, False)
        
        # Simgeyi (Icon) ayarlama
        icon_path = os.path.join(get_base_dir(), "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass
                
        # Pencereyi ekranın ortasına konumlandırma
        self.eval('tk::PlaceWindow . center')
        
        self.label_var = tk.StringVar()
        self.label_var.set(tr("UpdateStartMsg"))
        
        self.label = ttk.Label(self, textvariable=self.label_var, wraplength=380, justify="center")
        self.label.pack(pady=20)
        
        self.progress = ttk.Progressbar(self, orient="horizontal", length=350, mode="determinate")
        self.progress.pack(pady=10)
        
        # Güncelleme işlemini UI'ı dondurmamak için alt parçacıkta (thread) başlat
        threading.Thread(target=self.update_binaries, daemon=True).start()
        
    def download_hook(self, count, block_size, total_size, name):
        if total_size > 0:
            percent = int(count * block_size * 100 / total_size)
            if percent > 100: 
                percent = 100
            self.progress["value"] = percent
            self.label_var.set(tr("DownloadingLabel", name=name, percent=percent))
            self.update_idletasks()

    def update_binaries(self):
        appdata_dir = os.path.join(os.getenv('APPDATA'), 'YTAudioCatcher', 'bin')
        os.makedirs(appdata_dir, exist_ok=True)
        temp_dir = tempfile.mkdtemp()
        
        try:
            try:
                notification.notify(
                    title=tr("UpdateTitle"),
                    message=tr("UpdateStartMsg"),
                    app_name="YT Audio Catcher",
                    timeout=3
                )
            except Exception: 
                pass
            
            # 1. yt-dlp.exe
            ytdlp_url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
            ytdlp_dest = os.path.join(appdata_dir, "yt-dlp.exe")
            urllib.request.urlretrieve(ytdlp_url, ytdlp_dest, reporthook=lambda c,b,t: self.download_hook(c,b,t, "yt-dlp.exe"))
            
            # 2. ffmpeg ve ffprobe
            ffmpeg_url = "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
            ffmpeg_zip = os.path.join(temp_dir, "ffmpeg.zip")
            urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip, reporthook=lambda c,b,t: self.download_hook(c,b,t, "ffmpeg.zip"))
            
            self.label_var.set(tr("ExtractingLabel", name="FFmpeg"))
            self.progress["mode"] = "indeterminate"
            self.progress.start(10)
            with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.filename.endswith('ffmpeg.exe') or file_info.filename.endswith('ffprobe.exe'):
                        source = zip_ref.open(file_info.filename)
                        target_name = os.path.basename(file_info.filename)
                        target_path = os.path.join(appdata_dir, target_name)
                        with open(target_path, "wb") as target:
                            shutil.copyfileobj(source, target)
            self.progress.stop()
            self.progress["mode"] = "determinate"
            self.progress["value"] = 0
            
            # 3. deno
            deno_url = "https://github.com/denoland/deno/releases/download/v2.8.1/deno-x86_64-pc-windows-msvc.zip"
            deno_zip = os.path.join(temp_dir, "deno.zip")
            urllib.request.urlretrieve(deno_url, deno_zip, reporthook=lambda c,b,t: self.download_hook(c,b,t, "deno.zip"))
            
            self.label_var.set(tr("ExtractingLabel", name="Deno"))
            self.progress["mode"] = "indeterminate"
            self.progress.start(10)
            with zipfile.ZipFile(deno_zip, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.filename.endswith('deno.exe'):
                        source = zip_ref.open(file_info.filename)
                        target_name = os.path.basename(file_info.filename)
                        target_path = os.path.join(appdata_dir, target_name)
                        with open(target_path, "wb") as target:
                            shutil.copyfileobj(source, target)
            self.progress.stop()
            self.progress["mode"] = "determinate"
            self.progress["value"] = 100
                            
            self.label_var.set(tr("UpdateCompleteLabel"))
            try:
                notification.notify(
                    title=tr("UpdateTitle"),
                    message=tr("UpdateSuccessMsg"),
                    app_name="YT Audio Catcher",
                    timeout=5
                )
            except Exception: 
                pass
            
            # Başarılı olduğunda 3 saniye sonra ekranı kapat
            self.after(3000, self.destroy)
            
        except Exception as e:
            self.progress.stop()
            self.progress["mode"] = "determinate"
            self.label_var.set(tr("UpdateErrorLabel", error=str(e)))
            try:
                notification.notify(
                    title=tr("UpdateErrorTitle"),
                    message=tr("UpdateErrorMsg", error=str(e)),
                    app_name="YT Audio Catcher",
                    timeout=5
                )
            except Exception: 
                pass
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    app = UpdaterApp()
    app.mainloop()
