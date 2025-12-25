import tkinter as tk
from tkinter import ttk, scrolledtext
import datetime
import windows

class MainUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.colors = {
            "bg": "#f0f0f0", "fg": "black", "frame_bg": "#f0f0f0", "input_bg": "white",
            "tree_bg": "white", "tree_fg": "black", "log_bg": "white", "log_fg": "black"
        }

        self.style = ttk.Style()
        self.setup_styles()
        self.build_widgets()

        self.apply_theme(self.controller.is_dark_mode)

    def setup_styles(self):
        self.style.theme_use('clam')
        self._configure_style_colors()

    def _configure_style_colors(self):
        c = self.colors
        self.root.configure(bg=c["bg"])
        self.style.configure("TFrame", background=c["frame_bg"])
        self.style.configure("TLabel", background=c["frame_bg"], foreground=c["fg"], font=("Segoe UI", 9))
        self.style.configure("TLabelframe", background=c["frame_bg"], foreground=c["fg"], font=("Segoe UI", 9, "bold"))
        self.style.configure("TLabelframe.Label", background=c["frame_bg"], foreground=c["fg"])
        self.style.configure("TButton", font=("Segoe UI", 9))
        self.style.configure("Big.TButton", font=("Segoe UI", 11, "bold"))
        self.style.configure("TEntry", fieldbackground=c["input_bg"], foreground=c["fg"])

        self.style.configure("Treeview", background=c["tree_bg"], foreground=c["tree_fg"],
                             fieldbackground=c["tree_bg"], font=("Segoe UI", 9), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        self.style.map("Treeview", background=[('selected', '#0078d7')])
        self.style.configure("Green.Horizontal.TProgressbar", troughcolor='#d9d9d9', background='#4caf50')

    def apply_theme(self, is_dark):
        if is_dark:
            self.colors = {
                "bg": "#2b2b2b", "fg": "#e0e0e0", "frame_bg": "#2b2b2b", "input_bg": "#3c3f41",
                "tree_bg": "#3c3f41", "tree_fg": "#e0e0e0", "log_bg": "#1e1e1e", "log_fg": "#00ff00"
            }
            self.btn_theme.config(text="☀️ Tryb Jasny")
        else:
            self.colors = {
                "bg": "#f0f0f0", "fg": "black", "frame_bg": "#f0f0f0", "input_bg": "white",
                "tree_bg": "white", "tree_fg": "black", "log_bg": "white", "log_fg": "black"
            }
            self.btn_theme.config(text="🌙 Tryb Ciemny")

        self._configure_style_colors()
        self.log_widget.config(bg=self.colors["log_bg"], fg=self.colors["log_fg"])

    def build_widgets(self):
        pad = 10

        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill="x", padx=pad, pady=(5, 0))

        ttk.Button(toolbar, text="⚙️ Ustawienia",
                   command=lambda: windows.open_settings_window(self.controller)).pack(side="left", padx=(0, 5))
        ttk.Button(toolbar, text="📜 Historia",
                   command=lambda: windows.open_history_window(self.controller)).pack(side="left", padx=(0, 5))

        self.btn_theme = ttk.Button(toolbar, text="🌙 Tryb Ciemny", command=self.controller.toggle_theme)
        self.btn_theme.pack(side="right")

        f_frame = ttk.LabelFrame(self.root, text="Folder zapisu", padding=10)
        f_frame.pack(fill="x", padx=pad, pady=(5, 5))
        ttk.Entry(f_frame, textvariable=self.controller.download_path, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(f_frame, text="Zmień...", command=self.controller.choose_directory).pack(side="right")

        u_frame = ttk.LabelFrame(self.root, text="Adres filmu / Playlisty", padding=10)
        u_frame.pack(fill="x", padx=pad, pady=5)
        ttk.Entry(u_frame, textvariable=self.controller.url_var).pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_analyze = ttk.Button(u_frame, text="Szukaj", command=self.controller.start_analysis)
        self.btn_analyze.pack(side="right")

        m_frame = ttk.Frame(self.root, padding=(pad, 5))
        m_frame.pack(fill="x", anchor="w")
        ttk.Label(m_frame, text="Tryb:").pack(side="left", padx=(0, 10))

        modes = [("Wideo+Audio", "video"), ("Tylko Wideo", "video_only"), ("Tylko Dźwięk", "audio")]
        for text, val in modes:
            ttk.Radiobutton(m_frame, text=text, variable=self.controller.download_mode, value=val,
                            command=self.controller.on_mode_change).pack(side="left", padx=5)

        self.table_frame = ttk.LabelFrame(self.root, text="Zawartość", padding=10)
        self.table_frame.pack(fill="both", expand=True, padx=pad, pady=5)

        cols = ("col1", "col2", "col3", "col4", "col5")
        self.tree = ttk.Treeview(self.table_frame, columns=cols, show="headings", selectmode="browse", height=8)
        self.reset_tree_columns_video()

        scroll = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.btn_download = ttk.Button(self.root, text="ROZPOCZNIJ POBIERANIE", style="Big.TButton",
                                       state="disabled", command=self.controller.start_download)
        self.btn_download.pack(fill="x", padx=pad, pady=10, ipady=5)

        l_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        l_frame.pack(fill="both", expand=True, padx=pad, pady=(0, pad))

        self.status_label = ttk.Label(l_frame, text="Gotowy", font=("Segoe UI", 9, "bold"))
        self.status_label.pack(anchor="w", pady=(0, 2))

        self.progress_bar = ttk.Progressbar(l_frame, orient="horizontal", mode="determinate", style="Green.Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", pady=(0, 10))

        self.log_widget = scrolledtext.ScrolledText(l_frame, height=6, state='disabled', font=("Consolas", 9))
        self.log_widget.pack(fill="both", expand=True)

    def log_to_widget(self, message):
        ts = datetime.datetime.now().strftime("[%H:%M:%S]")
        self.log_widget.config(state='normal')
        self.log_widget.insert(tk.END, f"{ts} {message}\n")
        self.log_widget.see(tk.END)
        self.log_widget.config(state='disabled')

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def reset_tree_columns_video(self):
        self.tree.heading("col1", text="Jakość")
        self.tree.heading("col2", text="Kodek")
        self.tree.heading("col3", text="Format")
        self.tree.heading("col4", text="Rozmiar")
        self.tree.heading("col5", text="FPS")
        self.tree.column("col1", width=80); self.tree.column("col2", width=80)
        self.tree.column("col3", width=60); self.tree.column("col4", width=100); self.tree.column("col5", width=60)

    def reset_tree_columns_playlist(self):
        self.tree.heading("col1", text="Lp.")
        self.tree.heading("col2", text="Tytuł Wideo")
        self.tree.heading("col3", text="ID")
        self.tree.heading("col4", text="Czas")
        self.tree.heading("col5", text="Status")
        self.tree.column("col1", width=40); self.tree.column("col2", width=350)
        self.tree.column("col3", width=100); self.tree.column("col4", width=80); self.tree.column("col5", width=120)