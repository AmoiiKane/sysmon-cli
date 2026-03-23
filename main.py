#!/usr/bin/env python3
"""
sysmon-cli — A clean system resource monitor for the terminal.
Usage:
    python main.py              # single snapshot
    python main.py --watch      # live refresh every 2s
    python main.py --watch --interval 5
    python main.py --export     # save snapshot to JSON
"""

import argparse
import json
import time
from datetime import datetime

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table
from rich.text import Text

from sysmon import (
    get_cpu_info,
    get_disk_info,
    get_memory_info,
    get_network_info,
    get_top_processes,
)

console = Console()


def make_bar(percent: float, width: int = 30) -> Text:
    """Render a colored progress bar as Rich Text."""
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    color = "green" if percent < 60 else "yellow" if percent < 85 else "red"
    return Text(f"[{bar}] {percent:.1f}%", style=color)


def build_cpu_panel(cpu: dict) -> Panel:
    table = Table.grid(padding=(0, 1))
    table.add_column(style="bold cyan", width=20)
    table.add_column()

    table.add_row("Overall Usage", make_bar(cpu["usage_percent"]))
    table.add_row("Physical Cores", str(cpu["cores_physical"]))
    table.add_row("Logical Cores", str(cpu["cores_logical"]))
    if cpu["freq_current"]:
        table.add_row("Frequency", f"{cpu['freq_current']} MHz (max {cpu['freq_max']} MHz)")

    # Per-core bars
    for i, pct in enumerate(cpu["per_core"]):
        table.add_row(f"  Core {i}", make_bar(pct, width=20))

    return Panel(table, title="[bold cyan]⚙ CPU[/bold cyan]", border_style="cyan")


def build_memory_panel(mem: dict) -> Panel:
    table = Table.grid(padding=(0, 1))
    table.add_column(style="bold magenta", width=20)
    table.add_column()

    r = mem["ram"]
    s = mem["swap"]
    table.add_row("RAM", make_bar(r["percent"]))
    table.add_row("", f"Used {r['used_gb']} GB / {r['total_gb']} GB  —  Free {r['available_gb']} GB")
    table.add_row("Swap", make_bar(s["percent"]))
    table.add_row("", f"Used {s['used_gb']} GB / {s['total_gb']} GB")

    return Panel(table, title="[bold magenta]🧠 Memory[/bold magenta]", border_style="magenta")


def build_disk_panel(disks: list) -> Panel:
    table = Table(show_header=True, header_style="bold yellow", box=None, padding=(0, 1))
    table.add_column("Mount", style="yellow")
    table.add_column("FS")
    table.add_column("Total")
    table.add_column("Used")
    table.add_column("Free")
    table.add_column("Usage", min_width=36)

    for d in disks:
        table.add_row(
            d["mountpoint"],
            d["fstype"],
            f"{d['total_gb']} GB",
            f"{d['used_gb']} GB",
            f"{d['free_gb']} GB",
            make_bar(d["percent"]),
        )

    return Panel(table, title="[bold yellow]💾 Disk[/bold yellow]", border_style="yellow")


def build_network_panel(net: dict) -> Panel:
    table = Table.grid(padding=(0, 1))
    table.add_column(style="bold green", width=20)
    table.add_column()

    table.add_row("Sent", f"{net['bytes_sent_mb']} MB  ({net['packets_sent']:,} packets)")
    table.add_row("Received", f"{net['bytes_recv_mb']} MB  ({net['packets_recv']:,} packets)")

    return Panel(table, title="[bold green]🌐 Network[/bold green]", border_style="green")


def build_processes_panel(procs: list) -> Panel:
    table = Table(show_header=True, header_style="bold red", box=None, padding=(0, 1))
    table.add_column("PID", style="dim", width=8)
    table.add_column("Name")
    table.add_column("CPU %", justify="right")
    table.add_column("MEM %", justify="right")
    table.add_column("Status")

    for p in procs:
        cpu_color = "green" if p["cpu_percent"] < 10 else "yellow" if p["cpu_percent"] < 50 else "red"
        table.add_row(
            str(p["pid"]),
            p["name"],
            f"[{cpu_color}]{p['cpu_percent']}[/{cpu_color}]",
            f"{p['mem_percent']}",
            p["status"],
        )

    return Panel(table, title="[bold red]📋 Top Processes[/bold red]", border_style="red")


def build_dashboard() -> str:
    cpu = get_cpu_info()
    mem = get_memory_info()
    disks = get_disk_info()
    net = get_network_info()
    procs = get_top_processes(10)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"\n[bold]sysmon-cli[/bold]  [dim]{timestamp}[/dim]\n")
    console.print(build_cpu_panel(cpu))
    console.print(build_memory_panel(mem))
    console.print(build_disk_panel(disks))
    console.print(build_network_panel(net))
    console.print(build_processes_panel(procs))


def build_renderable():
    """Build all panels as a single renderable for Live mode."""
    from rich.console import Group

    cpu = get_cpu_info()
    mem = get_memory_info()
    disks = get_disk_info()
    net = get_network_info()
    procs = get_top_processes(10)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = Text(f"sysmon-cli  —  {timestamp}", style="bold")

    return Group(
        header,
        build_cpu_panel(cpu),
        build_memory_panel(mem),
        build_disk_panel(disks),
        build_network_panel(net),
        build_processes_panel(procs),
    )


def export_snapshot():
    data = {
        "timestamp": datetime.now().isoformat(),
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
        "network": get_network_info(),
        "processes": get_top_processes(10),
    }
    filename = f"sysmon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    console.print(f"[green]✓ Snapshot exported to[/green] [bold]{filename}[/bold]")


def main():
    parser = argparse.ArgumentParser(
        description="sysmon-cli — Terminal system resource monitor"
    )
    parser.add_argument("--watch", action="store_true", help="Live refresh mode")
    parser.add_argument("--interval", type=int, default=2, help="Refresh interval in seconds (default: 2)")
    parser.add_argument("--export", action="store_true", help="Export snapshot to JSON")
    args = parser.parse_args()

    if args.export:
        export_snapshot()
        return

    if args.watch:
        console.print("[bold cyan]sysmon-cli[/bold cyan] — live mode  [dim](Ctrl+C to quit)[/dim]\n")
        with Live(build_renderable(), refresh_per_second=1, screen=True) as live:
            try:
                while True:
                    time.sleep(args.interval)
                    live.update(build_renderable())
            except KeyboardInterrupt:
                console.print("\n[dim]Stopped.[/dim]")
    else:
        build_dashboard()


if __name__ == "__main__":
    main()
