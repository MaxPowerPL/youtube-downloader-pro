import re
import ctypes
import os

def center_window(window, width, height):
    """Centruje podane okno na ekranie"""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    window.geometry(f"{width}x{height}+{x}+{y}")

def clean_ansi(text):
    """Usuwa kody kolorów (ANSI) z tekstu"""
    if not text: return ""
    return re.sub(r'\x1b\[[0-9;]*m', '', str(text)).strip()

def set_app_id(app_id):
    """Ustawia ID aplikacji dla paska zadań Windows"""
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except:
        pass