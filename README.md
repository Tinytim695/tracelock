# 🔒 TraceLock

[![Version](https://img.shields.io/badge/version-0.2.0-blue)](VERSION)
[![Python](https://img.shields.io/badge/python-3.9%2B-yellow)](https://www.python.org/)
[![Privacy](https://img.shields.io/badge/privacy-local--first-success)](#-privacy)
[![CI](https://github.com/Tinytim695/tracelock/actions/workflows/quality.yml/badge.svg)](https://github.com/Tinytim695/tracelock/actions/workflows/quality.yml)
[![License](https://img.shields.io/badge/license-MIT-informational)](LICENSE)

**Make command-line work reproducible without turning your terminal into a black box.**

TraceLock wraps a command you are authorised to run and records the conditions and result locally.

## What it records

- UTC start time
- elapsed time
- exact argument vector
- working directory
- resolved executable path
- first useful version response, when available
- exit code
- SHA-256 of stdout and stderr
- optional captured stdout and stderr
- filtered environment summary

Each run gets a stable local record ID.

## Installation

Requires Python 3.9+.

```bash
git clone https://github.com/Tinytim695/tracelock.git
cd tracelock
chmod +x tracelock
sudo install -m 0755 tracelock /usr/local/bin/tracelock
```

Or run directly:

```bash
python3 tracelock -- printf 'hello\n'
```

## Usage

Record a command:

```bash
tracelock -- curl http://127.0.0.1:8080/
```

Record a security-tool run:

```bash
tracelock -- nmap -sV 127.0.0.1
```

Keep hashes but do not store command output:

```bash
tracelock --no-capture -- your-command --argument value
```

List records:

```bash
tracelock list
```

Inspect one record:

```bash
tracelock show RUN_ID
```

Check a record without rerunning anything:

```bash
tracelock verify RUN_ID
```

Records live under:

```text
~/.tracelock/
```

Set a different local storage directory with:

```bash
TRACELOCK_HOME=/path/to/records tracelock -- your-command
```

## 🔐 Privacy

TraceLock has no network service, daemon, telemetry or automatic upload.

Environment variables whose names suggest keys, tokens, secrets, passwords, cookies or authentication data are omitted from the environment snapshot.

Captured stdout/stderr can still contain sensitive information. Use `--no-capture` when retaining output is unnecessary.

TraceLock **never reruns a recorded command**. `verify` validates the record structure only.

## Why it exists

Security testing, incident response, debugging and research often produce results that are difficult to reproduce later.

TraceLock adds a lightweight audit trail around ordinary command-line work without requiring a database or hosted service.

## Scope

Use only with commands and data you are authorised to run and retain.

## License

MIT
