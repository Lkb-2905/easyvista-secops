# EasyVista - SecOps (demo portfolio)

Objectif: proposer des outils SecOps simples a demonstrer, avec sorties
faciles a capturer.

## Contenu
- `01-scanner-vulnerabilites`: scan de ports + rapport JSON.
- `02-dashboard-monitoring-secops`: tableau de bord (CLI/Streamlit).
- `03-bot-notification-incident`: detection d'incidents (log -> alerte).
- `04-verificateur-ssl`: verification expiration certificats.
- `05-analyseur-headers-securite`: verif headers OWASP.

## Demarrage rapide (demos)
```
cd 01-scanner-vulnerabilites
python scanner.py 127.0.0.1 --output report.json

cd ../02-dashboard-monitoring-secops
python app.py --cli --input logs.sample.json

cd ../03-bot-notification-incident
python notify.py --log incidents.sample.log

cd ../04-verificateur-ssl
python check_ssl.py --offline --output ssl_report.json

cd ../05-analyseur-headers-securite
python headers_check.py --input urls.sample.txt --offline --output headers_report.json
```

## Captures conseillees
- `01-scanner-vulnerabilites/report.json`
- Terminal: resume dashboard, alertes, checks SSL/headers.
- `04-verificateur-ssl/ssl_report.json`
- `05-analyseur-headers-securite/headers_report.json`

## Dependances
Voir `requirements.txt`.

## Roadmap et suggestions
- `ROADMAP.md`
- `CODE_SUGGESTIONS.md`
