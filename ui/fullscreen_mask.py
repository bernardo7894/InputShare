import threading
import sys
import tkinter as tk
import customtkinter as ctk

from typing import Any

from utils import VoidCallable, selected_monitor
from utils.config_manager import get_config
from utils.i18n import get_i18n
from utils.logger import LogType, LOGGER

show_event = threading.Event()
hide_event = threading.Event()
exit_event = threading.Event()
show_frozen_cursor_event = threading.Event()
hide_frozen_cursor_event = threading.Event()
frozen_cursor_shown_event = threading.Event()
frozen_cursor_position: tuple[int, int] | None = None
frozen_cursor_snapshot: tuple[Any, int, int] | None = None
frozen_cursor_photo = None
frozen_cursor_transparent_color = "#ff00ff"

def format_position(x: int, y: int) -> str:
    x_offset = f"+{x}" if x >= 0 else str(x)
    y_offset = f"+{y}" if y >= 0 else str(y)
    return f"{x_offset}{y_offset}"

def format_geometry(width: int, height: int, x: int, y: int) -> str:
    return f"{width}x{height}{format_position(x, y)}"

def set_no_activate(window: ctk.CTk | ctk.CTkToplevel):
    if sys.platform != "win32": return
    import ctypes

    GWL_EXSTYLE = -20
    WS_EX_NOACTIVATE = 0x08000000
    hwnd = window.winfo_id()
    current_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, current_style | WS_EX_NOACTIVATE)

def capture_current_cursor_snapshot() -> tuple[Any, int, int] | None:
    if sys.platform != "win32": return None
    try:
        import ctypes
        from ctypes import wintypes
        from PIL import Image

        class CURSORINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_uint),
                ("flags", ctypes.c_uint),
                ("hCursor", ctypes.c_void_p),
                ("ptScreenPos", ctypes.c_long * 2),
            ]
        class ICONINFO(ctypes.Structure):
            _fields_ = [
                ("fIcon", ctypes.c_bool),
                ("xHotspot", ctypes.c_uint),
                ("yHotspot", ctypes.c_uint),
                ("hbmMask", ctypes.c_void_p),
                ("hbmColor", ctypes.c_void_p),
            ]
        class BITMAP(ctypes.Structure):
            _fields_ = [
                ("bmType", ctypes.c_long),
                ("bmWidth", ctypes.c_long),
                ("bmHeight", ctypes.c_long),
                ("bmWidthBytes", ctypes.c_long),
                ("bmPlanes", ctypes.c_ushort),
                ("bmBitsPixel", ctypes.c_ushort),
                ("bmBits", ctypes.c_void_p),
            ]
        class BITMAPINFOHEADER(ctypes.Structure):
            _fields_ = [
                ("biSize", ctypes.c_uint),
                ("biWidth", ctypes.c_long),
                ("biHeight", ctypes.c_long),
                ("biPlanes", ctypes.c_ushort),
                ("biBitCount", ctypes.c_ushort),
                ("biCompression", ctypes.c_uint),
                ("biSizeImage", ctypes.c_uint),
                ("biXPelsPerMeter", ctypes.c_long),
                ("biYPelsPerMeter", ctypes.c_long),
                ("biClrUsed", ctypes.c_uint),
                ("biClrImportant", ctypes.c_uint),
            ]
        class BITMAPINFO(ctypes.Structure):
            _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", ctypes.c_uint * 3)]

        ctypes.windll.user32.GetCursorInfo.argtypes = [ctypes.POINTER(CURSORINFO)]
        ctypes.windll.user32.GetCursorInfo.restype = wintypes.BOOL
        ctypes.windll.user32.CopyIcon.argtypes = [wintypes.HICON]
        ctypes.windll.user32.CopyIcon.restype = wintypes.HICON
        ctypes.windll.user32.GetIconInfo.argtypes = [wintypes.HICON, ctypes.POINTER(ICONINFO)]
        ctypes.windll.user32.GetIconInfo.restype = wintypes.BOOL
        ctypes.windll.user32.DestroyIcon.argtypes = [wintypes.HICON]
        ctypes.windll.user32.DestroyIcon.restype = wintypes.BOOL
        ctypes.windll.gdi32.GetObjectW.argtypes = [wintypes.HGDIOBJ, ctypes.c_int, ctypes.c_void_p]
        ctypes.windll.gdi32.GetObjectW.restype = ctypes.c_int
        ctypes.windll.gdi32.GetDIBits.argtypes = [
            wintypes.HDC,
            wintypes.HBITMAP,
            wintypes.UINT,
            wintypes.UINT,
            ctypes.c_void_p,
            ctypes.POINTER(BITMAPINFO),
            wintypes.UINT]
        ctypes.windll.gdi32.GetDIBits.restype = ctypes.c_int
        ctypes.windll.gdi32.DeleteObject.argtypes = [wintypes.HGDIOBJ]
        ctypes.windll.gdi32.DeleteObject.restype = wintypes.BOOL

        cursor_info = CURSORINFO()
        cursor_info.cbSize = ctypes.sizeof(CURSORINFO)
        if not ctypes.windll.user32.GetCursorInfo(ctypes.byref(cursor_info)): return None
        cursor_showing = 0x00000001
        if cursor_info.flags != cursor_showing or not cursor_info.hCursor: return None

        hcursor = ctypes.windll.user32.CopyIcon(cursor_info.hCursor)
        icon_info = ICONINFO()
        if not ctypes.windll.user32.GetIconInfo(hcursor, ctypes.byref(icon_info)): return None
        hbitmap = icon_info.hbmColor or icon_info.hbmMask
        if not hbitmap: return None

        bitmap = BITMAP()
        ctypes.windll.gdi32.GetObjectW(hbitmap, ctypes.sizeof(BITMAP), ctypes.byref(bitmap))
        width = bitmap.bmWidth
        height = bitmap.bmHeight
        if icon_info.hbmColor == 0:
            height //= 2

        bmi = BITMAPINFO()
        bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmi.bmiHeader.biWidth = width
        bmi.bmiHeader.biHeight = -height
        bmi.bmiHeader.biPlanes = 1
        bmi.bmiHeader.biBitCount = 32
        bmi.bmiHeader.biCompression = 0
        buffer_size = width * height * 4
        bits = ctypes.create_string_buffer(buffer_size)
        hdc = ctypes.windll.user32.GetDC(None)
        ctypes.windll.gdi32.GetDIBits(hdc, hbitmap, 0, height, bits, ctypes.byref(bmi), 0)
        ctypes.windll.user32.ReleaseDC(None, hdc)

        image = Image.frombuffer("RGBA", (width, height), bits, "raw", "BGRA", 0, 1).copy()
        if image.getextrema()[3] == (0, 0):
            image.putalpha(255)

        if icon_info.hbmColor: ctypes.windll.gdi32.DeleteObject(icon_info.hbmColor)
        if icon_info.hbmMask: ctypes.windll.gdi32.DeleteObject(icon_info.hbmMask)
        ctypes.windll.user32.DestroyIcon(hcursor)
        return image, int(icon_info.xHotspot), int(icon_info.yHotspot)
    except Exception as e:
        LOGGER.write(LogType.Error, "Capture cursor failed: " + str(e))
        return None

def cursor_edge_blend_color(cursor_image: Any) -> str:
    try:
        rgba_image = cursor_image.convert("RGBA")
        pixels = rgba_image.load()
        width, height = rgba_image.size
        samples = []
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if 32 <= a <= 224:
                    samples.append((r, g, b))
        if len(samples) == 0:
            for y in range(height):
                for x in range(width):
                    r, g, b, a = pixels[x, y]
                    if a > 0:
                        samples.append((r, g, b))
        if len(samples) == 0: return frozen_cursor_transparent_color
        visible_colors = set(samples)
        r = int((sum(pixel[0] for pixel in samples) // len(samples)) * 0.85)
        g = int((sum(pixel[1] for pixel in samples) // len(samples)) * 0.85)
        b = int((sum(pixel[2] for pixel in samples) // len(samples)) * 0.85)
        while (r, g, b) in visible_colors:
            r = (r + 17) % 256
            g = (g + 31) % 256
            b = (b + 47) % 256
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception as e:
        LOGGER.write(LogType.Error, "Cursor blend color failed: " + str(e))
        return frozen_cursor_transparent_color

def check_event(
    root: ctk.CTk,
    toplevel: ctk.CTkToplevel,
    frozen_cursor: ctk.CTkToplevel,
    frozen_cursor_canvas: tk.Canvas):
    def show_window(root: ctk.CTk, toplevel: ctk.CTkToplevel):
        root.deiconify()
        toplevel.deiconify()
        toplevel.lift()
    def hide_window(root: ctk.CTk, toplevel: ctk.CTkToplevel):
        toplevel.withdraw()
        root.withdraw()
    def show_frozen_cursor(frozen_cursor: ctk.CTkToplevel):
        global frozen_cursor_photo, frozen_cursor_transparent_color
        if frozen_cursor_position is None: return
        x, y = frozen_cursor_position
        hotspot_x = 0
        hotspot_y = 0
        frozen_cursor_canvas.delete("all")
        if frozen_cursor_snapshot is not None:
            from PIL import ImageTk
            cursor_image, hotspot_x, hotspot_y = frozen_cursor_snapshot
            frozen_cursor_transparent_color = cursor_edge_blend_color(cursor_image)
            try:
                if sys.platform == "win32":
                    frozen_cursor.wm_attributes("-transparentcolor", frozen_cursor_transparent_color)
                frozen_cursor_canvas.configure(
                    width=cursor_image.width,
                    height=cursor_image.height,
                    bg=frozen_cursor_transparent_color)
                frozen_cursor_photo = ImageTk.PhotoImage(cursor_image, master=root)
                frozen_cursor_canvas.image = frozen_cursor_photo
                frozen_cursor_canvas.create_image(0, 0, image=frozen_cursor_photo, anchor="nw")
            except tk.TclError as e:
                LOGGER.write(LogType.Error, "Show captured cursor failed: " + str(e))
                frozen_cursor.withdraw()
                return
        else:
            frozen_cursor.withdraw()
            return
        frozen_cursor.geometry(format_position(x - hotspot_x, y - hotspot_y))
        frozen_cursor.deiconify()
        frozen_cursor.lift()
        frozen_cursor.update_idletasks()
        frozen_cursor_shown_event.set()
    def hide_frozen_cursor(frozen_cursor: ctk.CTkToplevel):
        frozen_cursor.withdraw()

    try:
        if show_event.is_set():
            show_window(root, toplevel)
            show_event.clear()
        elif hide_event.is_set():
            hide_window(root, toplevel)
            hide_event.clear()
        elif show_frozen_cursor_event.is_set():
            show_frozen_cursor(frozen_cursor)
            show_frozen_cursor_event.clear()
        elif hide_frozen_cursor_event.is_set():
            hide_frozen_cursor(frozen_cursor)
            hide_frozen_cursor_event.clear()
        elif exit_event.is_set():
            LOGGER.write(LogType.Info, "Fullscreen mask exited.")
            root.quit()
            return
    except Exception as e:
        show_event.clear()
        hide_event.clear()
        show_frozen_cursor_event.clear()
        hide_frozen_cursor_event.clear()
        frozen_cursor.withdraw()
        LOGGER.write(LogType.Error, "Fullscreen mask callback failed: " + str(e))
        frozen_cursor_shown_event.set()
    finally:
        interval_ms = 2 # 500 times per second
        root.after(interval_ms, check_event, root, toplevel, frozen_cursor, frozen_cursor_canvas)

def open_mask_window():
    i18n = get_i18n()
    config = get_config()
    monitor = selected_monitor(config.overlay_monitor_index)
    geometry = format_geometry(monitor.width, monitor.height, monitor.x, monitor.y)
    cursor_style = "none"

    root = ctk.CTk()
    root.wm_title(i18n(["InputShare Mask", "输入流转 —— 蒙版"]))
    root.wm_attributes("-alpha", 0.01)
    root.wm_attributes("-topmost", True)
    root.configure(cursor=cursor_style)
    root.overrideredirect(True)
    root.geometry(geometry)
    root.update_idletasks()
    set_no_activate(root)

    larger_font = i18n([
        ctk.CTkFont(family="Arial", size=18),
        ctk.CTkFont(family="Microsoft YaHei", size=18),
    ])

    label_toplevel = ctk.CTkToplevel(master=root)
    label_toplevel.geometry(format_position(monitor.x + 20, monitor.y + 20))
    label_toplevel.wm_title(i18n(["InputShare Shortcuts", "输入流转 —— 快捷键提示"]))
    label_toplevel.wm_attributes('-alpha', 0.6)
    label_toplevel.wm_attributes("-topmost", True)
    label_toplevel.overrideredirect(True)
    label_toplevel.configure(cursor=cursor_style)
    label_toplevel.update_idletasks()
    set_no_activate(label_toplevel)

    label1 = ctk.CTkLabel(
        master=label_toplevel,
        text=i18n(["Use <Ctrl>+<Alt>+q to quit", "使用 <Ctrl>+<Alt>+q 退出程序"]),
        font=larger_font,
    )
    label2 = ctk.CTkLabel(
        master=label_toplevel,
        text=i18n(["Use <Ctrl>+<Alt>+s to toggle", "使用 <Ctrl>+<Alt>+s 切换控制"]),
        font=larger_font,
    )
    label1.pack(padx=8, pady=4, anchor="w")
    label2.pack(padx=8, pady=4, anchor="w")

    frozen_cursor = ctk.CTkToplevel(master=root)
    frozen_cursor.geometry("+0+0")
    frozen_cursor.wm_attributes("-topmost", True)
    if sys.platform == "win32":
        frozen_cursor.wm_attributes("-transparentcolor", frozen_cursor_transparent_color)
    frozen_cursor.overrideredirect(True)
    frozen_cursor.configure(cursor="none")
    frozen_cursor.update_idletasks()
    set_no_activate(frozen_cursor)

    frozen_cursor_canvas = tk.Canvas(
        master=frozen_cursor,
        width=1,
        height=1,
        bg=frozen_cursor_transparent_color,
        highlightthickness=0)
    frozen_cursor_canvas.pack()
    frozen_cursor.withdraw()

    root.after(0, check_event, root, label_toplevel, frozen_cursor, frozen_cursor_canvas)
    root.mainloop()

def show_frozen_cursor(position: tuple[int, int], snapshot: tuple[Any, int, int] | None, wait: bool=False):
    global frozen_cursor_position, frozen_cursor_snapshot
    frozen_cursor_position = position
    frozen_cursor_snapshot = snapshot
    frozen_cursor_shown_event.clear()
    show_frozen_cursor_event.set()
    if wait:
        frozen_cursor_shown_event.wait(0.2)

def hide_frozen_cursor():
    hide_frozen_cursor_event.set()

def mask_thread_factory() -> tuple[
    VoidCallable, VoidCallable, VoidCallable,
]:
    def show_mask():
        show_event.set()
    def hide_mask():
        hide_event.set()
    def exit_mask():
        exit_event.set()

    mask_thread = threading.Thread(target=open_mask_window)
    mask_thread.start()
    return show_mask, hide_mask, exit_mask
