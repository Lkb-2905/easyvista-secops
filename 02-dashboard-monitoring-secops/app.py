import argparse
import json
from collections import Counter


def load_logs(path: str) -> list:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def summarize(logs: list) -> dict:
    status_counts = Counter(item.get("status", "unknown") for item in logs)
    severity_counts = Counter(item.get("severity", "low") for item in logs)
    return {
        "status_counts": dict(status_counts),
        "severity_counts": dict(severity_counts),
        "total": len(logs),
    }


def cli_mode(path: str) -> None:
    logs = load_logs(path)
    summary = summarize(logs)
    print("Total logs:", summary["total"])
    print("Etat serveurs:", summary["status_counts"])
    print("Criticite:", summary["severity_counts"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Dashboard SecOps (Streamlit ou CLI)")
    parser.add_argument("--input", default="logs.sample.json")
    parser.add_argument("--cli", action="store_true", help="Mode CLI sans Streamlit")
    args = parser.parse_args()

    if args.cli:
        cli_mode(args.input)
        return

    try:
        import streamlit as st
    except Exception:
        print("Streamlit requis. Installez: pip install streamlit")
        print("Astuce: relancez avec --cli pour une demo.")
        return

    st.set_page_config(page_title="SecOps Monitoring", layout="wide")
    st.title("Dashboard de Monitoring SecOps")

    path = st.text_input("Fichier JSON", args.input)
    try:
        logs = load_logs(path)
    except Exception as exc:
        st.error(f"Erreur lecture: {exc}")
        return

    summary = summarize(logs)
    st.metric("Total logs", summary["total"])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Etat serveurs")
        st.bar_chart(summary["status_counts"])
    with col2:
        st.subheader("Criticite")
        st.bar_chart(summary["severity_counts"])

    st.subheader("Logs")
    st.dataframe(logs)


if __name__ == "__main__":
    main()
