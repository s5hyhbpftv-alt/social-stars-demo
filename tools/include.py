#!/usr/bin/env python3
"""Вставляет общие блоки (шапка, заявка, подвал) во все страницы ai/.

Страницы — обычный статический HTML. Общие блоки лежат в tools/partials/*.html
и вставляются между маркерами:
    <!-- @header -->…<!-- /@header -->   <!-- @cta -->…<!-- /@cta -->   <!-- @footer -->…<!-- /@footer -->
Запуск из корня репозитория после правки партиалов:  python3 tools/include.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS = {p.stem: p.read_text(encoding="utf-8").strip() for p in (ROOT / "tools" / "partials").glob("*.html")}

for page in sorted((ROOT / "ai").rglob("index.html")):
    src = page.read_text(encoding="utf-8")
    out = src
    for name, body in PARTS.items():
        out = re.sub(rf"(<!-- @{name} -->).*?(<!-- /@{name} -->)", lambda m: f"{m.group(1)}\n{body}\n{m.group(2)}", out, flags=re.S)
    if out != src:
        page.write_text(out, encoding="utf-8")
        print("updated", page.relative_to(ROOT))
