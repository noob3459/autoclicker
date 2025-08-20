#!/usr/bin/env python3
"""
Simple, safe autoclicker.

Hotkeys (changeable via flags):
  • Start/Stop toggle: F8
  • Quit:             F9

Examples:
  python autoclicker.py --cps 12            # 12 clicks per second, left button
  python autoclicker.py --button right       # right button instead
  python autoclicker.py --start-key f6 --quit-key f7

Notes (macOS):
  - You must grant Accessibility permissions to your terminal/IDE for this to work:
    System Settings → Privacy & Security → Accessibility → enable your terminal/IDE.
"""

import argparse
import threading
import time
from pynput import mouse, keyboard

BUTTON_MAP = {
    "left": mouse.Button.left,
    "right": mouse.Button.right,
    "middle": mouse.Button.middle,
}

FUNCTION_KEYS = {
    "f1": keyboard.Key.f1, "f2": keyboard.Key.f2, "f3": keyboard.Key.f3, "f4": keyboard.Key.f4,
    "f5": keyboard.Key.f5, "f6": keyboard.Key.f6, "f7": keyboard.Key.f7, "f8": keyboard.Key.f8,
    "f9": keyboard.Key.f9, "f10": keyboard.Key.f10, "f11": keyboard.Key.f11, "f12": keyboard.Key.f12,
}


class AutoClicker:
    def __init__(self, cps: float, button: str, start_key: str, quit_key: str):
        self.interval = max(0.0005, 1.0 / cps)  # seconds between clicks
        self.button = BUTTON_MAP[button]
        self.start_key = FUNCTION_KEYS[start_key]
        self.quit_key = FUNCTION_KEYS[quit_key]
        self.mouse = mouse.Controller()
        self.running = False
        self.exiting = False
        self.thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        while not self.exiting:
            if self.running:
                try:
                    self.mouse.click(self.button)
                except Exception:
                    # ignore transient OS errors
                    pass
                time.sleep(self.interval)
            else:
                time.sleep(0.02)

    def toggle(self):
        self.running = not self.running
        state = "ON" if self.running else "OFF"
        print(f"[autoclicker] Toggled {state}")

    def start(self):
        print(
            "[autoclicker] Ready. Press your start/stop key to toggle, quit key to exit.")
        self.thread.start()
        with keyboard.Listener(on_press=self._on_press) as listener:
            listener.join()

    def _on_press(self, key):
        if key == self.start_key:
            self.toggle()
        elif key == self.quit_key:
            self.exiting = True
            print("[autoclicker] Exiting…")
            return False  # stop listener


def parse_args():
    p = argparse.ArgumentParser(description="Simple autoclicker with hotkeys.")
    p.add_argument("--cps", type=float, default=10.0,
                   help="Clicks per second (default 10)")
    p.add_argument("--button", choices=list(BUTTON_MAP.keys()),
                   default="left", help="Mouse button")
    p.add_argument("--start-key", choices=list(FUNCTION_KEYS.keys()),
                   default="f8", help="Toggle key")
    p.add_argument("--quit-key", choices=list(FUNCTION_KEYS.keys()),
                   default="f9", help="Quit key")
    return p.parse_args()


def main():
    args = parse_args()
    print(
        f"[autoclicker] cps={args.cps}, button={args.button}, start={args.start_key}, quit={args.quit_key}")
    ac = AutoClicker(cps=args.cps, button=args.button,
                     start_key=args.start_key, quit_key=args.quit_key)
    ac.start()


if __name__ == "__main__":
    main()
