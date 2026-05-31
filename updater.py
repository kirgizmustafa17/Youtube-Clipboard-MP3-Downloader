import os
import sys
import urllib.request
import zipfile
import shutil
import tempfile
from plyer import notification
from i18n import tr

def download_file(url, dest):
    print(tr("DownloadLog", url=url))
    urllib.request.urlretrieve(url, dest)

def update_binaries():
    appdata_dir = os.path.join(os.getenv('APPDATA'), 'YTAudioCatcher', 'bin')
    os.makedirs(appdata_dir, exist_ok=True)
    
    # Geçici klasör oluştur
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
        download_file(ytdlp_url, ytdlp_dest)
        
        # 2. ffmpeg ve ffprobe
        ffmpeg_url = "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        ffmpeg_zip = os.path.join(temp_dir, "ffmpeg.zip")
        download_file(ffmpeg_url, ffmpeg_zip)
        
        # Extract ffmpeg.exe and ffprobe.exe
        print(tr("ExtractFfmpeg"))
        with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if file_info.filename.endswith('ffmpeg.exe') or file_info.filename.endswith('ffprobe.exe'):
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
        print(tr("ExtractDeno"))
        with zipfile.ZipFile(deno_zip, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if file_info.filename.endswith('deno.exe'):
                    source = zip_ref.open(file_info.filename)
                    target_name = os.path.basename(file_info.filename)
                    target_path = os.path.join(appdata_dir, target_name)
                    with open(target_path, "wb") as target:
                        shutil.copyfileobj(source, target)
                        
        print(tr("UpdateSuccessLog"))
        try:
            notification.notify(
                title=tr("UpdateTitle"),
                message=tr("UpdateSuccessMsg"),
                app_name="YT Audio Catcher",
                timeout=5
            )
        except Exception:
            pass
        
    except Exception as e:
        print(tr("UpdateErrorLog", error=str(e)))
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
        # Temizlik
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    update_binaries()
