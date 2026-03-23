import psutil


def get_cpu_info() -> dict:
    """Return CPU usage stats."""
    freq = psutil.cpu_freq()
    return {
        "usage_percent": psutil.cpu_percent(interval=0.5),
        "per_core": psutil.cpu_percent(interval=0.5, percpu=True),
        "cores_physical": psutil.cpu_count(logical=False),
        "cores_logical": psutil.cpu_count(logical=True),
        "freq_current": round(freq.current, 1) if freq else None,
        "freq_max": round(freq.max, 1) if freq else None,
    }
