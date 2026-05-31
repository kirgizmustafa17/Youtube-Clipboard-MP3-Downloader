import os
import sys
import urllib.request
import zipfile
import shutil
import tempfile
from plyer import notification

def download_file(url, dest):
    print(f"İndiriliyor: {url}")
    urllib.request.urlretrieve(url, dest)

def update_binaries():
    appdata_dir = os.path.join(os.getenv('APPDATA'), 'YTAudioCatcher', 'bin')
    os.makedirs(appdata_dir, exist_ok=True)
    
    # Geçici klasör oluştur
    temp_dir = tempfile.mkdtemp()
    
    try:
        notification.notify(
            title="YT Audio Catcher Güncelleme",
            message="Gerekli dosyalar indiriliyor, lütfen bekleyin...",
            app_name="YT Audio Catcher",
            timeout=3
        )
        
        # 1. yt-dlp.exe
        ytdlp_url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
        ytdlp_dest = os.path.join(appdata_dir, "yt-dlp.exe")
        download_file(ytdlp_url, ytdlp_dest)
        
        # 2. ffmpeg ve ffprobe
        ffmpeg_url = "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        ffmpeg_zip = os.path.join(temp_dir, "ffmpeg.zip")
        download_file(ffmpeg_url, ffmpeg_zip)
        
        # Extract ffmpeg.exe and ffprobe.exe
        print("FFmpeg çıkartılıyor...")
        with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if file_info.filename.endswith('ffmpeg.exe') or file_info.filename.endswith('ffprobe.exe'):
                    # zip_ref.extract extracts with full path, we just want to read and write
                    source = zip_ref.open(file_info.filename)
                    target_name = os.path.basename(file_info.filename)
                    target_path = os.path.join(appdata_dir, target_name)
                    with open(target_path, "wb") as target:
                        shutil.copyfileobj(source, target)
        
        # 3. deno
        deno_url = "https://github.com/denoland/deno/releases/download/v2.8.1/deno-x86_64-pc-windows-msvc.zip"
        deno_zip = os.path.join(temp_dir, "deno.zip")
        download_file(deno_url, deno_zip)
        
        # Extract deno.exe
        print("Deno çıkartılıyor...")
        with zipfile.ZipFile(deno_zip, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if file_info.filename.endswith('deno.exe'):
                    source = zip_ref.open(file_info.filename)
                    target_name = os.path.basename(file_info.filename)
                    target_path = os.path.join(appdata_dir, target_name)
                    with open(target_path, "wb") as target:
                        shutil.copyfileobj(source, target)
                        
        print("Tüm dosyalar başarıyla güncellendi!")
        notification.notify(
            title="YT Audio Catcher Güncelleme",
            message="Güncelleme tamamlandı. Uygulamayı kullanabilirsiniz.",
            app_name="YT Audio Catcher",
            timeout=5
        )
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
        notification.notify(
            title="Güncelleme Hatası",
            message=f"Hata: {str(e)}",
            app_name="YT Audio Catcher",
            timeout=5
        )
    finally:
        # Temizlik
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    update_binaries()
