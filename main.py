import tkinter as tk
from tkinter import filedialog
import threading
import yt_dlp
import os
import datetime
import imageio_ffmpeg
from plyer import notification

# Importy modułów
import utils
import data_manager
import ui
import windows

class YouTubeDownloaderPro:
    def __init__(self, root):
        self.root = root
        self.root.title("YT Downloader Pro v1.4.1")

        # --- LOGIKA ---
        self.data_manager = data_manager.DataManager()
        self.is_dark_mode = self.data_manager.settings.get("dark_mode", False)

        # Zmienne stanu (Model)
        self.download_path = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self.url_var = tk.StringVar()
        self.download_mode = tk.StringVar(value="video")
        self.formats_data = {}
        self.is_playlist = False
        self.playlist_entries = []
        self.playlist_id_map = {}
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        self.icon_path_ico = None

        # --- SETUP ---
        utils.center_window(self.root, 850, 850)
        self._load_icon()

        # Inicjalizacja UI (Widok) - Przekazujemy 'self' jako kontroler
        self.ui = ui.MainUI(self.root, self)

        self.log(f"System gotowy. FFmpeg załadowany.")
        self.log(f"Jakość domyślna: {self.data_manager.settings.get('default_quality', '1080p')}")

    def _load_icon(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "assets", "images", "logo.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
                self.icon_path_ico = icon_path
        except: pass

    # --- ACTION HANDLERS ---
    def log(self, msg):
        self.ui.log_to_widget(msg)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.data_manager.settings["dark_mode"] = self.is_dark_mode
        self.data_manager.save_settings(self.data_manager.settings)
        self.ui.apply_theme(self.is_dark_mode)

    def choose_directory(self):
        p = filedialog.askdirectory()
        if p: self.download_path.set(p)

    def on_mode_change(self):
        """Wywoływane TYLKO przez kliknięcie RadioButton"""
        # Czyścimy tabelę przez UI
        self.ui.clear_table()
        self.formats_data = {}
        self.playlist_id_map = {}
        self.ui.btn_download.config(state="disabled")

        # Jeśli jest URL, uruchom analizę ponownie
        if self.url_var.get().strip():
            self.start_analysis()

    # --- ANALIZA ---
    def start_analysis(self):
        url = self.url_var.get().strip()
        if not url: return

        # NAPRAWA REKURENCJI: Nie wywołujemy self.on_mode_change()!
        # Czyścimy ręcznie:
        self.ui.clear_table()
        self.formats_data = {}
        self.playlist_id_map = {}
        self.ui.btn_download.config(state="disabled")

        self.ui.btn_analyze.config(state="disabled")
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
            self.root.after(0, lambda: self.ui.btn_analyze.config(state="normal"))

    def _process_info(self, info):
        self.log(f"Tytuł: {info.get('title', 'Unknown')}")
        tree = self.ui.tree

        if 'entries' in info:
            self.is_playlist = True
            self.playlist_entries = list(info['entries'])
            self.ui.reset_tree_columns_playlist()
            self.ui.table_frame.config(text=f"Playlista: {len(self.playlist_entries)} filmów")
            self.playlist_id_map = {}
            for i, entry in enumerate(self.playlist_entries, 1):
                dur = str(datetime.timedelta(seconds=int(entry.get('duration', 0))))
                vid_id = entry.get('id')
                iid = tree.insert("", "end", values=(i, entry.get('title'), vid_id, dur, "Oczekuje"))
                if vid_id: self.playlist_id_map[vid_id] = iid
            self.ui.btn_download.config(state="normal", text="POBIERZ CAŁĄ PLAYLISTĘ")
        else:
            self.is_playlist = False
            self.ui.reset_tree_columns_video()
            self.ui.table_frame.config(text="Dostępne jakości")
            formats = info.get('formats', [])
            seen = set()
            mode = self.download_mode.get()

            if mode == "audio":
                iid = tree.insert("", "end", values=("Audio HQ", "AAC/MP3", "mp3", "Auto", "-"))
                self.formats_data[iid] = {'type': 'audio'}
            else:
                formats.sort(key=lambda x: (x.get('height') or 0, x.get('tbr') or 0), reverse=True)
                for f in formats:
                    if f.get('vcodec') == 'none' or not f.get('height'): continue
                    sc = f.get('vcodec', '').split('.')[0]
                    ext = f.get('ext'); fps = f.get('fps', 0)
                    sz = f"{(f.get('filesize') or 0)/1024/1024:.1f} MB" if f.get('filesize') else "?"
                    uk = (f.get('height'), ext, sc)
                    if uk in seen: continue
                    seen.add(uk)
                    iid = tree.insert("", "end", values=(f"{f.get('height')}p", sc, ext, sz, f"{fps}"))
                    self.formats_data[iid] = {'format_id': f.get('format_id'), 'type': 'video', 'ext': ext}

            if tree.get_children():
                self.ui.btn_download.config(state="normal", text="ROZPOCZNIJ POBIERANIE")
                tree.selection_set(tree.get_children()[0])

    # --- POBIERANIE ---
    def start_download(self):
        url, path = self.url_var.get(), self.download_path.get()
        mode = self.download_mode.get()
        if self.is_playlist:
            data = {'type': 'playlist'}
            target_info = f"Playlista ({len(self.playlist_entries)})"
        else:
            sel = self.ui.tree.selection()
            if not sel: return
            data = self.formats_data.get(sel[0])
            target_info = "Wideo"

        self.ui.btn_download.config(state="disabled")
        self.ui.btn_analyze.config(state="disabled")
        self.ui.progress_bar['value'] = 0
        self.log(f"Start: {target_info}")
        threading.Thread(target=self._download_thread, args=(url, path, data, mode), daemon=True).start()

    def _download_thread(self, url, path, data, mode):
        def progress_hook(d):
            if self.is_playlist and d.get('info_dict'):
                vid_id = d['info_dict'].get('id')
                if vid_id in self.playlist_id_map:
                    rid = self.playlist_id_map[vid_id]
                    if d['status'] == 'downloading':
                        if self.ui.tree.item(rid)['values'][4] != "Pobieranie...":
                            self.root.after(0, lambda: self.ui.tree.set(rid, column="col5", value="Pobieranie..."))
                    elif d['status'] == 'finished':
                        self.root.after(0, lambda: self.ui.tree.set(rid, column="col5", value="Gotowe"))

            if d['status'] == 'downloading':
                try:
                    p = float(utils.clean_ansi(d.get('_percent_str', '0%')).replace('%',''))
                    s = utils.clean_ansi(d.get('_speed_str', 'N/A'))
                    e = utils.clean_ansi(d.get('_eta_str', 'N/A'))
                    self.root.after(0, lambda: self.ui.progress_bar.configure(value=p))
                    self.root.after(0, lambda: self.ui.status_label.configure(text=f"{p:.1f}% | {s} | ETA: {e}"))
                except: pass
            elif d['status'] == 'finished':
                 if not self.is_playlist:
                    self.root.after(0, lambda: self.ui.status_label.configure(text="Przetwarzanie..."))

        class MyLogger:
            def __init__(self, app): self.app = app
            def debug(self, m):
                if not ('[download]' in m or 'ETA' in m) and not m.startswith('[debug] '):
                    self.app.root.after(0, lambda: self.app.log(m))
            def info(self, m):
                if not '[download]' in m: self.app.root.after(0, lambda: self.app.log(m))
            def warning(self, m): pass
            def error(self, m): self.app.root.after(0, lambda: self.app.log(f"BŁĄD: {m}"))

        if self.is_playlist: out_tmpl = os.path.join(path, '%(playlist_title)s', '%(title)s.%(ext)s')
        else: out_tmpl = os.path.join(path, '%(title)s.%(ext)s')

        ydl_opts = {
            'logger': MyLogger(self),
            'progress_hooks': [progress_hook],
            'outtmpl': out_tmpl,
            'ffmpeg_location': self.ffmpeg_exe,
            'nocolor': True,
            'ignoreerrors': True,
        }

        q = self.data_manager.settings.get("default_quality", "1080p").replace('p','')
        if mode == 'audio':
            ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]})
        elif self.is_playlist:
            if mode == 'video_only': ydl_opts['format'] = f"bestvideo[height<={q}]"
            else:
                ydl_opts['format'] = f"bestvideo[height<={q}]+bestaudio/best"
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
                    title = f"Playlista: {info.get('title', 'Playlist')}"
                    final_path = os.path.join(path, info.get('title', 'Playlist'))
                else:
                    filename = ydl.prepare_filename(info)
                    if mode != 'video_only': filename = os.path.splitext(filename)[0] + (".mp3" if mode=='audio' else ".mp4")
                    final_path = filename
                    title = info.get('title', 'Video')

                self.root.after(0, lambda: self.data_manager.add_history_entry(title, url, final_path))

            self.root.after(0, lambda: self.log("SUKCES: Zakończono proces."))
            self.root.after(0, lambda: self.ui.status_label.configure(text="Gotowe!"))
            self.root.after(0, lambda: self.ui.progress_bar.configure(value=100))

            kwargs = {'title': "Pobieranie zakończone", 'message': f"Zapisano: {title}", 'app_name': "YT Downloader Pro", 'timeout': 5}
            if self.icon_path_ico and os.path.exists(self.icon_path_ico): kwargs['app_icon'] = self.icon_path_ico
            try: notification.notify(**kwargs)
            except: pass

        except Exception as e:
            self.root.after(0, lambda: self.log(f"BŁĄD KRYTYCZNY: {str(e)}"))
            self.root.after(0, lambda: self.ui.status_label.configure(text="Błąd pobierania"))
        finally:
            self.root.after(0, lambda: self.ui.btn_download.config(state="normal"))
            self.root.after(0, lambda: self.ui.btn_analyze.config(state="normal"))

if __name__ == "__main__":
    utils.set_app_id('YT Downloader Pro')
    root = tk.Tk()
    app = YouTubeDownloaderPro(root)
    root.mainloop()