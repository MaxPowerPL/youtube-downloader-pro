<div align="center">

  <img src="assets/images/logo.png" alt="YouTube Downloader Pro Logo" width="200" height="auto" />

  # YouTube Downloader Pro

  **Profesjonalna aplikacja desktop do pobierania filmów i audio z YouTube**
  <br>
  *Prosta, szybka i intuicyjna - pobieraj bez ograniczeń*

  <p>
    <a href="https://github.com/MaxPowerPL/youtube-downloader-pro/releases/tag/v1.0.0">
      <img src="https://img.shields.io/github/v/tag/MaxPowerPL/youtube-downloader-pro?label=VERSION&style=for-the-badge&color=238636" alt="Wersja" />
    </a>
    <a href="#">
      <img src="https://img.shields.io/badge/Status-Stable-important?style=for-the-badge" alt="Status" />
    </a>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    </a>
    <a href="https://github.com/yt-dlp/yt-dlp">
      <img src="https://img.shields.io/badge/Engine-yt--dlp-FF5722?style=for-the-badge&logo=youtube&logoColor=white" alt="yt-dlp" />
    </a>
    <a href="https://github.com/MaxPowerPL/youtube-downloader-pro/stargazers">
      <img src="https://img.shields.io/github/stars/MaxPowerPL/youtube-downloader-pro?style=for-the-badge&color=yellow" alt="Stars" />
    </a>
    <a href="https://github.com/MaxPowerPL/youtube-downloader-pro">
      <img src="https://img.shields.io/github/last-commit/MaxPowerPL/youtube-downloader-pro?style=for-the-badge" alt="Last Commit" />
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
    </a>
  </p>

  <p>
    <a href="#-o-projekcie">📖 O Projekcie</a> •
    <a href="#-funkcjonalności">✨ Funkcjonalności</a> •
    <a href="#-instalacja-i-uruchomienie">🚀 Instalacja</a> •
    <a href="#-struktura-projektu">📂 Struktura</a> •
    <a href="#%EF%B8%8F-roadmapa">🗺️ Roadmapa</a>
  </p>
</div>

---

## 📖 O Projekcie

**YouTube Downloader Pro** to zaawansowana aplikacja desktop z graficznym interfejsem, stworzona w Pythonie z wykorzystaniem Tkinter. Umożliwia szybkie i wygodne pobieranie filmów oraz audio z YouTube w różnych jakościach i formatach, bez konieczności korzystania z wiersza poleceń.

Projekt powstał z potrzeby stworzenia prostego, ale funkcjonalnego narzędzia dla użytkowników, którzy chcą mieć pełną kontrolę nad pobieranymi materiałami - od wyboru jakości wideo (nawet 1080p+), przez samodzielne pobieranie strumieni video bez dźwięku, aż po konwersję audio do MP3. Wszystko w przejrzystym, nowoczesnym interfejsie.

Aplikacja opiera się na potężnym silniku **yt-dlp** oraz **FFmpeg** do przetwarzania multimediów, zapewniając stabilność i kompatybilność z setkami serwisów streamingowych. Dzięki użyciu biblioteki `imageio-ffmpeg`, FFmpeg jest automatycznie dostępny - nie wymaga osobnej instalacji.

### 🎯 Aktualna Wersja: `v1.0.0 (Stable)`
Pierwsza stabilna wersja zawiera kompletny zestaw funkcji pobierania wideo i audio, czysty interfejs użytkownika z Treeview do wyboru jakości, oraz zaawansowany system logów i monitorowania postępu z obsługą ANSI escape codes.

---

## ✨ Funkcjonalności

Co już działa w tej wersji?

- [x] **Pobieranie wideo i audio**:
  - **Wideo + Dźwięk**: Automatyczne łączenie najlepszego strumienia wideo z audio, merge do MP4 z AAC.
  - **Tylko Wideo**: Pobieranie czystego strumienia wideo bez dźwięku (dla edytorów/montażystów).
  - **Tylko Audio**: Ekstrakcja audio i konwersja do MP3 (192 kbps).
- [x] **Inteligentna analiza formatów**:
  - Automatyczne wykrywanie dostępnych jakości (360p, 720p, 1080p, itp.).
  - Wyświetlanie kodeków, rozmiaru pliku, FPS w czytelnej tabeli.
  - Deduplikacja - eliminacja powtarzających się formatów.
- [x] **Interfejs użytkownika**:
  - Nowoczesny UI z motywem "clam" i spójnymi stylami.
  - Pasek postępu z live danymi: procenty, prędkość, ETA (oczyszczony z kodów ANSI).
  - Dziennik zdarzeń z timestampami.
- [x] **FFmpeg automatyczny**:
  - Integracja `imageio-ffmpeg` - brak konieczności ręcznej instalacji.
  - Obsługa merge, konwersji audio, i przetwarzania wideo.

---

## 🛠️ Technologie

Projekt został zbudowany przy użyciu:

| Technologia | Opis |
| :--- | :--- |
| **Python 3.8+** | Główny język programowania, zapewnia przenośność i prostotę. |
| **Tkinter + ttk** | Natywna biblioteka GUI - lekki, szybki interfejs bez zewnętrznych zależności. |
| **yt-dlp** | Silnik pobierania wideo z YouTube i 1000+ innych serwisów, fork youtube-dl. |
| **imageio-ffmpeg** | Automatyczne dostarczanie binarek FFmpeg, eliminuje ręczną konfigurację. |
| **Threading** | Obsługa asynchronicznego pobierania bez blokowania UI. |

---

## 🚀 Instalacja i Uruchomienie

Aby uruchomić projekt na swoim komputerze, wykonaj następujące kroki:

### 1. Wymagania
- Python 3.8 lub nowszy
- System operacyjny: Windows, macOS lub Linux
- Połączenie z internetem (do pobierania filmów)

### 2. Klonowanie repozytorium
```bash
git clone https://github.com/MaxPowerPL/youtube-downloader-pro.git
cd youtube-downloader-pro
```

### 3. Konfiguracja środowiska

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalacja zależności
```bash
pip install -r requirements.txt
```

**Zawartość `requirements.txt`:**
```
yt-dlp
imageio-ffmpeg
```

### 5. Uruchomienie
```bash
python main.py
```

### 6. Obsługa aplikacji
- **Pole "Adres filmu"**: Wklej link YouTube.
- **Przycisk "Szukaj formatów"**: Analizuje dostępne jakości.
- **Radio buttons**: Wybierz tryb (Wideo+Dźwięk / Tylko Wideo / Tylko Audio).
- **Tabela jakości**: Kliknij na wybraną jakość/format.
- **Przycisk "ROZPOCZNIJ POBIERANIE"**: Startuje download.
- **Zmień folder**: Wybierz katalog zapisu (domyślnie Downloads).

---

## 📂 Struktura Projektu

Projekt ma prostą, jednoplikową architekturę - cały kod UI, logika pobierania i integracja yt-dlp/FFmpeg znajdują się w `main.py`. Taka struktura ułatwia deployment i modyfikacje.

```text
📦 youtube-downloader-pro
┣ 📂 assets/
┃ ┗ 📂 images/
┃   ┗ 📜 logo.png          # Logo projektu
┣ 📜 main.py               # Główny plik aplikacji (klasa YouTubeDownloaderPro)
┣ 📜 requirements.txt      # Lista zależności Pythona
┣ 📜 LICENSE               # Licencja MIT
┗ 📜 README.md
```

### Opis głównych modułów:

#### `main.py`
| Komponent | Opis |
|------|------|
| `YouTubeDownloaderPro` | Główna klasa aplikacji, inicjalizuje UI i FFmpeg. |
| `_setup_styles()` | Konfiguruje motywy ttk (clam), kolory, fonty dla spójnego UI. |
| `_build_ui()` | Tworzy interfejs graficzny (frames, buttons, Treeview, log widget). |
| `start_analysis()` | Wątek pobierania informacji o filmie z yt-dlp (asynchrouniczne). |
| `_process_info()` | Parsuje formaty, deduplikuje, wypełnia Treeview odpowiednimi danymi. |
| `start_download()` | Wątek pobierania pliku z obsługą progress hooks i ANSI cleaning. |
| `MyLogger` | Custom logger yt-dlp przekierowujący output do UI log widget. |
| `_clean_ansi()` | Usuwa ANSI escape codes z tekstu (fix dla ETA/prędkości). |

---

## ⚙️ Zaawansowane Opcje

### Tryby pobierania:
- **Wideo + Dźwięk**: Format `{format_id}+bestaudio/best`, merge do MP4, audio AAC. Rekomendowane dla standardowego użytku.
- **Tylko Wideo (bez dźwięku)**: Format `{format_id}`. Idealne dla edytorów chcących dodać własne audio lub oszczędzić miejsce.
- **Tylko Audio**: Format `bestaudio/best`, konwersja do MP3 192kbps via FFmpegExtractAudio.

### Progress Monitoring:
1. **Procenty** - Ekstrakcja z `_percent_str` oczyszczona z ANSI.
2. **Prędkość** - `_speed_str` wyświetlana w MB/s lub KB/s.
3. **ETA** - `_eta_str` pokazuje szacowany czas pozostały.

---

## 🗺️ Roadmapa

Plany rozwoju projektu:

### Faza 1: Core Features (Ukończone ✅)
- [x] Interfejs graficzny Tkinter
- [x] Integracja yt-dlp + FFmpeg
- [x] 3 tryby pobierania (Video+Audio, Video-only, Audio)
- [x] Progress bar z live stats
- [x] Deduplikacja formatów

### Faza 2: Enhancements (Planowane)
- [ ] Pobieranie playlist / kanałów YouTube
- [ ] Historia pobranych plików
- [ ] Ustawienia jakości domyślnej
- [ ] Ciemny motyw UI
- [ ] Powiadomienia systemowe po zakończeniu

### Faza 3: Pro Features (W przyszłości)
- [ ] Proxy/VPN support
- [ ] Skróty klawiaturowe
- [ ] Multi-threading (równoległe pobieranie)
- [ ] Wbudowany odtwarzacz podglądu

---

## 🐛 Znane Problemy i Rozwiązania

### ✅ Naprawione w v1.0.0:
- **ANSI escape codes w ETA**: Dodano `_clean_ansi()` do usuwania kolorów z postępu.
- **Blokowanie UI podczas pobierania**: Użycie `threading.Thread` dla operacji IO.
- **Brak FFmpeg**: `imageio-ffmpeg` dostarcza binarkę automatycznie.

### 🔧 Do poprawy:
- [ ] Obsługa bardzo długich tytułów filmów (truncate w UI)
- [ ] Retry mechanizm przy błędach sieci

---

## 📝 Changelog

### v1.0.0 (Initial Release)
**NEW FEATURES:**
- Pełna funkcjonalność pobierania wideo i audio z YouTube
- Trzy tryby: Wideo+Dźwięk, Tylko Wideo, Tylko Audio
- Treeview z automatycznym wykrywaniem formatów (jakość, kodek, rozmiar, FPS)
- Progress bar z czasem rzeczywistym (procenty, prędkość, ETA)
- Dziennik zdarzeń z timestampami

**Zmiany techniczne:**
- Integracja `yt-dlp` jako backend downloadera
- `imageio-ffmpeg` dla automatycznej dostępności FFmpeg
- Custom `MyLogger` przekierowujący output yt-dlp do GUI
- ANSI escape codes cleanup dla czytelności postępu
- Threading dla non-blocking downloads

---

## 📜 Licencja

Ten projekt jest udostępniony na licencji **MIT**.

### Co MOŻESZ robić:
- ✅ Używać komercyjnie
- ✅ Modyfikować kod źródłowy
- ✅ Dystrybuować kopie
- ✅ Używać prywatnie

### Czego NIE MOŻESZ robić:
- ❌ Usuwać informacji o prawach autorskich
- ❌ Obciążać autora odpowiedzialnością za szkody
- ❌ Używać nazwy autora do promocji bez zgody

### Użytek komercyjny
Projekt można swobodnie używać w celach komercyjnych z zachowaniem informacji o licencji MIT.

Zobacz pełne warunki prawne w pliku [LICENSE](LICENSE).

---

<div align="center">

### ⭐ Jeśli podoba Ci się ten projekt, zostaw gwiazdkę na GitHubie! ⭐

☕ Stworzono używając Python, Tkinter, yt-dlp i FFmpeg.
<br>
<sub>Projekt powstał dla celów edukacyjnych i niekomercyjnych. Użytkownik ponosi pełną odpowiedzialność za zgodność z prawem autorskim.</sub>
<br>
<sub>**MIT License** - Wolne oprogramowanie open-source. Zobacz [LICENSE](LICENSE) po szczegóły.</sub>

<p>
  <a href="https://github.com/MaxPowerPL/youtube-downloader-pro/issues/new?template=bug_report.yml">🐛 Zgłoś Bug</a> •
  <a href="https://github.com/MaxPowerPL/youtube-downloader-pro/issues/new?template=feature_request.yml">💡 Zaproponuj Funkcję</a> •
  <a href="https://github.com/MaxPowerPL/youtube-downloader-pro/wiki">📖 Wiki</a>
</p>

![Status](https://img.shields.io/badge/Status-Stable-brightgreen?style=for-the-badge&logo=statuspage&logoColor=white)

</div>