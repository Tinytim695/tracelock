# TraceLock

A small local wrapper that records how a command-line task was run so results can be reproduced later.

RECORDS
- start time and duration
- exact argument vector
- working directory
- exit code
- executable path
- tool version where available
- SHA-256 of stdout and stderr
- captured stdout and stderr
- non-secret environment summary

INSTALL
1. git clone https://github.com/Tinytim695/tracelock.git
2. cd tracelock
3. chmod +x tracelock
4. sudo install -m 0755 tracelock /usr/local/bin/tracelock

USAGE
tracelock -- nmap -sV 127.0.0.1
tracelock -- curl http://127.0.0.1:8080/
tracelock list
tracelock show RUN_ID

Privacy: records stay local under ~/.tracelock/. No telemetry or remote service.

Use only with commands and data you are authorised to run and retain.

License: MIT
