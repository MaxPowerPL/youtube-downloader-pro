<div align="center">

  <img src="assets/images/logo.ico" alt="YouTube Downloader Pro Logo" width="200" height="auto" />

  # YouTube Downloader Pro

  **Profesjonalna aplikacja desktop do pobierania filmów, playlist i audio z YouTube**
  <br>
  *Prosta, szybka i intuicyjna - pobieraj bez ograniczeń*

  <p>
    <a href="https://github.com/MaxPowerPL/youtube-downloader-pro/releases/tag/v1.4.1">
      <img src="https://img.shields.io/github/v/tag/MaxPowerPL/youtube-downloader-pro?label=VERSION&style=for-the-badge&color=238636" alt="Wersja" />
    </a>
    <a href="#">
      <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status" />
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

Projekt umożliwia nie tylko pobieranie pojedynczych filmów w jakości 4K/1080p, ale teraz obsługuje również **całe playlisty**, posiada **historię pobrań**, **tryb ciemny** oraz system powiadomień. Aplikacja dba o automatyczne łączenie obrazu z dźwiękiem oraz konwersję formatów przy użyciu silników **yt-dlp** oraz **FFmpeg**.

### 🎯 Aktualna Wersja: `v1.4.1 (Stable)`
Najnowsza wersja wprowadza **całkowitą przebudowę kodu (Refactoring)**. Aplikacja została podzielona na logiczne moduły (MVC), co ułatwia jej rozwój, testowanie i czytelność kodu, zachowując jednocześnie wszystkie dotychczasowe funkcjonalności.

---

## ✨ Funkcjonalności

Co oferuje aplikacja?

### 📥 Pobieranie
- **Obsługa Playlist**: Wykrywa linki do playlist, wyświetla listę utworów i pobiera całość do dedykowanego podfolderu.
- **3 Tryby**:
  - **Wideo + Dźwięk**: Najlepsza jakość (merge do MP4/AAC).
  - **Tylko Wideo**: Czysty strumień obrazu.
  - **Tylko Audio**: Konwersja do MP3 (192 kbps).
- **Inteligentna tabela**: Wyświetla kodeki (AV1/VP9/H264), rozmiar i FPS.

### ⚙️ Zarządzanie i UI
- **Historia Pobrań**:
  - Pełna lista pobranych plików z datą i ścieżką.
  - **Weryfikacja**: Oznacza kolorem pliki, które zostały usunięte z dysku.
  - **Zarządzanie**: Możliwość usuwania wpisów lub czyszczenia całej historii.
- **Personalizacja**:
  - **Tryb Ciemny / Jasny**: Przełącznik motywu aplikacji.
  - **Domyślna Jakość**: Ustawienie preferowanej rozdzielczości (np. max 1080p) dla playlist.
- **Powiadomienia**: Systemowe dymki powiadomień (Windows Toast) po zakończeniu pobierania.

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
```text
yt-dlp
imageio-ffmpeg
plyer
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

W wersji v1.4.1 kod został zrefaktoryzowany i podzielony na moduły odpowiedzialne za konkretne zadania.

```text
📦 youtube-downloader-pro
┣ 📂 assets/
┃ ┗ 📂 images/
┃   ┗ 📜 logo.ico          # Ikona aplikacji i powiadomień
┣ 📜 main.py               # [Controller] Główny punkt wejścia i logika biznesowa
┣ 📜 ui.py                 # [View] Główne okno aplikacji, widgety i style
┣ 📜 windows.py            # [View] Okna dodatkowe (Ustawienia, Historia)
┣ 📜 data_manager.py       # [Model] Zarządzanie plikami JSON (config, history)
┣ 📜 utils.py              # [Utils] Funkcje pomocnicze (centrowanie, ikony)
┣ 📜 config.json           # [Auto] Zapisuje motyw i domyślną jakość
┣ 📜 history.json          # [Auto] Baza danych historii pobrań
┣ 📜 requirements.txt      # Lista zależności
┣ 📜 LICENSE               # Licencja MIT
┗ 📜 README.md
```

### Opis modułów:

| Plik | Rola i Odpowiedzialność |
|------|-------------------------|
| `main.py` | **Entry Point**. Inicjalizuje aplikację, zarządza wątkami pobierania (`yt-dlp`), logiką `ffmpeg` oraz łączy UI z danymi. |
| `ui.py` | **Interfejs**. Zawiera klasę `MainUI`, która buduje główne okno, tabelę wyników, paski postępu oraz obsługuje motywy graficzne. |
| `windows.py` | **Okna Dialogowe**. Zawiera funkcje tworzące okno "Ustawienia" oraz zaawansowane okno "Historia" z tabelą. |
| `data_manager.py` | **Dane**. Odpowiada za odczyt i zapis plików `config.json` oraz `history.json`. |
| `utils.py` | **Narzędzia**. Helpery do centrowania okien na ekranie, czyszczenia kodów ANSI z tekstu oraz obsługi AppID w Windows. |

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

### Faza 2: Enhancements (Ukończone ✅)
- [x] Pobieranie playlist / kanałów YouTube
- [x] Historia pobranych plików (z zarządzaniem i weryfikacją)
- [x] Ustawienia jakości domyślnej
- [x] Ciemny motyw UI
- [x] Powiadomienia systemowe po zakończeniu

### Faza 3: Pro Features (Planowane)
- [ ] Proxy/VPN support
- [ ] Skróty klawiaturowe
- [ ] Multi-threading (równoległe pobieranie)
- [ ] Wbudowany odtwarzacz podglądu

---

## 🐛 Znane Problemy i Rozwiązania

### ✅ Naprawione w v1.4.1:
- **Modularność**: Rozwiązano problem "God Object" w `main.py`, dzieląc kod na mniejsze pliki.
- **Zależności cykliczne**: Naprawiono błędy importów i rekurencji w logice UI.

### 🔧 Do poprawy:
- [ ] Obsługa bardzo długich tytułów filmów (truncate w UI)
- [ ] Retry mechanizm przy błędach sieci

---

## 📝 Changelog

### v1.4.1 (Modular Refactoring)
- **Refactor**: Gruntowna przebudowa struktury projektu. Kod podzielono z jednego pliku `main.py` na 5 wyspecjalizowanych modułów (`ui`, `windows`, `data_manager`, `utils`).
- **Fix**: Naprawiono błędy rekurencji przy odświeżaniu widoku.
- **Dev**: Zastosowano wzorzec zbliżony do MVC dla łatwiejszego utrzymania kodu.

### v1.4.0 (Icon & UI Fix)
- **Fix:** Poprawiono wyświetlanie ikon aplikacji (.ico) na pasku zadań i w oknach.
- **UI:** Dodano automatyczne centrowanie wszystkich okien na ekranie.
- **UI:** Poprawiono kolejność okien (Z-order) przy komunikatach potwierdzeń.

### v1.3 (History Fix)
- **Feature:** Weryfikacja istnienia plików w Historii (zielony = dostępny, czerwony = usunięty).
- **Feature:** Możliwość usuwania zaznaczonych wpisów z historii.
- **Fix:** Poprawiono zapisywanie ścieżek plików w historii.

### v1.2 (Playlist Support)
- **Feature:** Pełna obsługa playlist YouTube.
- **Feature:** Automatyczne tworzenie podfolderów dla playlist.
- **Feature:** Statusy pobierania dla poszczególnych plików w tabeli playlisty.

### v1.1 (Settings & Theme)
- **Feature:** Dodano Tryb Ciemny.
- **Feature:** Dodano okno Ustawień (wybór domyślnej jakości).
- **Feature:** Integracja powiadomień systemowych (plyer).

### v1.0.0 (Initial Release)
- Podstawowa funkcjonalność pobierania pojedynczych wideo.

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