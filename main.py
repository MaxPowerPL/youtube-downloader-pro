import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import yt_dlp
import os
import datetime
import imageio_ffmpeg
import re

class YouTubeDownloaderPro:
    def __init__(self, root):
        self.root = root
        self.root.title("YT Downloader Pro v1.0.0")
        self.root.geometry("700x780")

        # --- Zmienne ---
        self.download_path = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self.url_var = tk.StringVar()
        self.download_mode = tk.StringVar(value="video") # video | video_only | audio
        self.formats_data = {}

        # FFmpeg
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

        self._setup_styles()
        self._build_ui()

        self.log(f"System gotowy. FFmpeg: {self.ffmpeg_exe}")

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        bg_color = "#f0f0f0"
        self.root.configure(bg=bg_color)
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, font=("Segoe UI", 9))
        style.configure("TLabelframe", background=bg_color, font=("Segoe UI", 9, "bold"))
        style.configure("TLabelframe.Label", background=bg_color)
        style.configure("TButton", font=("Segoe UI", 9))
        style.configure("Big.TButton", font=("Segoe UI", 11, "bold"))

        style.configure("Treeview", font=("Segoe UI", 9), rowheight=25)
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

        style.configure("Green.Horizontal.TProgressbar", troughcolor='#d9d9d9', background='#4caf50')

    def _build_ui(self):
        main_pad = 10

        # --- 1. Sekcja Folderu ---
        folder_frame = ttk.LabelFrame(self.root, text="Folder zapisu", padding=10)
        folder_frame.pack(fill="x", padx=main_pad, pady=(main_pad, 5))

        ttk.Entry(folder_frame, textvariable=self.download_path, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(folder_frame, text="Zmień folder...", command=self.choose_directory).pack(side="right")

        # --- 2. Sekcja Adresu ---
        url_frame = ttk.LabelFrame(self.root, text="Adres filmu", padding=10)
        url_frame.pack(fill="x", padx=main_pad, pady=5)

        ttk.Entry(url_frame, textvariable=self.url_var).pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.btn_analyze = ttk.Button(url_frame, text="Szukaj formatów", command=self.start_analysis)
        self.btn_analyze.pack(side="right")

        # --- 3. Wybór Trybu ---
        mode_frame = ttk.Frame(self.root, padding=(main_pad, 5))
        mode_frame.pack(fill="x", anchor="w")

        ttk.Label(mode_frame, text="Wybierz tryb:").pack(side="left", padx=(0, 10))

        # Opcja 1: Wideo + Dźwięk
        ttk.Radiobutton(mode_frame, text="Wideo + Dźwięk", variable=self.download_mode, value="video", command=self.on_mode_change).pack(side="left", padx=10)
        # Opcja 2: Tylko Wideo
        ttk.Radiobutton(mode_frame, text="Tylko Wideo (bez dźwięku)", variable=self.download_mode, value="video_only", command=self.on_mode_change).pack(side="left", padx=10)
        # Opcja 3: Tylko Audio
        ttk.Radiobutton(mode_frame, text="Tylko Dźwięk", variable=self.download_mode, value="audio", command=self.on_mode_change).pack(side="left", padx=10)

        # --- 4. Tabela Jakości ---
        table_frame = ttk.LabelFrame(self.root, text="Dostępne jakości", padding=10)
        table_frame.pack(fill="both", expand=True, padx=main_pad, pady=5)

        columns = ("quality", "codec", "format", "size", "fps")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse", height=8)

        self.tree.heading("quality", text="Jakość")
        self.tree.heading("codec", text="Kodek")
        self.tree.heading("format", text="Format")
        self.tree.heading("size", text="Rozmiar (ok.)")
        self.tree.heading("fps", text="FPS")

        self.tree.column("quality", width=80, anchor="center")
        self.tree.column("codec", width=80, anchor="center")
        self.tree.column("format", width=60, anchor="center")
        self.tree.column("size", width=100, anchor="e")
        self.tree.column("fps", width=60, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- 5. Przycisk Pobierania ---
        self.btn_download = ttk.Button(self.root, text="ROZPOCZNIJ POBIERANIE", style="Big.TButton", state="disabled", command=self.start_download)
        self.btn_download.pack(fill="x", padx=main_pad, pady=15, ipady=5)

        # --- 6. Status i Dziennik ---
        log_frame = ttk.LabelFrame(self.root, text="Status i Dziennik", padding=10)
        log_frame.pack(fill="both", expand=True, padx=main_pad, pady=(0, main_pad))

        self.status_label = ttk.Label(log_frame, text="Gotowy", font=("Segoe UI", 9, "bold"), foreground="#333")
        self.status_label.pack(anchor="w", pady=(0, 2))

        self.progress_bar = ttk.Progressbar(log_frame, orient="horizontal", mode="determinate", style="Green.Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", pady=(0, 10))

        self.log_widget = scrolledtext.ScrolledText(log_frame, height=8, state='disabled', font=("Consolas", 9))
        self.log_widget.pack(fill="both", expand=True)

    # --- Funkcje UI ---
    def log(self, message):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        full_msg = f"{timestamp} {message}\n"
        self.log_widget.config(state='normal')
        self.log_widget.insert(tk.END, full_msg)
        self.log_widget.see(tk.END)
        self.log_widget.config(state='disabled')

    def choose_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.download_path.set(path)
            self.log(f"Folder: {path}")

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.formats_data = {}
        self.btn_download.config(state="disabled")

    def on_mode_change(self):
        self.clear_table()
        if self.url_var.get().strip():
            self.start_analysis()
        else:
            self.log(f"Zmieniono tryb na: {self.download_mode.get()}.")

    # --- Analiza ---
    def start_analysis(self):
        url = self.url_var.get().strip()
        if not url: return

        self.clear_table()
        self.btn_analyze.config(state="disabled")
        self.log(f"Analiza łącza...")
        threading.Thread(target=self._fetch_info, args=(url,), daemon=True).start()

    def _fetch_info(self, url):
        opts = {'quiet': True, 'no_warnings': True}
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
            self.root.after(0, lambda: self._process_info(info))
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Błąd analizy: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.btn_analyze.config(state="normal"))

    def _process_info(self, info):
        self.log(f"Znaleziono: {info.get('title', 'Video')}")
        formats = info.get('formats', [])
        seen_keys = set()

        current_mode = self.download_mode.get()

        if current_mode == "audio":
            item_id = self.tree.insert("", "end", values=("Audio HQ", "AAC/MP3", "mp3", "Auto", "-"))
            self.formats_data[item_id] = {'type': 'audio'}
        else:
            # Obsługa trybu 'video' oraz 'video_only' - lista formatów jest ta sama
            formats.sort(key=lambda x: (x.get('height') or 0, x.get('tbr') or 0), reverse=True)
            count = 0
            for f in formats:
                if f.get('vcodec') == 'none' or not f.get('height'): continue

                simple_codec = f.get('vcodec', '').split('.')[0]
                ext = f.get('ext')
                fps = f.get('fps', 0)

                fs = f.get('filesize') or f.get('filesize_approx')
                size_str = f"{fs / 1024 / 1024:.1f} MB" if fs else "?"

                unique_key = (f.get('height'), ext, simple_codec)
                if unique_key in seen_keys: continue
                seen_keys.add(unique_key)

                vals = (f"{f.get('height')}p", simple_codec, ext, size_str, f"{fps} fps")
                item_id = self.tree.insert("", "end", values=vals)

                self.formats_data[item_id] = {
                    'format_id': f.get('format_id'),
                    'type': 'video', # Typ video oznacza tu dostępny strumień wideo
                    'ext': ext
                }
                count += 1

        if self.tree.get_children():
            self.btn_download.config(state="normal")
            self.tree.selection_set(self.tree.get_children()[0])

    # --- Pobieranie ---
    def start_download(self):
        sel = self.tree.selection()
        if not sel: return

        data = self.formats_data.get(sel[0])
        url, path = self.url_var.get(), self.download_path.get()
        mode = self.download_mode.get()

        self.btn_download.config(state="disabled")
        self.btn_analyze.config(state="disabled")
        self.progress_bar['value'] = 0
        self.status_label.config(text="Inicjalizacja...")
        self.log(f"Rozpoczynam pobieranie (Tryb: {mode})...")

        threading.Thread(target=self._download_thread, args=(url, path, data, mode), daemon=True).start()

    def _clean_ansi(self, text):
        """Usuwa kody kolorów z tekstu"""
        if not text: return ""
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        return ansi_escape.sub('', str(text)).strip()

    def _download_thread(self, url, path, data, mode):
        # 1. Custom Logger
        class MyLogger:
            def __init__(self, app): self.app = app
            def debug(self, msg):
                if '[download]' in msg or 'ETA' in msg or '%' in msg: return
                if not msg.startswith('[debug] '): self.app.root.after(0, lambda: self.app.log(msg))
            def info(self, msg):
                if '[download]' in msg: return
                self.app.root.after(0, lambda: self.app.log(msg))
            def warning(self, msg): pass
            def error(self, msg): self.app.root.after(0, lambda: self.app.log(f"BŁĄD: {msg}"))

        # 2. Hook postępu (Naprawione ETA)
        def progress_hook(d):
            if d['status'] == 'downloading':
                try:
                    # Czyścimy wszystkie pola z kodów kolorów
                    p_str = self._clean_ansi(d.get('_percent_str', '0%')).replace('%','')
                    speed = self._clean_ansi(d.get('_speed_str', 'N/A'))
                    eta = self._clean_ansi(d.get('_eta_str', 'N/A'))

                    val = float(p_str)

                    self.root.after(0, lambda: self.progress_bar.configure(value=val))
                    self.root.after(0, lambda: self.status_label.configure(
                        text=f"Pobieranie: {val:.1f}% | Pozostało: {eta} | Prędkość: {speed}"
                    ))
                except: pass
            elif d['status'] == 'finished':
                msg = "Pobieranie zakończone."
                if mode == "video": msg += " Przetwarzanie (łączenie)..."
                self.root.after(0, lambda: self.status_label.configure(text=msg))

        # 3. Konfiguracja
        ydl_opts = {
            'logger': MyLogger(self),
            'progress_hooks': [progress_hook],
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'ffmpeg_location': self.ffmpeg_exe,
            'nocolor': True, # Wymuszenie braku kolorów (dla pewności)
        }

        # Konfiguracja zależna od trybu
        if mode == 'audio':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
            })

        elif mode == 'video_only':
            # Tylko wideo - bez łączenia z audio
            f_id = data['format_id']
            ydl_opts.update({
                'format': f_id,
                # Opcjonalnie: można wymusić mp4 jeśli strumień jest inny, ale "video_only"
                # zazwyczaj implikuje pobranie tego co jest. Dla wygody można dodać konwersję:
                # 'merge_output_format': 'mp4'
            })

        else: # mode == 'video' (Video + Audio)
            f_id = data['format_id']
            ydl_opts.update({
                'format': f'{f_id}+bestaudio/best',
                'merge_output_format': 'mp4',
                # Konwersja audio do AAC dla kompatybilności
                'postprocessor_args': {'merger': ['-c:a', 'aac']}
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.root.after(0, lambda: self.log("SUKCES: Plik zapisany."))
            self.root.after(0, lambda: self.status_label.configure(text="Gotowe!"))
        except Exception as e:
            self.root.after(0, lambda: self.log(f"BŁĄD: {str(e)}"))
            self.root.after(0, lambda: self.status_label.configure(text="Wystąpił błąd."))
        finally:
            self.root.after(0, lambda: self.btn_download.config(state="normal"))
            self.root.after(0, lambda: self.btn_analyze.config(state="normal"))

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderPro(root)
    root.mainloop()