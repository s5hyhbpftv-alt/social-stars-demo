#!/usr/bin/env bash
# Первый запуск на своём компьютере (macOS, Linux) — одна команда в терминале:
#   curl -fsSL https://raw.githubusercontent.com/s5hyhbpftv-alt/social-stars-demo/main/tools/start-local.sh | bash
# Скачивает проект в ~/social-stars-demo (или обновляет), ставит Claude Code при необходимости и открывает сессию.
# Остальное (медиа из ~/Downloads/export, зависимости, локальный сервер) делает хук старта сессии.
set -e
DIR="${SS_DIR:-$HOME/social-stars-demo}"
REPO="https://github.com/s5hyhbpftv-alt/social-stars-demo.git"
need() { command -v "$1" >/dev/null 2>&1 || { echo "Сначала установите: $2"; exit 1; }; }
need git "Git — https://git-scm.com"
need node "Node.js 18 или новее — https://nodejs.org"
command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1 || { echo "Сначала установите: Python 3 — https://www.python.org"; exit 1; }
if ! command -v claude >/dev/null 2>&1; then
  echo "Устанавливаю Claude Code…"
  curl -fsSL https://claude.ai/install.sh | bash
  export PATH="$HOME/.local/bin:$PATH"
fi
if [ -d "$DIR/.git" ]; then
  git -C "$DIR" pull --ff-only -q || echo "Не удалось обновить (есть свои изменения) — продолжаю с текущей версией."
else
  git clone -q "$REPO" "$DIR"
fi
cd "$DIR"
echo "Проект: $DIR — открываю Claude Code…"
exec claude "Поехали" < /dev/tty
