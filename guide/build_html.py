#!/usr/bin/env python3
"""
Build guide/study-guide.html -- a single self-contained page holding the whole guide.

Why a build script rather than a hand-written page: the Markdown day files are the
source of truth. Edit those, re-run this, and the HTML follows. Nothing to keep in sync.

What it produces:
  * one file, no network needed -- syntax highlighting is done here, not by a CDN script
  * code and its numbered annotations side by side on a wide screen, stacked on a phone
  * a sticky sidebar of all 7 days and 70 problems, with live filtering
  * light/dark following the reader's system theme
  * print rules, so Ctrl/Cmd-P -> Save as PDF gives a clean printed guide

Usage:  pip install markdown && python3 guide/build_html.py
"""

import html
import os
import re
import sys

try:
    import markdown
except ImportError:
    sys.exit("This script needs the `markdown` package:  pip install markdown")

HERE = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    ("how-to", "How to Use This Guide", "00-how-to-use.md"),
    ("python", "Python for DSA", "01-python-for-dsa.md"),
    ("complexity", "Complexity", "02-complexity.md"),
    ("patterns", "Pattern Cheat Sheet", "03-pattern-cheatsheet.md"),
    ("bugs", "Bugs Found in the Original Code", "bugs-found.md"),
    ("day1", "Day 1 — Hashing, Sets & Bit Tricks", "day-1-hashing.md"),
    ("day2", "Day 2 — Two Pointers, Sliding Window & Prefix Sums", "day-2-two-pointers-sliding-window.md"),
    ("day3", "Day 3 — Binary Search & Heaps", "day-3-binary-search-heaps.md"),
    ("day4", "Day 4 — Stacks, Queues & Monotonic Stack", "day-4-stacks-queues.md"),
    ("day5", "Day 5 — Linked Lists", "day-5-linked-lists.md"),
    ("day6", "Day 6 — Binary Trees", "day-6-trees.md"),
    ("day7", "Day 7 — BST, Graphs, Backtracking & DP", "day-7-bst-graphs-backtracking-dp.md"),
]


# ----------------------------------------------------------------------------------
# Python syntax highlighting, done here so the page needs no external script
# ----------------------------------------------------------------------------------
KEYWORDS = (
    "def class return if elif else for while in not and or import from None True False "
    "is lambda break continue pass yield with as try except finally raise global nonlocal "
    "del assert async await"
).split()

BUILTINS = (
    "len range max min sum sorted set dict list tuple int str float bool abs enumerate zip "
    "print append pop popleft appendleft add remove discard heappush heappop heapify "
    "heappushpop nlargest nsmallest deque Counter defaultdict isalpha isdigit lower upper "
    "join sort reverse get items values keys ord chr all any reversed bit_length ceil "
    "setdefault extend insert index count copy"
).split()

TOKEN_RE = re.compile(
    r"(?P<entity>&(?:[a-zA-Z]+|#\d+);)"
    r"|(?P<comment>\#[^\n]*)"
    r"|(?P<string>\"(?:[^\"\\\n]|\\.)*\"|'(?:[^'\\\n]|\\.)*')"
    r"|(?P<number>\b\d+\.?\d*\b)"
    r"|(?P<word>\b[A-Za-z_][A-Za-z_0-9]*\b)"
)


def highlight_python(escaped_source):
    """Wrap tokens in spans. Input is already HTML-escaped, so entities pass through."""
    out = []
    pos = 0
    for m in TOKEN_RE.finditer(escaped_source):
        out.append(escaped_source[pos:m.start()])
        pos = m.end()
        kind = m.lastgroup
        text = m.group()
        if kind == "entity":
            out.append(text)
        elif kind == "comment":
            out.append(f'<span class="tok-c">{text}</span>')
        elif kind == "string":
            out.append(f'<span class="tok-s">{text}</span>')
        elif kind == "number":
            out.append(f'<span class="tok-n">{text}</span>')
        else:
            if text in KEYWORDS:
                out.append(f'<span class="tok-k">{text}</span>')
            elif text in BUILTINS:
                out.append(f'<span class="tok-b">{text}</span>')
            elif text == "self":
                out.append(f'<span class="tok-self">{text}</span>')
            else:
                out.append(text)
    out.append(escaped_source[pos:])
    return "".join(out)


CODE_BLOCK_RE = re.compile(
    r'<pre><code class="language-(?P<lang>\w+)">(?P<body>.*?)</code></pre>', re.S
)


def apply_highlighting(html_text):
    def repl(m):
        body = m.group("body")
        if m.group("lang") == "python":
            body = highlight_python(body)
        return f'<pre class="code"><code>{body}</code></pre>'
    html_text = CODE_BLOCK_RE.sub(repl, html_text)
    # fenced blocks with no language, and indented blocks
    html_text = html_text.replace("<pre><code>", '<pre class="code plain"><code>')
    return html_text


# ----------------------------------------------------------------------------------
# Side-by-side: a code block followed by its numbered annotations
# ----------------------------------------------------------------------------------
# After conversion a "The code" section looks like:
#     <pre class="code">...</pre>
#     <p><strong>(1)</strong> why this line ...</p>
#     <p><strong>(2)</strong> ...</p>
# Those runs become two columns: code on the left (sticky), notes on the right.
# The inner patterns are "tempered" -- (?:(?!END).)* -- so a code block can never swallow
# the prose and tables that follow it while the regex engine backtracks looking for a match.
# Without that, a plain <pre> earlier in the section absorbs everything up to the real one.
# An annotation may be followed by a bullet list, so one <ul>/<ol> is allowed to sit
# between consecutive numbered notes without ending the run.
ANNOTATED_RE = re.compile(
    r'(?P<pre><pre class="code[^"]*"><code>(?:(?!</code></pre>).)*</code></pre>)\s*'
    r'(?P<notes>(?:<p><strong>\(\d+\)[^<]*</strong>(?:(?!</p>).)*</p>\s*'
    r'(?:<[uo]l>(?:(?!</[uo]l>).)*</[uo]l>\s*)?)+)',
    re.S,
)


def split_annotated_blocks(html_text):
    def repl(m):
        return (
            '<div class="split">'
            f'<div class="split-code">{m.group("pre")}</div>'
            f'<div class="split-notes">{m.group("notes")}</div>'
            "</div>"
        )
    return ANNOTATED_RE.sub(repl, html_text)


# ----------------------------------------------------------------------------------
# Rewrite the inter-file links so everything works inside one page
# ----------------------------------------------------------------------------------
FILE_TO_ANCHOR = {src: pid for pid, _title, src in PAGES}


def rewrite_links(html_text, page_id):
    # ./day-3-binary-search-heaps.md          -> #day3
    # ./01-python-for-dsa.md#anything         -> #python
    def md_link(m):
        target = m.group("file")
        anchor = FILE_TO_ANCHOR.get(target)
        return f'href="#{anchor}"' if anchor else m.group(0)

    html_text = re.sub(r'href="\./(?P<file>[\w\-.]+\.md)(?:#[^"]*)?"', md_link, html_text)
    # ../04-Two_sum.py -> point at the file on GitHub-relative path from guide/
    html_text = re.sub(r'href="\.\./([\w\-.]+\.py)"',
                       r'href="../\1" class="src-link"', html_text)
    html_text = re.sub(r'href="\./(verify\.py)"', r'href="./\1" class="src-link"', html_text)
    # external links open in a new tab
    html_text = re.sub(r'<a href="(https?://[^"]+)"',
                       r'<a target="_blank" rel="noopener" href="\1"', html_text)
    return html_text


# ----------------------------------------------------------------------------------
def slugify(text, seen):
    s = re.sub(r"<[^>]+>", "", text)
    s = html.unescape(s)
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    base, i = s, 2
    while s in seen:
        s, i = f"{base}-{i}", i + 1
    seen.add(s)
    return s


def build():
    md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list", "md_in_html"])

    sections, nav = [], []
    seen_slugs = set()

    for page_id, title, filename in PAGES:
        path = os.path.join(HERE, filename)
        with open(path) as fh:
            text = fh.read()

        md.reset()
        body = md.convert(text)
        body = apply_highlighting(body)
        body = split_annotated_blocks(body)
        body = rewrite_links(body, page_id)

        # The first <h1> becomes the section heading; drop it from the body.
        body = re.sub(r"^\s*<h1>.*?</h1>", "", body, count=1, flags=re.S)

        # Give every problem heading an id, and collect them for the sidebar.
        subnav = []

        def tag_h2(m):
            inner = m.group(1)
            slug = slugify(inner, seen_slugs)
            plain = re.sub(r"<[^>]+>", "", inner)
            subnav.append((slug, html.unescape(plain)))
            return f'<h2 id="{slug}">{inner}</h2>'

        body = re.sub(r"<h2>(.*?)</h2>", tag_h2, body, flags=re.S)

        sections.append(
            f'<section class="page" id="{page_id}">'
            f'<h1 class="page-title">{html.escape(title)}</h1>{body}</section>'
        )
        nav.append((page_id, title, subnav))

    nav_html = []
    for page_id, title, subnav in nav:
        items = "".join(
            f'<li><a href="#{slug}" data-search="{html.escape(label.lower())}">'
            f"{html.escape(label)}</a></li>"
            for slug, label in subnav
        )
        nav_html.append(
            f'<li class="nav-group"><a class="nav-top" href="#{page_id}" '
            f'data-search="{html.escape(title.lower())}">{html.escape(title)}</a>'
            f"<ul>{items}</ul></li>"
        )

    out = TEMPLATE.replace("{{NAV}}", "\n".join(nav_html)).replace(
        "{{CONTENT}}", "\n".join(sections)
    )

    dest = os.path.join(HERE, "study-guide.html")
    with open(dest, "w") as fh:
        fh.write(out)

    kb = len(out.encode()) / 1024
    problems = sum(1 for _, _, sub in nav for s, l in sub if re.match(r"^\d+\.", l))
    print(f"wrote {dest}  ({kb:.0f} KB, {problems} problem sections)")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DSA in 7 Days — 70 Problems, Pattern by Pattern</title>
<style>
:root{
  --bg:#fbfbfa; --surface:#fff; --border:#e3e1dc; --border-soft:#eeece7;
  --text:#232220; --muted:#6c6862; --accent:#9a4a1f; --accent-soft:#f5ece5;
  --code-bg:#f6f4f0; --warn-bg:#fdf4ea; --warn-border:#e0a35c;
  --tok-k:#9a4a1f; --tok-s:#3f6b4a; --tok-c:#8c877f; --tok-n:#7a4b86; --tok-b:#2b5b86;
  --mono:ui-monospace,"SF Mono",SFMono-Regular,"Cascadia Mono","Roboto Mono",Menlo,Consolas,monospace;
  --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#16151a; --surface:#1d1c22; --border:#34323b; --border-soft:#2a292f;
    --text:#e6e3dd; --muted:#9d988f; --accent:#e39a6a; --accent-soft:#2c2119;
    --code-bg:#111015; --warn-bg:#2a2014; --warn-border:#a9723a;
    --tok-k:#e39a6a; --tok-s:#8fbf9a; --tok-c:#726d66; --tok-n:#c49ad4; --tok-b:#7fb2dd;
  }
}
:root[data-theme="dark"]{
  --bg:#16151a; --surface:#1d1c22; --border:#34323b; --border-soft:#2a292f;
  --text:#e6e3dd; --muted:#9d988f; --accent:#e39a6a; --accent-soft:#2c2119;
  --code-bg:#111015; --warn-bg:#2a2014; --warn-border:#a9723a;
  --tok-k:#e39a6a; --tok-s:#8fbf9a; --tok-c:#726d66; --tok-n:#c49ad4; --tok-b:#7fb2dd;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.65 var(--sans);
     -webkit-text-size-adjust:100%}
.layout{display:grid;grid-template-columns:300px minmax(0,1fr);gap:0;max-width:1500px;margin:0 auto}

/* ---------- sidebar ---------- */
aside{position:sticky;top:0;height:100vh;overflow-y:auto;padding:22px 14px 60px 20px;
      border-right:1px solid var(--border);background:var(--surface)}
aside h2{font-size:15px;margin:0 0 4px;letter-spacing:-.01em}
aside .sub{font-size:12px;color:var(--muted);margin:0 0 14px}
#q{width:100%;padding:7px 10px;border:1px solid var(--border);border-radius:7px;
   background:var(--bg);color:var(--text);font:13px var(--sans);margin-bottom:14px}
#q:focus{outline:2px solid var(--accent);outline-offset:-1px}
aside ul{list-style:none;margin:0;padding:0}
aside .nav-group>ul{margin:2px 0 12px 0}
aside a{display:block;text-decoration:none;color:var(--muted);padding:3px 8px;
        border-radius:5px;font-size:13px;line-height:1.4}
aside a:hover{background:var(--accent-soft);color:var(--text)}
aside a.nav-top{color:var(--text);font-weight:620;font-size:13.5px;margin-top:6px}
aside a.active{background:var(--accent-soft);color:var(--accent);font-weight:600}
aside li a{padding-left:14px}
aside li a.nav-top{padding-left:8px}
#theme{position:absolute;top:20px;right:16px;border:1px solid var(--border);
       background:var(--bg);color:var(--muted);border-radius:6px;cursor:pointer;
       font-size:14px;width:28px;height:28px;line-height:1}
#theme:hover{color:var(--text);border-color:var(--accent)}

/* ---------- content ---------- */
main{padding:34px 40px 120px;min-width:0;overflow-wrap:break-word}
main a{overflow-wrap:anywhere}
.page{max-width:1180px}
.page+.page{margin-top:60px;padding-top:34px;border-top:2px solid var(--border)}
.page-title{font-size:27px;line-height:1.25;letter-spacing:-.02em;margin:0 0 22px;
            padding-bottom:12px;border-bottom:1px solid var(--border)}
h2{font-size:21px;letter-spacing:-.015em;margin:44px 0 12px;scroll-margin-top:16px}
h3{font-size:15.5px;margin:26px 0 8px;color:var(--accent);letter-spacing:.01em}
h4{font-size:14px;margin:18px 0 6px}
p{margin:11px 0;max-width:74ch}
ul,ol{max-width:74ch;padding-left:22px}
li{margin:5px 0}
a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:2px}
hr{border:0;border-top:1px solid var(--border-soft);margin:34px 0}
strong{font-weight:640}
blockquote{margin:18px 0;padding:12px 18px;border-left:3px solid var(--accent);
           background:var(--accent-soft);border-radius:0 7px 7px 0;max-width:74ch}
blockquote p{margin:6px 0}
blockquote p:first-child{margin-top:0} blockquote p:last-child{margin-bottom:0}

/* ---------- code ---------- */
code{font-family:var(--mono);font-size:.875em;background:var(--code-bg);
     padding:1.5px 5px;border-radius:4px;border:1px solid var(--border-soft)}
pre.code{background:var(--code-bg);border:1px solid var(--border);border-radius:9px;
         padding:14px 16px;overflow-x:auto;margin:14px 0;font-size:13px;line-height:1.6}
pre.code code{background:none;border:0;padding:0;font-size:inherit}
.tok-k{color:var(--tok-k);font-weight:600}
.tok-s{color:var(--tok-s)}
.tok-c{color:var(--tok-c);font-style:italic}
.tok-n{color:var(--tok-n)}
.tok-b{color:var(--tok-b)}
.tok-self{color:var(--tok-n);font-style:italic}

/* ---------- the side-by-side pane ---------- */
.split{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);
       gap:20px;margin:16px 0;align-items:start}
.split-code,.split-notes{min-width:0}
.split-code{position:sticky;top:16px}
.split-code pre.code{margin:0}
.split-notes{font-size:14.5px}
.split-notes p{margin:0 0 11px;max-width:none}
.split-notes p:first-child{margin-top:0}
.split-notes>p{padding-left:12px;border-left:2px solid var(--border-soft)}
.split-notes>p:hover{border-left-color:var(--accent)}

/* ---------- tables ---------- */
.tablewrap{overflow-x:auto;margin:14px 0}
table{border-collapse:collapse;font-size:13.5px;min-width:100%}
th,td{border:1px solid var(--border);padding:6px 11px;text-align:left;vertical-align:top}
th{background:var(--code-bg);font-weight:640;white-space:nowrap}
td code,th code{font-size:.9em}

details{margin:18px 0;border:1px solid var(--border);border-radius:9px;
        padding:12px 16px;background:var(--surface)}
summary{cursor:pointer;font-weight:640;color:var(--accent)}
details[open] summary{margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid var(--border-soft)}

/* ---------- responsive ---------- */
@media (max-width:1080px){
  .split{grid-template-columns:minmax(0,1fr)}
  .split-code{position:static}
  .split-notes>p{border-left:2px solid var(--accent-soft)}
}
@media (max-width:860px){
  .layout{grid-template-columns:minmax(0,1fr)}
  aside{position:static;height:auto;max-height:none;border-right:0;
        border-bottom:1px solid var(--border)}
  aside .nav-group>ul{display:none}
  main{padding:22px 18px 80px}
  .page-title{font-size:22px}
  h2{font-size:18px}
}

/* ---------- print / save-as-PDF ---------- */
@media print{
  :root{--bg:#fff;--surface:#fff;--code-bg:#f6f6f4;--text:#000;--muted:#444;
        --border:#bbb;--border-soft:#ddd;--accent:#8a3d14;--accent-soft:#f7f2ed;
        --tok-k:#8a3d14;--tok-s:#2f5c3a;--tok-c:#666;--tok-n:#5c3a68;--tok-b:#1e4666}
  aside,#theme,#q{display:none!important}
  .layout{display:block;max-width:none}
  main{padding:0}
  .page{max-width:none;page-break-before:always}
  .page:first-of-type{page-break-before:auto}
  h2{page-break-after:avoid;page-break-before:auto}
  h3,h4{page-break-after:avoid}
  pre.code,table,blockquote{page-break-inside:avoid}
  .split{grid-template-columns:minmax(0,1fr)}
  .split-code{position:static}
  details{page-break-inside:avoid}
  details>*{display:revert!important}
  a{color:#000;text-decoration:none}
  a[href^="http"]::after{content:" (" attr(href) ")";font-size:9px;color:#666;
                          word-break:break-all}
  aside a::after,.nav-top::after{content:""}
  @page{margin:16mm 14mm}
}
</style>
</head>
<body>
<div class="layout">
<aside>
  <button id="theme" title="Toggle light / dark">◐</button>
  <h2>DSA in 7 Days</h2>
  <p class="sub">70 problems, pattern by pattern</p>
  <input id="q" type="search" placeholder="Filter problems…" autocomplete="off">
  <ul id="nav">
{{NAV}}
  </ul>
</aside>
<main>
{{CONTENT}}
</main>
</div>

<script>
(function () {
  "use strict";

  // Tables need their own scroll container so the page body never scrolls sideways.
  document.querySelectorAll("main table").forEach(function (t) {
    if (t.parentElement.classList.contains("tablewrap")) return;
    var w = document.createElement("div");
    w.className = "tablewrap";
    t.parentNode.insertBefore(w, t);
    w.appendChild(t);
  });

  // Theme toggle. localStorage can throw in a private window or on file:// in some
  // browsers, so every access is guarded and the page renders fine without it.
  var root = document.documentElement;
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }

  var saved = load("dsa-theme");
  if (saved) root.setAttribute("data-theme", saved);

  document.getElementById("theme").addEventListener("click", function () {
    var dark = root.getAttribute("data-theme") === "dark" ||
      (!root.getAttribute("data-theme") &&
        window.matchMedia("(prefers-color-scheme: dark)").matches);
    var next = dark ? "light" : "dark";
    root.setAttribute("data-theme", next);
    store("dsa-theme", next);
  });

  // Sidebar filter.
  var q = document.getElementById("q");
  var links = Array.prototype.slice.call(document.querySelectorAll("#nav a"));
  q.addEventListener("input", function () {
    var term = q.value.trim().toLowerCase();
    links.forEach(function (a) {
      var hit = !term || (a.dataset.search || "").indexOf(term) !== -1;
      a.style.display = hit ? "" : "none";
    });
    document.querySelectorAll("#nav .nav-group").forEach(function (g) {
      var any = Array.prototype.some.call(g.querySelectorAll("a"), function (a) {
        return a.style.display !== "none";
      });
      g.style.display = any ? "" : "none";
    });
  });
  q.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { q.value = ""; q.dispatchEvent(new Event("input")); }
  });

  // Highlight the heading currently in view.
  var heads = Array.prototype.slice.call(document.querySelectorAll("main h2[id], section.page[id]"));
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });

  if ("IntersectionObserver" in window) {
    var current = null;
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var a = byId[en.target.id];
        if (!a || a === current) return;
        if (current) current.classList.remove("active");
        a.classList.add("active");
        current = a;
      });
    }, { rootMargin: "0px 0px -75% 0px", threshold: 0 });
    heads.forEach(function (h) { obs.observe(h); });
  }
})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    build()
