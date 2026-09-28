#!/usr/bin/env bash
# Готовит проект при старте каждой сессии Claude Code (хук SessionStart в .claude/settings.json).
# Всё, что скрипт печатает, Claude видит в начале сессии.
set -u
ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$ROOT" || exit 0
PORT="${PORT:-8123}"
URL="http://localhost:$PORT/social-stars-demo/ai/"
LOCAL=1; [ "${CLAUDE_CODE_REMOTE:-}" = "true" ] && LOCAL=0
mkdir -p tools/qa/out
echo "## Подготовка сессии (tools/session-start.sh)"

# 1. Свежая версия с GitHub — только локально и только если нет своих изменений
if [ $LOCAL = 1 ] && git rev-parse --git-dir >/dev/null 2>&1 && [ -z "$(git status --porcelain 2>/dev/null)" ]; then
  if git pull --ff-only -q >/dev/null 2>&1; then echo "- Код обновлён из GitHub (ветка $(git branch --show-current))."; fi
fi

# 2. Медиа из «Загрузок»: папка export → export/ в репозитории (в git не попадает)
if [ $LOCAL = 1 ] && { [ ! -d export ] || [ -z "$(ls -A export 2>/dev/null)" ]; }; then
  for d in "$HOME/Downloads/export" "$HOME/Загрузки/export" "$HOME/Desktop/export" "$HOME/Рабочий стол/export" "${USERPROFILE:-/nonexistent}/Downloads/export"; do
    if [ -d "$d" ] && [ -n "$(ls -A "$d" 2>/dev/null)" ]; then
      mkdir -p export && cp -R "$d"/. export/ && echo "- Медиа скопированы из «$d» в export/."
      break
    fi
  done
fi
if [ -d export ] && [ -n "$(ls -A export 2>/dev/null)" ]; then
  find export -type f ! -name '.*' | sort > tools/qa/out/export-list.txt
  n=$(wc -l < tools/qa/out/export-list.txt | tr -d ' ')
  img=$(grep -ciE '\.(jpe?g|png|webp|heic|gif)$' tools/qa/out/export-list.txt)
  vid=$(grep -ciE '\.(mp4|mov|webm|m4v)$' tools/qa/out/export-list.txt)
  echo "- В export/ файлов: $n (фото: $img, видео: $vid). Полный список — tools/qa/out/export-list.txt. Первые файлы:"
  head -40 tools/qa/out/export-list.txt | sed 's/^/    /'
else
  echo "- Папки export/ нет: медиа не найдены в ~/Downloads/export (или ~/Загрузки/export). Попросите пользователя положить туда файлы или перетащить их в чат."
fi

# 3. Зависимости проверок и браузер
if [ ! -d tools/qa/node_modules/playwright ]; then
  if command -v npm >/dev/null 2>&1 && (cd tools/qa && npm install --silent --no-audit --no-fund >/dev/null 2>&1); then
    echo "- Установлены зависимости проверок (tools/qa)."
  else
    echo "- Не удалось установить зависимости tools/qa: нужен Node.js 18+ (https://nodejs.org)."
  fi
fi
if [ $LOCAL = 1 ] && [ -d tools/qa/node_modules/playwright ] && [ ! -f tools/qa/out/.chromium-ok ]; then
  (cd tools/qa && nohup sh -c 'npx playwright install chromium > out/playwright-install.log 2>&1 && touch out/.chromium-ok' >/dev/null 2>&1 &)
  echo "- Браузер для проверок устанавливается в фоне, 1–3 минуты (tools/qa/out/playwright-install.log)."
fi

# 4. Локальный сервер
up() { curl -s -o /dev/null -w '%{http_code}' "$URL" 2>/dev/null | grep -q 200; }
if up; then
  echo "- Сайт уже открыт: $URL"
else
  PY="$(command -v python3 || command -v python || true)"
  if [ -n "$PY" ]; then
    nohup "$PY" tools/serve.py --port "$PORT" > tools/qa/out/server.log 2>&1 &
    for _ in 1 2 3 4 5 6; do up && break; sleep .5; done
    if up; then echo "- Запущен локальный сервер: $URL"; else echo "- Сервер не поднялся, см. tools/qa/out/server.log"; fi
  else
    echo "- Нет Python 3 — локальный сервер не запущен (https://www.python.org)."
  fi
fi

echo "- Дальше: раздел «Старт новой сессии» и «Открытые задачи» в CLAUDE.md."
exit 0
