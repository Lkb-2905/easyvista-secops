import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> None:
    result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
    assert result.returncode == 0


def test_demo_runs(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    run(
        [
            sys.executable,
            str(repo / "01-scanner-vulnerabilites" / "scanner.py"),
            "127.0.0.1",
            "--output",
            str(tmp_path / "report.json"),
        ],
        cwd=repo / "01-scanner-vulnerabilites",
    )
    run(
        [
            sys.executable,
            str(repo / "02-dashboard-monitoring-secops" / "app.py"),
            "--cli",
            "--input",
            str(repo / "02-dashboard-monitoring-secops" / "logs.sample.json"),
        ],
        cwd=repo / "02-dashboard-monitoring-secops",
    )
    run(
        [
            sys.executable,
            str(repo / "04-verificateur-ssl" / "check_ssl.py"),
            "--offline",
            "--output",
            str(tmp_path / "ssl_report.json"),
        ],
        cwd=repo / "04-verificateur-ssl",
    )
