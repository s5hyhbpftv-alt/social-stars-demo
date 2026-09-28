#!/usr/bin/env bash
# Локальный сервер: сайт живёт под /social-stars-demo/, поэтому отдаём папку уровнем выше.
# Папка репозитория должна называться social-stars-demo. Откройте http://localhost:${PORT:-8123}/social-stars-demo/ai/
set -e
cd "$(dirname "$0")/../.."
[ -d social-stars-demo ] || { echo "Папка репозитория должна называться social-stars-demo"; exit 1; }
echo "http://localhost:${PORT:-8123}/social-stars-demo/ai/"
python3 -m http.server "${PORT:-8123}"
