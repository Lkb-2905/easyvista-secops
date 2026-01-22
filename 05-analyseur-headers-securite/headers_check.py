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


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyseur de headers HTTP")
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", default="headers_report.json")
    args = parser.parse_args()

    headers = fetch_headers(args.url)
    report = {
        "url": args.url,
        "present": [h for h in REQUIRED_HEADERS if h in headers],
        "missing": [h for h in REQUIRED_HEADERS if h not in headers],
    }

    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(report, ensure_ascii=True, indent=2))
    print(f"Rapport ecrit: {args.output}")


if __name__ == "__main__":
    main()
