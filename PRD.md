# PRD - EasyVista SecOps

## Vision
Outiller un SOC avec des scripts simples pour detection et reporting rapide.

## Probleme
Les petites equipes SecOps manquent d'outils legers pour la surveillance.

## Utilisateurs
- Analystes SOC
- Equipes ITSM / NOC

## MVP (fonctionnalites)
- Scan de ports + rapport JSON
- Dashboard CLI/Streamlit
- Alerte incident via log
- Verification SSL
- Controle headers OWASP

## Evolutions
- Integrations webhook/ITSM
- Historisation des rapports
- Score global de posture

## KPI
- Temps de detection
- Nombre d'alertes utiles
- Couverture des checks

## Entrees / Sorties
- Entrees: logs JSON, URLs, domaines
- Sorties: rapports JSON

## Contraintes
- Demos offline disponibles

## Hors perimetre
- SIEM entreprise complet
