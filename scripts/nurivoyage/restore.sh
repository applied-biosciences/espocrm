#!/usr/bin/env bash
set -euo pipefail
python3 scripts/nurivoyage/snapshot.py restore "$1"
