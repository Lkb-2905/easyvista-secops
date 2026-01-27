import argparse
import json
import urllib.request


REQUIRED_HEADERS = [
    "strict-transport-security",
    "x-frame-options",
    "x-content-type-options",
    "content-security-policy",
    "referrer-policy",
]


def fetch_headers(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "SecOps-Checker"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return {k.lower(): v for k, v in resp.headers.items()}


OFFLINE_HEADERS = {
    "https://example.com": {"x-content-type-options": "nosniff", "referrer-policy": "no-referrer"},
    "https://github.com": {
        "strict-transport-security": "max-age=31536000",
        "x-frame-options": "deny",
        "x-content-type-options": "nosniff",
        "content-security-policy": "default-src 'none'",
        "referrer-policy": "no-referrer",
    },
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyseur de headers HTTP")
    parser.add_argument("--url", help="URL cible")
    parser.add_argument("--input", help="Fichier de URLs (une par ligne)")
    parser.add_argument("--output", default="headers_report.json")
    parser.add_argument("--offline", action="store_true", help="Mode demo sans reseau")
    args = parser.parse_args()

    targets = []
    if args.url:
        targets.append(args.url)
    if args.input:
        with open(args.input, "r", encoding="utf-8") as handle:
            targets.extend([line.strip() for line in handle if line.strip()])
    if not targets:
        raise SystemExit("Fournissez --url ou --input.")

    reports = []
    for url in targets:
        if args.offline:
            headers = OFFLINE_HEADERS.get(url, {})
        else:
            headers = fetch_headers(url)
        reports.append(
            {
                "url": url,
                "present": [h for h in REQUIRED_HEADERS if h in headers],
                "missing": [h for h in REQUIRED_HEADERS if h not in headers],
            }
        )

    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(reports, ensure_ascii=True, indent=2))
    print(f"Rapport ecrit: {args.output}")


if __name__ == "__main__":
    main()
