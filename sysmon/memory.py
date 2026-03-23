import psutil


def get_memory_info() -> dict:
    """Return RAM and swap usage stats."""
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "ram": {
            "total_gb": round(ram.total / 1e9, 2),
            "used_gb": round(ram.used / 1e9, 2),
            "available_gb": round(ram.available / 1e9, 2),
            "percent": ram.percent,
        },
        "swap": {
            "total_gb": round(swap.total / 1e9, 2),
            "used_gb": round(swap.used / 1e9, 2),
            "percent": swap.percent,
        },
    }
