# Simple Autoclicker (Python)

Run:

```bash
python autoclicker.py --cps 10
```
cat > README.md <<'EOF'
# Simple Autoclicker (Python)

A lightweight Python autoclicker built with `pynput`.

## Features
- Toggle with hotkeys (default **F8** start/stop, **F9** quit)
- Adjustable clicks per second (`--cps 12`)
- Choose mouse button (`--button left|right|middle`)
- Cross-platform (macOS/Windows/Linux)

## Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
