# sysmon-cli 🖥️

A clean, real-time system resource monitor for the terminal — built with Python.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-lightgrey?style=for-the-badge)

---

## Features

- **CPU** — overall usage, per-core breakdown, frequency
- **Memory** — RAM and swap with visual progress bars
- **Disk** — all mounted partitions with usage stats
- **Network** — total bytes sent/received
- **Processes** — top 10 by CPU usage, live updated
- **Live mode** — auto-refreshing dashboard (`--watch`)
- **Export** — snapshot to JSON (`--export`)

---

## Installation

```bash
git clone https://github.com/AmoiiKane/sysmon-cli.git
cd sysmon-cli
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

```bash
# Single snapshot
python main.py

# Live refresh (updates every 2 seconds)
python main.py --watch

# Custom refresh interval (5 seconds)
python main.py --watch --interval 5

# Export snapshot to JSON
python main.py --export
```

---

## Project Structure

```
sysmon-cli/
├── sysmon/
│   ├── __init__.py
│   ├── cpu.py          # CPU stats via psutil
│   ├── memory.py       # RAM & swap stats
│   ├── disk.py         # Disk partition stats
│   ├── network.py      # Network I/O stats
│   └── processes.py    # Top processes by CPU
├── main.py             # CLI entry point & Rich UI
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.10+
- Linux or macOS
- [`psutil`](https://pypi.org/project/psutil/) — system data
- [`rich`](https://pypi.org/project/rich/) — terminal UI

---

## License

MIT — free to use, modify, and distribute.

---

*Built by [AmoiiKane](https://github.com/AmoiiKane)*
