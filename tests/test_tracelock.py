import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tracelock"


def run(tmp_path, *args):
    env = dict(os.environ)
    env["TRACELOCK_HOME"] = str(tmp_path / "records")
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_records_command_and_hashes(tmp_path):
    result = run(tmp_path, "--", sys.executable, "-c", "print('hello')")
    assert result.returncode == 0

    records = list((tmp_path / "records").glob("*.json"))
    assert len(records) == 1

    data = json.loads(records[0].read_text(encoding="utf-8"))
    assert data["argv"][0] == sys.executable
    assert data["exit_code"] == 0
    assert data["stdout"] == "hello\n"
    assert len(data["stdout_sha256"]) == 64


def test_no_capture(tmp_path):
    result = run(tmp_path, "--no-capture", "--", sys.executable, "-c", "print('secret')")
    assert result.returncode == 0

    record = next((tmp_path / "records").glob("*.json"))
    data = json.loads(record.read_text(encoding="utf-8"))
    assert data["captured_output"] is False
    assert data["stdout"] is None
    assert len(data["stdout_sha256"]) == 64


def test_list_show_and_verify(tmp_path):
    result = run(tmp_path, "--", sys.executable, "-c", "print('x')")
    assert result.returncode == 0
    run_id = result.stdout.splitlines()[0].split(":", 1)[1].strip()

    listed = run(tmp_path, "list")
    assert listed.returncode == 0
    assert run_id in listed.stdout

    shown = run(tmp_path, "show", run_id)
    assert shown.returncode == 0
    assert run_id in shown.stdout

    verified = run(tmp_path, "verify", run_id)
    assert verified.returncode == 0
    assert "does not rerun" in verified.stdout


def test_missing_command(tmp_path):
    result = run(tmp_path, "--", "definitely-not-a-command")
    assert result.returncode == 127
