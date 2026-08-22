"""docs/ 를 읽어 site.html 한 파일로 묶습니다.

목차는 **디렉터리 구조에서 그대로 뽑습니다.** 파일을 넣으면 사이트에 나오고,
지우면 사라집니다. 따로 등록할 곳이 없습니다.

  docs/README.md          → 최상단 "README"
  docs/reference/enums.md → "reference" 묶음 아래 "enums"

GitBook 이 읽는 docs/SUMMARY.md 도 같은 트리로 다시 씁니다. 손으로 관리하면
사이트와 어긋나므로 생성물로 둡니다.
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from md2html import convert

BOOK = Path(__file__).parent
DOCS = BOOK.parent / "docs"
OUT  = BOOK / "site.html"

# 문서가 아닌 파일. SUMMARY 는 이 스크립트가 만드는 생성물입니다.
SKIP = {"SUMMARY.md"}


def walk():
    """docs/ 를 훑어 (그룹 라벨, [(라벨, 페이지키)]) 목록을 만듭니다.

    최상위 파일이 먼저 오고 README 를 맨 앞에 둡니다. 그 뒤로 디렉터리를
    이름순으로 붙이되 `_` 로 시작하는 것(작업 노트 등)은 맨 뒤로 보냅니다.
    ASCII 순으로 두면 `_work` 가 `core` 앞에 와서 부록이 첫머리에 옵니다.
    """
    def label(p):
        return p.stem

    root_files = sorted((p for p in DOCS.glob("*.md") if p.name not in SKIP),
                        key=lambda p: (p.stem != "README", p.stem.lower()))
    sections = [(None, [(label(p), p.relative_to(DOCS).as_posix()[:-3]) for p in root_files])]

    dirs = sorted((d for d in DOCS.iterdir() if d.is_dir()),
                  key=lambda d: (d.name.startswith("_"), d.name.lower()))
    for d in dirs:
        files = sorted((p for p in d.rglob("*.md") if p.name not in SKIP),
                       key=lambda p: p.relative_to(d).as_posix().lower())
        if files:
            sections.append((d.name,
                             [(label(p), p.relative_to(DOCS).as_posix()[:-3]) for p in files]))
    return sections


sections = walk()

nav = []
for group, items in sections:
    if group:
        nav.append({"kind": "group", "label": group})
    for lbl, key in items:
        nav.append({"kind": "link", "depth": 0, "label": lbl, "page": key, "frag": ""})

# ── 페이지 변환 ──────────────────────────────────────────
MARKERS = "✅🟡⚠️❓🔵🔒🚨⭐🚫📌🔐💡📊📎"
MARKER_CLASS = {"✅": "ok", "🟡": "partial", "⚠️": "weak", "❓": "guess", "🔵": "post",
                "🔒": "auth", "🚨": "danger", "⭐": "star", "🚫": "dead"}


def decorate(h):
    """표 안의 상태 마커와 HTTP 메서드를 스캔 가능한 요소로 승격합니다."""
    def cell(m):
        tag, body = m.group(1), m.group(2)
        plain = re.sub(r'\s|️', '', body)
        if plain and all(c in MARKERS for c in plain):
            chips = "".join(
                f'<span class="chip chip-{MARKER_CLASS.get(c,"star")}" title="{c}">{c}</span>'
                for c in plain)
            return f'<{tag} class="cell-marker">{chips}</{tag}>'
        return m.group(0)
    h = re.sub(r'<(td|th)>(.*?)</\1>', cell, h, flags=re.S)
    h = re.sub(r'<code>(GET|POST|PUT|DELETE|WSS|WS)(\s|&)',
               lambda m: f'<code><span class="method m-{m.group(1).lower()}">{m.group(1)}</span>{m.group(2)}', h)
    return h


pages, index = {}, []
for item in nav:
    if item["kind"] != "link":
        continue
    key = item["page"]
    md = (DOCS / f"{key}.md").read_text(encoding="utf-8")
    body, headings = convert(md, key)
    title = next((t for l, a, t in headings if l == 1), key)
    pages[key] = {"title": title, "html": decorate(body),
                  "toc": [{"level": l, "id": a, "text": t} for l, a, t in headings if 2 <= l <= 3]}
    text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', body))
    index.append({"p": key, "t": title,
                  "h": [t for l, a, t in headings if l >= 2],
                  "b": text[:6000]})

tpl = (BOOK / "template.html").read_text(encoding="utf-8")
OUT.write_text(
    tpl.replace("__NAV__", json.dumps(nav, ensure_ascii=False))
       .replace("__PAGES__", json.dumps(pages, ensure_ascii=False))
       .replace("__INDEX__", json.dumps(index, ensure_ascii=False)),
    encoding="utf-8")

# ── SUMMARY.md 다시 쓰기 ─────────────────────────────────
# GitBook 은 이 파일로 목차를 만듭니다. 위 트리와 같은 내용을 써서
# 사이트와 GitBook 이 어긋나지 않게 합니다.
lines = ["# Table of contents", ""]
for group, items in sections:
    if group:
        lines += [f"## {group}", ""]
    lines += [f"* [{lbl}]({key}.md)" for lbl, key in items]
    lines.append("")
(DOCS / "SUMMARY.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

print(f"{OUT}  {OUT.stat().st_size/1024:.0f} KB  · 페이지 {len(pages)}개 · 목차 {len(nav)}행")
print(f"{DOCS / 'SUMMARY.md'} 갱신")
