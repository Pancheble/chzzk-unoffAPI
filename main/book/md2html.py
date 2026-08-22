"""chzzkAPI_docs 전용 마크다운 변환기.

이 문서가 쓰는 문법만 다룹니다: 제목·표·코드펜스·인용·목록·hr·인라인·raw HTML.
범용 변환기가 아니라 이 저장소에 맞춘 것입니다.
"""
import html, re, unicodedata

def slug(h):
    h = re.sub(r'`([^`]*)`', r'\1', h.strip().lower())
    h = re.sub(r'\*\*?([^*]*)\*\*?', r'\1', h)
    h = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', h)
    out = []
    for ch in h:
        if ch.isalnum() or ch in "_-" or (ord(ch) > 0x7F and unicodedata.category(ch)[0] in "LN"):
            out.append(ch)
        elif ch in " \t":
            out.append("-")
    return "".join(out)

INLINE_CODE = re.compile(r'`([^`]+)`')
BOLD        = re.compile(r'\*\*([^*]+)\*\*')
STRIKE      = re.compile(r'~~([^~]+)~~')
LINK        = re.compile(r'\[([^\]]*)\]\(([^)\s]+)\)')

def inline(s, page):
    """인라인 서식. 코드 조각은 먼저 빼두고 나머지를 처리합니다."""
    stash = []
    def keep(m):
        stash.append(f'<code>{html.escape(m.group(1))}</code>')
        return f"\x00{len(stash)-1}\x00"
    s = INLINE_CODE.sub(keep, s)
    s = html.escape(s)
    s = BOLD.sub(r'<strong>\1</strong>', s)
    s = STRIKE.sub(r'<del>\1</del>', s)

    def link(m):
        label, href = m.group(1), m.group(2)
        if href.startswith(("http://", "https://", "mailto:")):
            return f'<a href="{href}" target="_blank" rel="noopener">{label}</a>'
        path, _, frag = href.partition("#")
        # 페이지 키에는 확장자가 없습니다 (build.py). 떼지 않으면 라우터가
        # 페이지를 못 찾아 전부 첫 페이지로 떨어집니다.
        if path.endswith(".md"):
            path = path[:-3]
        target = resolve(page, path) if path else page
        return f'<a href="#/{target}{"@" + frag if frag else ""}" data-nav>{label}</a>'
    s = LINK.sub(link, s)
    return re.sub(r'\x00(\d+)\x00', lambda m: stash[int(m.group(1))], s)

def resolve(page, rel):
    """페이지 기준 상대경로를 저장소 루트 기준으로 바꿉니다."""
    parts = page.split("/")[:-1]
    for seg in rel.split("/"):
        if seg == "..":
            if parts: parts.pop()
        elif seg not in (".", ""):
            parts.append(seg)
    return "/".join(parts)

def cells(row):
    row = row.strip()
    if row.startswith("|"): row = row[1:]
    if row.endswith("|"):   row = row[:-1]
    # \| 는 구분자가 아닙니다
    out, cur, i = [], "", 0
    while i < len(row):
        if row[i] == "\\" and i + 1 < len(row):
            cur += row[i+1]; i += 2
        elif row[i] == "|":
            out.append(cur); cur = ""; i += 1
        else:
            cur += row[i]; i += 1
    out.append(cur)
    return [c.strip() for c in out]

RAW_HTML = ("<details", "</details", "<summary", "</summary", "<!--")

def convert(md, page):
    lines = md.split("\n")
    out, i, headings = [], 0, []

    while i < len(lines):
        ln = lines[i]

        # 코드 펜스
        if ln.startswith("```"):
            lang = ln[3:].strip()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            cls = f' class="lang-{html.escape(lang)}"' if lang else ""
            body = html.escape("\n".join(buf))
            label = f'<span class="code-lang">{html.escape(lang)}</span>' if lang else ""
            out.append(f'<div class="code">{label}<pre><code{cls}>{body}</code></pre></div>')
            continue

        # raw HTML 통과
        if ln.strip().startswith(RAW_HTML):
            out.append(ln); i += 1; continue

        # 제목
        m = re.match(r'^(#{1,6})\s+(.*)$', ln)
        if m:
            lvl, txt = len(m.group(1)), m.group(2)
            a = slug(txt)
            base, n = a, 0
            while any(h[1] == a for h in headings):
                n += 1; a = f"{base}-{n}"
            headings.append((lvl, a, re.sub(r'<[^>]+>', '', inline(txt, page))))
            out.append(f'<h{lvl} id="{a}">{inline(txt, page)}'
                       f'<a class="anchor" href="#/{page}@{a}" data-nav aria-label="이 절 링크">#</a></h{lvl}>')
            i += 1; continue

        # 표
        if ln.startswith("|") and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|?\s*$', lines[i+1]):
            head = cells(ln); i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(cells(lines[i])); i += 1
            th = "".join(f'<th>{inline(c, page)}</th>' for c in head)
            tb = ""
            for r in rows:
                r += [""] * (len(head) - len(r))
                tb += "<tr>" + "".join(f'<td>{inline(c, page)}</td>' for c in r[:len(head)]) + "</tr>"
            empty = ' class="th-empty"' if not any(c.strip() for c in head) else ""
            out.append(f'<div class="table-wrap"><table><thead{empty}><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>')
            continue

        # 인용 (안에 제목·표가 들어옵니다 — 재귀)
        if ln.startswith(">"):
            buf = []
            while i < len(lines) and (lines[i].startswith(">") or
                                      (lines[i].strip() == "" and i+1 < len(lines) and lines[i+1].startswith(">"))):
                buf.append(re.sub(r'^>\s?', '', lines[i])); i += 1
            inner, _ = convert("\n".join(buf), page)
            out.append(f'<blockquote>{inner}</blockquote>')
            continue

        # 목록
        if re.match(r'^\s*[-*]\s+', ln) or re.match(r'^\s*\d+\.\s+', ln):
            ordered = bool(re.match(r'^\s*\d+\.\s+', ln))
            items, base_indent = [], len(ln) - len(ln.lstrip())
            while i < len(lines):
                cur = lines[i]
                m2 = re.match(r'^(\s*)(?:[-*]|\d+\.)\s+(.*)$', cur)
                if m2 and len(m2.group(1)) >= base_indent:
                    items.append(m2.group(2)); i += 1
                elif cur.strip() and not cur.startswith(("|", "#", "```", ">")) and (len(cur) - len(cur.lstrip())) > base_indent:
                    if items: items[-1] += " " + cur.strip()
                    i += 1
                else:
                    break
            tag = "ol" if ordered else "ul"
            li = "".join(f'<li>{inline(x, page)}</li>' for x in items)
            out.append(f'<{tag}>{li}</{tag}>')
            continue

        if re.match(r'^(?:-{3,}|\*{3,})\s*$', ln):
            out.append("<hr>"); i += 1; continue

        if not ln.strip():
            i += 1; continue

        # 문단 (연속 줄은 한 문단)
        buf = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("|", "#", "```", ">", "---", "***")) \
              and not re.match(r'^\s*(?:[-*]|\d+\.)\s+', lines[i]) and not lines[i].strip().startswith(RAW_HTML):
            buf.append(lines[i]); i += 1
        if buf:
            # 줄 끝 백슬래시는 강제 줄바꿈입니다 (GitBook 문법).
            # 공식 문서가 한 문단 안에서 문장을 줄로 나눌 때 씁니다.
            # inline() 이 HTML 을 이스케이프하므로 <br> 을 미리 넣으면 글자로
            # 나옵니다. 센티널로 통과시킨 뒤 마지막에 태그로 바꿉니다.
            joined = "\n".join(buf)
            joined = re.sub(r'\\\s*\n', '\x01', joined).replace("\n", " ")
            out.append(f'<p>{inline(joined, page).replace(chr(1), "<br>")}</p>')

    return "\n".join(out), headings
