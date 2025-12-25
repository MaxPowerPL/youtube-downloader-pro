import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import os
import utils

def open_settings_window(app):
    win = Toplevel(app.root)
    win.title("Ustawienia")
    utils.center_window(win, 300, 200)

    # FIX: Odwołanie do kolorów przez app.ui.colors
    if app.is_dark_mode: win.configure(bg=app.ui.colors["bg"])

    ttk.Label(win, text="Domyślna jakość wideo (dla Playlist):").pack(pady=10)

    qualities = ["2160p", "1440p", "1080p", "720p", "480p", "360p"]
    combo = ttk.Combobox(win, values=qualities, state="readonly")

    current_q = app.data_manager.settings.get("default_quality", "1080p")
    combo.set(current_q)
    combo.pack(pady=5)

    def save():
        app.data_manager.settings["default_quality"] = combo.get()
        app.data_manager.save_settings(app.data_manager.settings)
        app.log(f"Zapisano domyślną jakość: {combo.get()}")
        win.destroy()

    ttk.Button(win, text="Zapisz", command=save).pack(pady=20)

def open_history_window(app):
    win = Toplevel(app.root)
    win.title("Zarządzanie Historią")
    utils.center_window(win, 900, 500)

    # FIX: Odwołanie do kolorów przez app.ui.colors
    if app.is_dark_mode: win.configure(bg=app.ui.colors["bg"])

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

        history_list = app.data_manager.history

        for index, item in enumerate(history_list):
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

        if not messagebox.askyesno("Potwierdzenie", f"Usunąć {len(selected_items)} wpisów?", parent=win):
            return

        indices = sorted([int(x) for x in selected_items], reverse=True)
        history_list = app.data_manager.history

        for idx in indices:
            if 0 <= idx < len(history_list):
                del history_list[idx]

        app.data_manager.rewrite_history_file()
        load_data()

    def clear_all():
        if app.data_manager.history:
            if messagebox.askyesno("Uwaga", "Wyczyścić całą historię?", parent=win):
                app.data_manager.history = []
                app.data_manager.rewrite_history_file()
                load_data()

    ttk.Button(btn_frame, text="🗑️ Usuń zaznaczone", command=delete_selected).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="❌ Wyczyść wszystko", command=clear_all).pack(side="right", padx=5)

    load_data()