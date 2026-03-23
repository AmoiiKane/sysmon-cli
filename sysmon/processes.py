import psutil


def get_top_processes(n: int = 10) -> list[dict]:
    """Return top N processes sorted by CPU usage."""
    procs = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status"]):
        try:
            info = proc.info
            if info["cpu_percent"] is None:
                info["cpu_percent"] = 0.0
            if info["memory_percent"] is None:
                info["memory_percent"] = 0.0
            procs.append({
                "pid": info["pid"],
                "name": info["name"],
                "cpu_percent": round(info["cpu_percent"], 1),
                "mem_percent": round(info["memory_percent"], 1),
                "status": info["status"],
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return sorted(procs, key=lambda x: x["cpu_percent"], reverse=True)[:n]
