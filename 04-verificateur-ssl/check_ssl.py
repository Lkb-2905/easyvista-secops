import argparse
import json
import socket
import ssl
from datetime import datetime, timezone


def get_expiry(domain: str) -> str:
    context = ssl.create_default_context()
    with socket.create_connection((domain, 443), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()
    return cert.get("notAfter", "")


def parse_expiry(raw: str) -> datetime | None:
    if not raw:
        return None
    return datetime.strptime(raw, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verifier expiration SSL")
    parser.add_argument("--input", default="domains.txt")
    parser.add_argument("--threshold", type=int, default=30)
    parser.add_argument("--output", default="ssl_report.json")
    args = parser.parse_args()

    results = []
    with open(args.input, "r", encoding="utf-8") as handle:
        domains = [line.strip() for line in handle if line.strip()]

    now = datetime.now(timezone.utc)
    for domain in domains:
        try:
            raw = get_expiry(domain)
            expiry = parse_expiry(raw)
            days_left = (expiry - now).days if expiry else None
            results.append(
                {
                    "domain": domain,
                    "expires_at": raw,
                    "days_left": days_left,
                    "expires_soon": days_left is not None and days_left < args.threshold,
                }
            )
        except Exception as exc:
            results.append({"domain": domain, "error": str(exc)})

    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(results, ensure_ascii=True, indent=2))
    print(f"Rapport ecrit: {args.output}")


if __name__ == "__main__":
    main()
