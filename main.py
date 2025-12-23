import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox, Toplevel
import threading
import yt_dlp
import os
import datetime
import imageio_ffmpeg
import re
import ctypes
import json
from plyer import notification

# Pliki konfiguracyjne
CONFIG_FILE = "config.json"
HISTORY_FILE = "history.json"

class YouTubeDownloaderPro:
    def __init__(self, root):
        self.root = root
        self.root.title("YT Downloader Pro v1.4")

        # Ustawiamy rozmiar i centrujemy
        self._center_window(self.root, 850, 850)

        # --- DANE ---
        self.download_path = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self.url_var = tk.StringVar()
        self.download_mode = tk.StringVar(value="video")
        self.formats_data = {}
        self.is_playlist = False
        self.playlist_entries = []
        self.playlist_id_map = {}

        # --- KONFIGURACJA I HISTORIA ---
        self.settings = self._load_settings()
        self.history = self._load_history()
        self.is_dark_mode = self.settings.get("dark_mode", False)

        # FFmpeg
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

        # --- IKONA ---
        self.icon_path_ico = None
        self._load_icon()

        # --- UI START ---
        self._setup_styles()
        self._build_ui()

        # Aplikowanie motywu przy starcie
        if self.is_dark_mode:
            self._apply_dark_theme()

        self.log(f"System gotowy. FFmpeg załadowany.")
        self.log(f"Załadowano ustawienia. Domyślna jakość: {self.settings.get('default_quality', '1080p')}")

    # ---------------------------------------------------------
    # --- METODY POMOCNICZE (Centrowanie, Ikony) ---
    # ---------------------------------------------------------
    def _center_window(self, window, width, height):
        """Centruje podane okno na ekranie"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        window.geometry(f"{width}x{height}+{x}+{y}")

    def _load_icon(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Plik .ico
            icon_path = os.path.join(script_dir, "assets", "images", "logo.ico")

            if os.path.exists(icon_path):
                # 1. Ustawienie ikony okna i paska zadań (Windows wymaga iconbitmap dla .ico)
                self.root.iconbitmap(icon_path)

                # 2. Zapisanie ścieżki absolutnej dla powiadomień
                self.icon_path_ico = icon_path
            else:
                print(f"Brak pliku ikony: {icon_path}")

        except Exception as e:
            print(f"Błąd ładowania ikony: {e}")

    # ---------------------------------------------------------
    # --- SEKCJA DANYCH I PLIKÓW ---
    # ---------------------------------------------------------
    def _load_settings(self):
        default = {"default_quality": "1080p", "dark_mode": False}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return {**default, **json.load(f)}
            except: pass
        return default

    def _save_settings(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.settings, f)

    def _load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: pass
        return []

    def _save_to_history(self, title, url, path):
        entry = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "title": title,
            "url": url,
            "path": path
        }
        self.history.insert(0, entry)
        self._rewrite_history_file()

    def _rewrite_history_file(self):
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            self.log(f"Błąd zapisu historii: {e}")

    # ---------------------------------------------------------
    # --- UI & STYLE ---
    # ---------------------------------------------------------
    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.colors = {
            "bg": "#f0f0f0", "fg": "black",
            "frame_bg": "#f0f0f0", "input_bg": "white",
            "tree_bg": "white", "tree_fg": "black",
            "log_bg": "white", "log_fg": "black"
        }
        self._configure_colors()

    def _configure_colors(self):
        c = self.colors
        self.root.configure(bg=c["bg"])

        self.style.configure("TFrame", background=c["frame_bg"])
        self.style.configure("TLabel", background=c["frame_bg"], foreground=c["fg"], font=("Segoe UI", 9))
        self.style.configure("TLabelframe", background=c["frame_bg"], foreground=c["fg"], font=("Segoe UI", 9, "bold"))
        self.style.configure("TLabelframe.Label", background=c["frame_bg"], foreground=c["fg"])
        self.style.configure("TButton", font=("Segoe UI", 9))
        self.style.configure("Big.TButton", font=("Segoe UI", 11, "bold"))
        self.style.configure("TEntry", fieldbackground=c["input_bg"], foreground=c["fg"])

        self.style.configure("Treeview",
            background=c["tree_bg"], foreground=c["tree_fg"], fieldbackground=c["tree_bg"], font=("Segoe UI", 9), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        self.style.map("Treeview", background=[('selected', '#0078d7')])

        self.style.configure("Green.Horizontal.TProgressbar", troughcolor='#d9d9d9', background='#4caf50')

    def _apply_dark_theme(self):
        self.is_dark_mode = True
        self.settings["dark_mode"] = True
        self._save_settings()

        self.colors = {
            "bg": "#2b2b2b", "fg": "#e0e0e0",
            "frame_bg": "#2b2b2b", "input_bg": "#3c3f41",
            "tree_bg": "#3c3f41", "tree_fg": "#e0e0e0",
            "log_bg": "#1e1e1e", "log_fg": "#00ff00"
        }
        self._configure_colors()
        self.log_widget.config(bg=self.colors["log_bg"], fg=self.colors["log_fg"])
        self.btn_theme.config(text="☀️ Tryb Jasny")

    def _apply_light_theme(self):
        self.is_dark_mode = False
        self.settings["dark_mode"] = False
        self._save_settings()

        self.colors = {
            "bg": "#f0f0f0", "fg": "black",
            "frame_bg": "#f0f0f0", "input_bg": "white",
            "tree_bg": "white", "tree_fg": "black",
            "log_bg": "white", "log_fg": "black"
        }
        self._configure_colors()
        self.log_widget.config(bg=self.colors["log_bg"], fg=self.colors["log_fg"])
        self.btn_theme.config(text="🌙 Tryb Ciemny")

    def toggle_theme(self):
        if self.is_dark_mode: self._apply_light_theme()
        else: self._apply_dark_theme()

    def _build_ui(self):
        main_pad = 10

        # --- TOOLBAR ---
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill="x", padx=main_pad, pady=(5, 0))

        ttk.Button(toolbar, text="⚙️ Ustawienia", command=self.open_settings_window).pack(side="left", padx=(0, 5))
        ttk.Button(toolbar, text="📜 Historia", command=self.open_history_window).pack(side="left", padx=(0, 5))

        self.btn_theme = ttk.Button(toolbar, text="🌙 Tryb Ciemny", command=self.toggle_theme)
        self.btn_theme.pack(side="right")

        # --- 1. Folder ---
        folder_frame = ttk.LabelFrame(self.root, text="Folder zapisu", padding=10)
        folder_frame.pack(fill="x", padx=main_pad, pady=(5, 5))
        ttk.Entry(folder_frame, textvariable=self.download_path, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(folder_frame, text="Zmień...", command=self.choose_directory).pack(side="right")

        # --- 2. Adres ---
        url_frame = ttk.LabelFrame(self.root, text="Adres filmu / Playlisty", padding=10)
        url_frame.pack(fill="x", padx=main_pad, pady=5)
        ttk.Entry(url_frame, textvariable=self.url_var).pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.btn_analyze = ttk.Button(url_frame, text="Szukaj", command=self.start_analysis)
        self.btn_analyze.pack(side="right")

        # --- 3. Tryb ---
        mode_frame = ttk.Frame(self.root, padding=(main_pad, 5))
        mode_frame.pack(fill="x", anchor="w")
        ttk.Label(mode_frame, text="Tryb:").pack(side="left", padx=(0, 10))
        ttk.Radiobutton(mode_frame, text="Wideo+Audio", variable=self.download_mode, value="video", command=self.on_mode_change).pack(side="left", padx=5)
        ttk.Radiobutton(mode_frame, text="Tylko Wideo", variable=self.download_mode, value="video_only", command=self.on_mode_change).pack(side="left", padx=5)
        ttk.Radiobutton(mode_frame, text="Tylko Dźwięk", variable=self.download_mode, value="audio", command=self.on_mode_change).pack(side="left", padx=5)

        # --- 4. Tabela ---
        self.table_frame = ttk.LabelFrame(self.root, text="Zawartość", padding=10)
        self.table_frame.pack(fill="both", expand=True, padx=main_pad, pady=5)

        columns = ("col1", "col2", "col3", "col4", "col5")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", selectmode="browse", height=8)
        self._reset_tree_columns_video()

        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- 5. Pobieranie ---
        self.btn_download = ttk.Button(self.root, text="ROZPOCZNIJ POBIERANIE", style="Big.TButton", state="disabled", command=self.start_download)
        self.btn_download.pack(fill="x", padx=main_pad, pady=10, ipady=5)

        # --- 6. Logi ---
        log_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        log_frame.pack(fill="both", expand=True, padx=main_pad, pady=(0, main_pad))

        self.status_label = ttk.Label(log_frame, text="Gotowy", font=("Segoe UI", 9, "bold"))
        self.status_label.pack(anchor="w", pady=(0, 2))

        self.progress_bar = ttk.Progressbar(log_frame, orient="horizontal", mode="determinate", style="Green.Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", pady=(0, 10))

        self.log_widget = scrolledtext.ScrolledText(log_frame, height=6, state='disabled', font=("Consolas", 9))
        self.log_widget.pack(fill="both", expand=True)

    # ---------------------------------------------------------
    # --- LOGIKA UI / OKNA ---
    # ---------------------------------------------------------
    def open_settings_window(self):
        win = Toplevel(self.root)
        win.title("Ustawienia")
        # Centrowanie okna ustawień
        self._center_window(win, 300, 200)

        if self.is_dark_mode: win.configure(bg=self.colors["bg"])

        ttk.Label(win, text="Domyślna jakość wideo (dla Playlist):").pack(pady=10)
        qualities = ["2160p", "1440p", "1080p", "720p", "480p", "360p"]
        combo = ttk.Combobox(win, values=qualities, state="readonly")
        combo.set(self.settings.get("default_quality", "1080p"))
        combo.pack(pady=5)

        def save():
            self.settings["default_quality"] = combo.get()
            self._save_settings()
            self.log(f"Zapisano domyślną jakość: {combo.get()}")
            win.destroy()

        ttk.Button(win, text="Zapisz", command=save).pack(pady=20)

    def open_history_window(self):
        win = Toplevel(self.root)
        win.title("Zarządzanie Historią")
        # Centrowanie okna historii
        self._center_window(win, 900, 500)

        if self.is_dark_mode: win.configure(bg=self.colors["bg"])

        # Ustawienie okna jako modalnego (opcjonalnie, ale pomaga w zarządzaniu)
        # win.grab_set()

        btn_frame = ttk.Frame(win, padding=10)
        btn_frame.pack(fill="x")

        cols = ("Data", "Tytuł", "Status", "Ścieżka")
        tree = ttk.Treeview(win, columns=cols, show="headings", selectmode="extended")
        tree.heading("Data", text="Data")
        tree.heading("Tytuł", text="Tytuł")
        tree.heading("Status", text="Status Pliku")
        tree.heading("Ścieżka", text="Zapisano w (Plik/Folder)")

        tree.column("Data", width=110, anchor="center")
        tree.column("Tytuł", width=250)
        tree.column("Status", width=100, anchor="center")
        tree.column("Ścieżka", width=350)

        scroll = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        scroll.pack(side="right", fill="y", pady=10, padx=10)

        tree.tag_configure('missing', foreground='red')
        tree.tag_configure('ok', foreground='green')

        def load_data():
            for item in tree.get_children(): tree.delete(item)
            for index, item in enumerate(self.history):
                path = item.get("path", "")
                status = "Dostępny"
                tag = "ok"
                if not os.path.exists(path):
                    status = "Usunięty"
                    tag = "missing"
                tree.insert("", "end", iid=index, values=(item["date"], item["title"], status, path), tags=(tag,))

        def delete_selected():
            selected_items = tree.selection()
            if not selected_items: return

            # FIX Z-ORDER: parent=win sprawia, że popup należy do okna historii, a nie głównego
            if not messagebox.askyesno("Potwierdzenie", f"Usunąć {len(selected_items)} wpisów?", parent=win):
                return

            indices = sorted([int(x) for x in selected_items], reverse=True)
            for idx in indices:
                if 0 <= idx < len(self.history): del self.history[idx]

            self._rewrite_history_file()
            load_data()

        def clear_all():
            if self.history:
                # FIX Z-ORDER
                if messagebox.askyesno("Uwaga", "Wyczyścić całą historię?", parent=win):
                    self.history = []
                    self._rewrite_history_file()
                    load_data()

        ttk.Button(btn_frame, text="🗑️ Usuń zaznaczone", command=delete_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="❌ Wyczyść wszystko", command=clear_all).pack(side="right", padx=5)

        load_data()

    def _reset_tree_columns_video(self):
        self.tree.heading("col1", text="Jakość")
        self.tree.heading("col2", text="Kodek")
        self.tree.heading("col3", text="Format")
        self.tree.heading("col4", text="Rozmiar")
        self.tree.heading("col5", text="FPS")
        self.tree.column("col1", width=80); self.tree.column("col2", width=80)
        self.tree.column("col3", width=60); self.tree.column("col4", width=100); self.tree.column("col5", width=60)

    def _reset_tree_columns_playlist(self):
        self.tree.heading("col1", text="Lp.")
        self.tree.heading("col2", text="Tytuł Wideo")
        self.tree.heading("col3", text="ID")
        self.tree.heading("col4", text="Czas")
        self.tree.heading("col5", text="Status")
        self.tree.column("col1", width=40); self.tree.column("col2", width=350)
        self.tree.column("col3", width=100); self.tree.column("col4", width=80); self.tree.column("col5", width=120)

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        self.log_widget.config(state='normal')
        self.log_widget.insert(tk.END, f"{timestamp} {message}\n")
        self.log_widget.see(tk.END)
        self.log_widget.config(state='disabled')

    def choose_directory(self):
        path = filedialog.askdirectory()
        if path: self.download_path.set(path)

    def on_mode_change(self):
        self.clear_table()
        if self.url_var.get().strip(): self.start_analysis()

    def clear_table(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        self.formats_data = {}
        self.playlist_id_map = {}
        self.btn_download.config(state="disabled")

    def _show_notification(self, title, message):
        try:
            kwargs = {
                'title': title,
                'message': message,
                'app_name': "YT Downloader Pro",
                'timeout': 5,
            }
            if self.icon_path_ico and os.path.exists(self.icon_path_ico):
                kwargs['app_icon'] = self.icon_path_ico

            notification.notify(**kwargs)
        except Exception as e:
            print(f"Notification Error: {e}")

    # ---------------------------------------------------------
    # --- LOGIKA POBIERANIA ---
    # ---------------------------------------------------------
    def start_analysis(self):
        url = self.url_var.get().strip()
        if not url: return
        self.clear_table()
        self.btn_analyze.config(state="disabled")
        self.log(f"Analiza: {url}")
        threading.Thread(target=self._fetch_info, args=(url,), daemon=True).start()

    def _fetch_info(self, url):
        opts = {'quiet': True, 'no_warnings': True, 'extract_flat': 'in_playlist'}
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
            self.root.after(0, lambda: self._process_info(info))
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Błąd: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.btn_analyze.config(state="normal"))

    def _process_info(self, info):
        self.log(f"Tytuł: {info.get('title', 'Unknown')}")
        if 'entries' in info:
            self.is_playlist = True
            self.playlist_entries = list(info['entries'])
            self._reset_tree_columns_playlist()
            self.table_frame.config(text=f"Playlista: {len(self.playlist_entries)} filmów")
            self.playlist_id_map = {}
            for i, entry in enumerate(self.playlist_entries, 1):
                duration = str(datetime.timedelta(seconds=int(entry.get('duration', 0))))
                vid_id = entry.get('id')
                iid = self.tree.insert("", "end", values=(i, entry.get('title'), vid_id, duration, "Oczekuje"))
                if vid_id: self.playlist_id_map[vid_id] = iid
            self.btn_download.config(state="normal", text="POBIERZ CAŁĄ PLAYLISTĘ")
        else:
            self.is_playlist = False
            self.playlist_entries = []
            self.playlist_id_map = {}
            self._reset_tree_columns_video()
            self.table_frame.config(text="Dostępne jakości")
            formats = info.get('formats', [])
            seen_keys = set()
            mode = self.download_mode.get()
            if mode == "audio":
                item_id = self.tree.insert("", "end", values=("Audio HQ", "AAC/MP3", "mp3", "Auto", "-"))
                self.formats_data[item_id] = {'type': 'audio'}
            else:
                formats.sort(key=lambda x: (x.get('height') or 0, x.get('tbr') or 0), reverse=True)
                for f in formats:
                    if f.get('vcodec') == 'none' or not f.get('height'): continue
                    sc = f.get('vcodec', '').split('.')[0]
                    ext = f.get('ext'); fps = f.get('fps', 0)
                    fs = f.get('filesize') or f.get('filesize_approx')
                    sz = f"{fs/1024/1024:.1f} MB" if fs else "?"
                    uk = (f.get('height'), ext, sc)
                    if uk in seen_keys: continue
                    seen_keys.add(uk)
                    vals = (f"{f.get('height')}p", sc, ext, sz, f"{fps}")
                    iid = self.tree.insert("", "end", values=vals)
                    self.formats_data[iid] = {'format_id': f.get('format_id'), 'type': 'video', 'ext': ext}
            if self.tree.get_children():
                self.btn_download.config(state="normal", text="ROZPOCZNIJ POBIERANIE")
                self.tree.selection_set(self.tree.get_children()[0])

    def start_download(self):
        url, path = self.url_var.get(), self.download_path.get()
        mode = self.download_mode.get()
        if self.is_playlist:
            data = {'type': 'playlist'}
            target_info = f"Playlist ({len(self.playlist_entries)} video)"
        else:
            sel = self.tree.selection()
            if not sel: return
            data = self.formats_data.get(sel[0])
            target_info = "Single Video"

        self.btn_download.config(state="disabled")
        self.btn_analyze.config(state="disabled")
        self.progress_bar['value'] = 0
        self.log(f"Start pobierania: {target_info}")
        threading.Thread(target=self._download_thread, args=(url, path, data, mode), daemon=True).start()

    def _clean_ansi(self, text):
        if not text: return ""
        return re.sub(r'\x1b\[[0-9;]*m', '', str(text)).strip()

    def _download_thread(self, url, path, data, mode):
        class MyLogger:
            def __init__(self, app): self.app = app
            def debug(self, msg):
                if not ('[download]' in msg or 'ETA' in msg):
                    if not msg.startswith('[debug] '): self.app.root.after(0, lambda: self.app.log(msg))
            def info(self, msg):
                if not '[download]' in msg: self.app.root.after(0, lambda: self.app.log(msg))
            def warning(self, msg): pass
            def error(self, msg): self.app.root.after(0, lambda: self.app.log(f"BŁĄD: {msg}"))

        def progress_hook(d):
            if self.is_playlist and d.get('info_dict'):
                vid_id = d['info_dict'].get('id')
                if vid_id in self.playlist_id_map:
                    row_id = self.playlist_id_map[vid_id]
                    if d['status'] == 'downloading':
                        cur = self.tree.item(row_id)['values']
                        if cur[4] != "Pobieranie...":
                            self.root.after(0, lambda: self.tree.set(row_id, column="col5", value="Pobieranie..."))
                    elif d['status'] == 'finished':
                        self.root.after(0, lambda: self.tree.set(row_id, column="col5", value="Gotowe"))

            if d['status'] == 'downloading':
                try:
                    p = float(self._clean_ansi(d.get('_percent_str', '0%')).replace('%',''))
                    s = self._clean_ansi(d.get('_speed_str', 'N/A'))
                    e = self._clean_ansi(d.get('_eta_str', 'N/A'))
                    self.root.after(0, lambda: self.progress_bar.configure(value=p))
                    self.root.after(0, lambda: self.status_label.configure(text=f"{p:.1f}% | {s} | ETA: {e}"))
                except: pass
            elif d['status'] == 'finished':
                 if not self.is_playlist:
                    self.root.after(0, lambda: self.status_label.configure(text="Przetwarzanie..."))

        if self.is_playlist:
            out_tmpl = os.path.join(path, '%(playlist_title)s', '%(title)s.%(ext)s')
        else:
            out_tmpl = os.path.join(path, '%(title)s.%(ext)s')

        ydl_opts = {
            'logger': MyLogger(self),
            'progress_hooks': [progress_hook],
            'outtmpl': out_tmpl,
            'ffmpeg_location': self.ffmpeg_exe,
            'nocolor': True,
            'ignoreerrors': True,
        }

        pref_quality = self.settings.get("default_quality", "1080p").replace('p','')

        if mode == 'audio':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
            })
        elif self.is_playlist:
            if mode == 'video_only': ydl_opts['format'] = f"bestvideo[height<={pref_quality}]"
            else:
                ydl_opts['format'] = f"bestvideo[height<={pref_quality}]+bestaudio/best"
                ydl_opts['merge_output_format'] = 'mp4'
                ydl_opts['postprocessor_args'] = {'merger': ['-c:a', 'aac']}
        else:
            if mode == 'video_only': ydl_opts['format'] = data['format_id']
            else:
                ydl_opts['format'] = f"{data['format_id']}+bestaudio/best"
                ydl_opts['merge_output_format'] = 'mp4'
                ydl_opts['postprocessor_args'] = {'merger': ['-c:a', 'aac']}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                final_path = path

                if self.is_playlist:
                    playlist_title = info.get('title', 'Unknown Playlist')
                    final_path = os.path.join(path, playlist_title)
                    title = f"Playlista: {playlist_title}"
                else:
                    filename = ydl.prepare_filename(info)
                    if mode != 'video_only' and mode != 'audio':
                        base, _ = os.path.splitext(filename)
                        filename = base + ".mp4"
                    elif mode == 'audio':
                        base, _ = os.path.splitext(filename)
                        filename = base + ".mp3"
                    final_path = filename
                    title = info.get('title', 'Video')

                self.root.after(0, lambda: self._save_to_history(title, url, final_path))

            self.root.after(0, lambda: self.log("SUKCES: Zakończono proces."))
            self.root.after(0, lambda: self.status_label.configure(text="Gotowe!"))
            self.root.after(0, lambda: self.progress_bar.configure(value=100))
            self.root.after(0, lambda: self._show_notification("Pobieranie zakończone", f"Zapisano: {title}"))

        except Exception as e:
            self.root.after(0, lambda: self.log(f"BŁĄD KRYTYCZNY: {str(e)}"))
            self.root.after(0, lambda: self.status_label.configure(text="Błąd pobierania"))
        finally:
            self.root.after(0, lambda: self.btn_download.config(state="normal"))
            self.root.after(0, lambda: self.btn_analyze.config(state="normal"))

if __name__ == "__main__":
    myappid = 'YT Downloader Pro'
    try: ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except: pass

    root = tk.Tk()
    app = YouTubeDownloaderPro(root)
    root.mainloop()