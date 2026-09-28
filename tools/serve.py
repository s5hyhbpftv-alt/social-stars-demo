#!/usr/bin/env python3
"""Локальный сервер сайта — как на GitHub Pages: репозиторий доступен по адресу /social-stars-demo/.

Работает при любом имени папки и на любой ОС:  python3 tools/serve.py [--port 8123]
Откройте http://localhost:8123/social-stars-demo/ai/
"""
import argparse, http.server, os, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREFIX = '/social-stars-demo'


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def _route(self):
        path = urllib.parse.urlsplit(self.path).path
        if path in ('/', PREFIX):
            self.send_response(302); self.send_header('Location', PREFIX + '/ai/'); self.end_headers(); return False
        if not path.startswith(PREFIX + '/'):
            self.send_error(404); return False
        return True

    def translate_path(self, path):
        p = urllib.parse.urlsplit(path).path
        return super().translate_path(p[len(PREFIX):] if p.startswith(PREFIX + '/') else p)

    def do_GET(self):
        if self._route(): super().do_GET()

    def do_HEAD(self):
        if self._route(): super().do_HEAD()

    def log_message(self, *a):
        pass


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--port', type=int, default=int(os.environ.get('PORT', 8123)))
    port = ap.parse_args().port
    print(f'http://localhost:{port}{PREFIX}/ai/', flush=True)
    http.server.ThreadingHTTPServer(('127.0.0.1', port), Handler).serve_forever()
