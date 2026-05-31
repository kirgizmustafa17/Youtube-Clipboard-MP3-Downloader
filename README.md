# YT Audio Catcher 🎵
*A seamless YouTube to MP3 downloader running quietly in your system tray.*

[![Release](https://img.shields.io/github/v/release/kirgizmustafa17/Youtube-Clipboard-MP3-Downloader)](https://github.com/kirgizmustafa17/Youtube-Clipboard-MP3-Downloader/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

*Read this in other languages: [English](#english-description) | [Türkçe](#türkçe-açıklama)*

---

## English Description

**YT Audio Catcher** is a lightweight, background Windows application that monitors your clipboard. Whenever you copy a YouTube URL, it automatically catches it, downloads the audio in the highest quality (320kbps MP3), and saves it directly to your `Music/Youtube` folder. No need to click any buttons or paste URLs manually!

### ✨ Features
- **Auto-Clipboard Monitoring:** Just copy a YouTube link (Ctrl+C), and the download starts automatically!
- **Highest Quality:** Uses `yt-dlp` and `ffmpeg` to extract crisp 320kbps MP3 audio.
- **Smart Setup:** Automatically downloads and updates required binaries (`ffmpeg`, `yt-dlp`, `deno`) into your AppData with a clean GUI progress bar.
- **Multi-Language Support (i18n):** Automatically adapts to your Windows system language (English and Turkish supported).
- **Non-Intrusive:** Runs completely in the background (System Tray) with native Windows notifications.

### 🚀 Installation
1. Go to the [Releases page](https://github.com/kirgizmustafa17/Youtube-Clipboard-MP3-Downloader/releases).
2. Download **`YTAudioCatcher_Setup.exe`** (Recommended) or the Portable ZIP version.
3. Install and run! The application will handle downloading all required dependencies on first launch.

### 🎧 Usage
1. Ensure the app is running (you should see the 🎵 icon in your system tray on the bottom right).
2. Copy any YouTube link.
3. A notification will pop up: "Download Started".
4. Once completed, your song will be ready in `C:\Users\YourName\Music\Youtube`.

---

## Türkçe Açıklama

**YT Audio Catcher**, panonuzu (kopyaladığınız metinleri) arka planda takip eden hafif bir Windows uygulamasıdır. Herhangi bir YouTube bağlantısını kopyaladığınız anda bunu otomatik olarak algılar, videoyu en yüksek kalitede (320kbps MP3) indirir ve doğrudan `Müzik/Youtube` klasörünüze kaydeder. Herhangi bir butona basmanıza veya URL yapıştırmanıza gerek kalmaz!

### ✨ Özellikler
- **Otomatik Pano Takibi:** Sadece bir YouTube linkini kopyalayın (Ctrl+C), indirme otomatik olarak başlasın!
- **En Yüksek Kalite:** Sesleri pürüzsüz 320kbps MP3 formatında ayıklamak için `yt-dlp` ve `ffmpeg` kullanır.
- **Akıllı Kurulum:** Uygulama ilk açıldığında ihtiyaç duyduğu tüm yan araçları (`ffmpeg`, `yt-dlp`, `deno`) şık bir ilerleme çubuğuyla (GUI) AppData klasörünüze kendi kurar.
- **Çoklu Dil Desteği:** Windows sistem dilinizi algılayarak otomatik olarak İngilizce veya Türkçe çalışır.
- **Rahatsız Etmez:** Tamamen arka planda (Sistem Tepsisi - System Tray) gizlenerek çalışır ve size sadece şık Windows bildirimleriyle haber verir.

### 🚀 Kurulum
1. [Releases sayfasına](https://github.com/kirgizmustafa17/Youtube-Clipboard-MP3-Downloader/releases) gidin.
2. **`YTAudioCatcher_Setup.exe`** kurulum dosyasını veya Taşınabilir (Portable) ZIP dosyasını indirin.
3. Kurun ve çalıştırın! Uygulama ilk açılışta gerekli olan yan araçları otomatik olarak indirip kuracaktır.

### 🎧 Kullanım
1. Uygulamanın çalıştığından emin olun (Sağ alt köşedeki simgeler arasında 🎵 ikonunu görebilirsiniz).
2. Herhangi bir YouTube linkini kopyalayın.
3. Ekrana bildirim gelecektir: "İndirme Başladı".
4. İşlem bittiğinde müziğiniz `C:\Kullanıcılar\Adınız\Müzik\Youtube` klasöründe hazır olacaktır.
