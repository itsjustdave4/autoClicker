import time
import threading
import platform
import os

# Versuche 'mouse' zu nutzen (globaler Hook + Klick)
try:
    import mouse as mouse_lib
except Exception:
    mouse_lib = None

# Fallback: pynput (oft zuverlässiger zum Hören unter Linux/macOS)
try:
    from pynput.mouse import Controller, Button, Listener
    pynput_available = True
except Exception:
    pynput_available = False

# Steuerflags
pause_event = threading.Event()   # gesetzt = läuft, nicht gesetzt = pausiert
pause_event.set()
stop_event = threading.Event()

def safe_click():
    """Führe einen Linksklick aus, ohne die Hauptschleife zu blockieren."""
    def _do_click():
        # Erst 'mouse' versuchen
        if mouse_lib:
            try:
                mouse_lib.click("left")
                return
            except Exception:
                pass
        # Fallback: pynput
        if pynput_available:
            try:
                ctl = Controller()
                ctl.press(Button.left)
                ctl.release(Button.left)
                return
            except Exception:
                pass
        # Wenn beides nicht klappt, einfach still weitermachen
    threading.Thread(target=_do_click, daemon=True).start()

def toggle_pause(_=None):
    if pause_event.is_set():
        pause_event.clear()
        print("Gestoppt", flush=True)
    else:
        pause_event.set()
        print("Gestartet", flush=True)

def worker_loop():
    n = 0
    while not stop_event.is_set():
        pause_event.wait()  # blockiert, solange pausiert
        print(f"Clicked {n} times", flush=True)
        safe_click()
        n += 1
        time.sleep(0.25)

if __name__ == "__main__":
    # Rechtsklick abhören (mouse bevorzugt, sonst pynput)
    listener = None
    if mouse_lib:
        mouse_lib.on_right_click(toggle_pause)
    elif pynput_available:
        def on_click(x, y, button, pressed):
            if pressed and button == Button.right:
                toggle_pause()
        listener = Listener(on_click=on_click)
        listener.daemon = True
        listener.start()
    else:
        print("Hinweis: Weder 'mouse' noch 'pynput' verfügbar – Toggle per Rechtsklick deaktiviert.", flush=True)

    # Hinweis für Wayland (häufige Ursache für blockierende/verbietene Klick-Simulation)
    if platform.system() == "Linux" and os.environ.get("XDG_SESSION_TYPE") == "wayland":
        print("Achtung: Unter Wayland sind synthetische Klicks oft eingeschränkt. "
              "Alternativen: Xorg-Session, 'ydotool' oder geeignete Rechte/Udev-Regeln.", flush=True)

    t = threading.Thread(target=worker_loop, daemon=True)
    t.start()
    try:
        while True:
            time.sleep(10)  # Hauptthread am Leben halten
    except KeyboardInterrupt:
        stop_event.set()
        print("Beendet.", flush=True)
