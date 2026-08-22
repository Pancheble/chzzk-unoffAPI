"""문서 트리의 상대링크·앵커를 검사합니다. 인자 없으면 전체."""
import json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "docs"   # 문서 루트
SITE = Path(__file__).resolve().parent / "site.html"

def slug(h):
    h = h.strip().lower()
    h = re.sub(r'`([^`]*)`', r'\1', h)          # 코드 마크업 제거
    h = re.sub(r'\*\*?([^*]*)\*\*?', r'\1', h)  # 굵게/기울임 제거
    out = []
    for ch in h:
        if ch.isalnum() or ch in "_-" or ord(ch) > 0x7F and unicodedata.category(ch)[0] in "LN":
            out.append(ch)
        elif ch in " \t":
            out.append("-")
        # 그 외 문장부호는 버립니다 (GitHub 규칙)
    return "".join(out)

headings = {}   # path -> set of anchors
for f in ROOT.rglob("*.md"):
    hs = set()
    for line in f.read_text(encoding="utf-8").splitlines():
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            s = slug(m.group(2))
            n, base = 0, s
            while s in hs:
                n += 1; s = f"{base}-{n}"
            hs.add(s)
    headings[f.resolve()] = hs

targets = [ROOT / a for a in sys.argv[1:]] if len(sys.argv) > 1 else sorted(ROOT.rglob("*.md"))
bad = 0
for f in targets:
    text = f.read_text(encoding="utf-8")
    for m in re.finditer(r'\[([^\]]*)\]\(([^)\s]+)\)', text):
        label, href = m.group(1), m.group(2)
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        path, _, frag = href.partition("#")
        tgt = (f.parent / path).resolve() if path else f.resolve()
        rel = f.relative_to(ROOT)
        if not tgt.exists():
            print(f"  파일없음  {rel}: [{label}]({href})"); bad += 1
        elif frag and frag not in headings.get(tgt, set()):
            print(f"  앵커없음  {rel}: [{label}]({href})"); bad += 1
print(f"\n마크다운 — 검사 {len(targets)}개 파일 · 깨짐 {bad}건")


def check_site():
    """생성물의 href 를 페이지 키와 대조합니다.

    위 검사는 마크다운 원본만 봅니다. 변환 과정에서 href 가 깨지면 원본이
    멀쩡해도 사이트에서는 링크가 죽습니다 — 실제로 `.md` 가 안 떨어져 모든
    문서 간 링크가 첫 페이지로 가던 적이 있고, 원본 검사로는 못 잡았습니다.
    """
    site = SITE
    if not site.exists():
        print("site.html 이 없습니다. build.py 를 먼저 실행합니다.")
        return 0

    html = site.read_text(encoding="utf-8")
    dec = json.JSONDecoder()
    pages = dec.raw_decode(html[html.index("{", html.index("PAGES")):])[0]
    nav = dec.raw_decode(html[html.index("[", html.index("NAV")):])[0]

    n, seen = 0, set()
    # 변환된 문서 HTML 안의 링크만 봅니다. site.html 전체를 훑으면
    # 템플릿 JS 의 문자열(`'#/'+page+...`)까지 걸립니다.
    for src, doc in pages.items():
        for m in re.finditer(r'href="#/([^"@]*)(?:@([^"]*))?"', doc["html"]):
            key = (src, m.group(1), m.group(2))
            if key in seen:
                continue
            seen.add(key)
            page, frag = m.group(1), m.group(2)
            if page not in pages:
                print(f"  없는 페이지  {src} → #/{page}"); n += 1
            elif frag and f'id="{frag}"' not in pages[page]["html"]:
                print(f"  없는 앵커    {src} → #/{page}@{frag}"); n += 1

    for item in nav:
        if item["kind"] == "link" and item["page"] not in pages:
            print(f"  목차가 없는 페이지를 가리킴  {item['page']}"); n += 1

    print(f"site.html — 링크 {len(seen)}종 · 깨짐 {n}건")
    return n


bad += check_site()
sys.exit(1 if bad else 0)
