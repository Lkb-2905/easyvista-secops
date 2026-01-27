import argparse
import json
import socket
from datetime import datetime, timezone
from typing import Dict, List


DEFAULT_PORTS = [22, 80, 443, 3389, 5432, 6379, 8080]


def scan_port(host: str, port: int, timeout: float) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def scan_host(host: str, ports: List[int], timeout: float) -> Dict[str, object]:
    open_ports = []
    for port in ports:
        if scan_port(host, port, timeout):
            open_ports.append(port)
    return {
        "host": host,
        "open_ports": open_ports,
        "scanned_ports": ports,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def parse_ports(raw: str) -> List[int]:
    ports = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        ports.append(int(item))
    return ports


def main() -> None:
    parser = argparse.ArgumentParser(description="Scanner de ports simple (JSON)")
    parser.add_argument("host", help="IP ou domaine cible")
    parser.add_argument("--ports", default=",".join(str(p) for p in DEFAULT_PORTS))
    parser.add_argument("--timeout", type=float, default=0.5)
    parser.add_argument("--output", default="report.json")
    args = parser.parse_args()

    ports = parse_ports(args.ports)
    result = scan_host(args.host, ports, args.timeout)
    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(result, ensure_ascii=True, indent=2))
    print(f"Rapport ecrit: {args.output}")


if __name__ == "__main__":
    main()
