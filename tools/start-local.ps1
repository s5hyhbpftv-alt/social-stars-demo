# Первый запуск на Windows — одна команда в PowerShell:
#   irm https://raw.githubusercontent.com/s5hyhbpftv-alt/social-stars-demo/main/tools/start-local.ps1 | iex
# Скачивает проект в %USERPROFILE%\social-stars-demo (или обновляет), ставит Claude Code при необходимости и открывает сессию.
# Остальное (медиа из Загрузки\export, зависимости, локальный сервер) делает хук старта сессии.
$Dir = if ($env:SS_DIR) { $env:SS_DIR } else { Join-Path $HOME 'social-stars-demo' }
$Repo = 'https://github.com/s5hyhbpftv-alt/social-stars-demo.git'
function Test-Cmd($c) { [bool](Get-Command $c -ErrorAction SilentlyContinue) }
if (-not (Test-Cmd git)) { throw 'Сначала установите Git для Windows — https://git-scm.com (он нужен и Claude Code)' }
if (-not (Test-Cmd node)) { throw 'Сначала установите Node.js 18 или новее — https://nodejs.org' }
if (-not ((Test-Cmd python) -or (Test-Cmd python3))) { throw 'Сначала установите Python 3 — https://www.python.org (отметьте «Add to PATH»)' }
if (-not (Test-Cmd claude)) {
  Write-Host 'Устанавливаю Claude Code…'
  Invoke-RestMethod https://claude.ai/install.ps1 | Invoke-Expression
  $env:Path = "$env:Path;$HOME\.local\bin"
}
if (Test-Path (Join-Path $Dir '.git')) { git -C $Dir pull --ff-only -q } else { git clone -q $Repo $Dir }
Set-Location $Dir
Write-Host "Проект: $Dir — открываю Claude Code…"
claude 'Поехали'
