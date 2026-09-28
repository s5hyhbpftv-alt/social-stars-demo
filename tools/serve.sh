#!/usr/bin/env bash
# Локальный сервер: http://localhost:${PORT:-8123}/social-stars-demo/ai/
cd "$(dirname "$0")/.." && exec "$(command -v python3 || command -v python)" tools/serve.py --port "${PORT:-8123}"
