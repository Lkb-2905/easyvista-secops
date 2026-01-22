import argparse
import json
import os
import urllib.request


KEYWORDS = ["error", "critical", "failed", "panic"]


def read_lines(path: str) -> list:
    with open(path, "r", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def detect_incidents(lines: list) -> list:
    incidents = []
    for line in lines:
        lowered = line.lower()
        if any(keyword in lowered for keyword in KEYWORDS):
            incidents.append(line)
    return incidents


def send_webhook(url: str, message: str) -> None:
    payload = {"text": message}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        resp.read()


def main() -> None:
    parser = argparse.ArgumentParser(description="Bot notification incident (webhook)")
    parser.add_argument("--log", default="incidents.log")
    parser.add_argument("--webhook", default=os.getenv("WEBHOOK_URL", ""))
    args = parser.parse_args()

    lines = read_lines(args.log)
    incidents = detect_incidents(lines)
    if not incidents:
        print("Aucun incident detecte.")
        return

    message = "Alerte incident:\n" + "\n".join(incidents[:5])
    if not args.webhook:
        print(message)
        return
    send_webhook(args.webhook, message)
    print("Alerte envoyee.")


if __name__ == "__main__":
    main()
