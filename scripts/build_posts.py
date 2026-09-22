#!/usr/bin/env python
"""Build the static post index, including the public justinweon/TIL repository."""
from __future__ import annotations
import json
import re
import urllib.request
from urllib.parse import quote
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_ROOT = ROOT / 'posts'
OUT = ROOT / 'assets' / 'posts.json'
TIL_OWNER_REPO = 'justinweon/TIL'
BRANCH = 'main'


def request_json(url: str):
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


def request_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode('utf-8')


def clean_title(value: str) -> str:
    return re.sub(r'\s+', ' ', value.replace('_', ' ').replace('.md', '')).strip()


def excerpt(content: str) -> str:
    text = re.sub(r'^---[\s\S]*?---\s*', '', content).strip()
    text = re.sub(r'^#+\s+.*$', '', text, count=1, flags=re.M)
    text = re.sub(r'[`*_>#\[\]()|]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()[:110]


def frontmatter(content: str) -> dict:
    match = re.match(r'^---\s*\n([\s\S]*?)\n---\s*\n?', content)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip().strip('"\'')
    return result


def content_without_title(content: str) -> str:
    body = re.sub(r'^---[\s\S]*?---\s*', '', content)
    return re.sub(r'^\ufeff?\s*#\s+.+\r?\n+', '', body, count=1)


def local_posts() -> list[dict]:
    records = []
    # Keep the original `code` folder working, but surface it as AX Study.
    categories = {
        'daily': 'daily',
        'code': 'ax',
        'ax-study': 'ax',
        'ai-news': 'news',
        'projects': 'projects',
    }
    for directory_name, category in categories.items():
        directory = POSTS_ROOT / directory_name
        for path in sorted(directory.glob('*.md'), reverse=True) if directory.exists() else []:
            content = path.read_text(encoding='utf-8')
            meta = frontmatter(content)
            title_match = re.search(r'^#\s+(.+)$', content, re.M)
            title = meta.get('title') or (title_match.group(1) if title_match else clean_title(path.stem))
            records.append({'id': f'{directory_name}-{path.stem}', 'category': category, 'title': title, 'date': meta.get('date', ''), 'excerpt': meta.get('excerpt', '') or excerpt(content), 'content': content_without_title(content), 'source': ''})
    return records


def date_from_path(path: str) -> str:
    match = re.search(r'/(\d{2})(\d{2})_', path)
    if match:
        return f'{date.today().year}-{match.group(1)}-{match.group(2)}'
    match = re.search(r'/(\d{2})(\d{2})\.', path)
    if match:
        return f'{date.today().year}-{match.group(1)}-{match.group(2)}'
    return ''


def til_posts() -> list[dict]:
    tree = request_json(f'https://api.github.com/repos/{TIL_OWNER_REPO}/git/trees/{BRANCH}?recursive=1').get('tree', [])
    paths = [entry['path'] for entry in tree if entry.get('type') == 'blob' and entry['path'].endswith('.md') and entry['path'].lower() != 'readme.md']
    records = []
    for path in paths:
        raw_url = f'https://raw.githubusercontent.com/{TIL_OWNER_REPO}/{BRANCH}/{quote(path)}'
        content = request_text(raw_url)
        heading = re.search(r'^#\s+(.+)$', content, re.M)
        records.append({'id': 'til-' + re.sub(r'[^a-zA-Z0-9가-힣]+', '-', path).strip('-').lower(), 'category': 'til', 'title': heading.group(1).strip() if heading else clean_title(Path(path).stem), 'date': date_from_path(path), 'excerpt': excerpt(content), 'content': content_without_title(content), 'source': f'https://github.com/{TIL_OWNER_REPO}/blob/{BRANCH}/{path}'})
    return records


if __name__ == '__main__':
    posts = local_posts() + til_posts()
    posts.sort(key=lambda item: item['date'], reverse=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({'generated_at': date.today().isoformat(), 'posts': posts}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Built {len(posts)} posts ({sum(p["category"] == "til" for p in posts)} imported from TIL).')
