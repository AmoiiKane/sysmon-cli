import psutil


def get_network_info() -> dict:
    """Return network I/O stats."""
    io = psutil.net_io_counters()
    return {
        "bytes_sent_mb": round(io.bytes_sent / 1e6, 2),
        "bytes_recv_mb": round(io.bytes_recv / 1e6, 2),
        "packets_sent": io.packets_sent,
        "packets_recv": io.packets_recv,
    }
