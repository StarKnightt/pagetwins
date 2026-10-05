"""Hero illustrations and logo marks, drawn as SVG in code.

All artwork is original and generated here, so the dataset contains no
third-party images. Each function returns (svg_markup, width, height).
"""

from xml.sax.saxutils import escape

FONT = "Segoe UI, Arial, sans-serif"
MONO = "Consolas, 'Courier New', monospace"


def _svg(w, h, body, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}">'
        f"<defs>{defs}"
        '<filter id="sh" x="-20%" y="-20%" width="140%" height="150%">'
        '<feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#0f172a" flood-opacity="0.16"/>'
        "</filter></defs>"
        f"{body}</svg>"
    )


def _t(x, y, s, size=13, fill="#0f172a", weight=400, anchor="start", family=FONT, extra=""):
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>'
    )


def _window(x, y, w, h, fill="#ffffff", bar="#F1F3F8", dark=False):
    dots = "".join(
        f'<circle cx="{x + 20 + i * 16}" cy="{y + 18}" r="5" fill="{c}"/>'
        for i, c in enumerate(["#F87171", "#FBBF24", "#34D399"])
    )
    return (
        f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}"/></g>'
        f'<path d="M{x} {y + 12} a12 12 0 0 1 12 -12 h{w - 24} a12 12 0 0 1 12 12 v24 h-{w} z" fill="{bar}"/>'
        f"{dots}"
    )


def _pill(x, y, w, h, fill, label, ink="#ffffff", size=11, weight=600):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{fill}"/>'
        + _t(x + w / 2, y + h / 2 + size * 0.36, label, size, ink, weight, "middle")
    )


# --------------------------------------------------------------- split art

def invoices(c, brand):
    w, h = 540, 420
    rows = [
        ("Harbor Coffee", "$1,240", "Paid", "#DCFCE7", "#166534"),
        ("Oakline Studio", "$860", "Sent", "#DBEAFE", "#1E40AF"),
        ("Mira Lopez", "$2,150", "Paid", "#DCFCE7", "#166534"),
        ("Nordic Print", "$430", "Overdue", "#FEE2E2", "#991B1B"),
    ]
    body = f'<rect width="{w}" height="{h}" rx="18" fill="{c["accent"]}"/>'
    body += _window(26, 28, 488, 330)
    body += '<rect x="26" y="64" width="112" height="294" fill="#F8F9FD"/>'
    body += _t(42, 92, brand, 13, c["primary"], 700)
    for i, item in enumerate(["Invoices", "Clients", "Time", "Reports"]):
        yy = 108 + i * 30
        if i == 0:
            body += f'<rect x="36" y="{yy}" width="92" height="24" rx="6" fill="{c["accent"]}"/>'
        body += _t(46, yy + 16, item, 12, c["primary"] if i == 0 else "#64748B", 600 if i == 0 else 400)
    body += _t(156, 94, "Invoices", 16, "#0F172A", 700)
    body += f'<rect x="410" y="78" width="88" height="26" rx="7" fill="{c["primary"]}"/>'
    body += _t(454, 95, "New invoice", 11, "#ffffff", 600, "middle")
    body += _t(156, 128, "CLIENT", 10, "#94A3B8", 700) + _t(330, 128, "AMOUNT", 10, "#94A3B8", 700)
    body += _t(420, 128, "STATUS", 10, "#94A3B8", 700)
    for i, (name, amt, st, bg, ink) in enumerate(rows):
        yy = 140 + i * 40
        body += f'<line x1="156" y1="{yy}" x2="498" y2="{yy}" stroke="#EEF1F6"/>'
        body += _t(156, yy + 25, name, 13, "#1E293B", 500) + _t(330, yy + 25, amt, 13, "#1E293B", 600)
        body += _pill(420, yy + 10, 64, 22, bg, st, ink, 11)
    body += '<g filter="url(#sh)"><rect x="292" y="314" width="220" height="80" rx="14" fill="#ffffff"/></g>'
    body += '<circle cx="324" cy="354" r="16" fill="#DCFCE7"/>'
    body += '<path d="M316 354 l6 6 l11 -12" stroke="#16A34A" stroke-width="3" fill="none" stroke-linecap="round"/>'
    body += _t(350, 348, "Invoice #1042 paid", 13, "#0F172A", 700)
    body += _t(350, 368, "$1,240 from Harbor Coffee", 12, "#64748B")
    return _svg(w, h, body), w, h


def schedule(c, brand):
    w, h = 540, 420
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    staff = ["Ana", "Ben", "Chloe", "Dev", "Eli"]
    colors = [c["primary"], "#D97706", "#7C3AED"]
    plan = [
        [0, 0, None, 1, 1, None, 2], [1, None, 1, 1, None, 2, 2], [None, 2, 2, None, 0, 0, None],
        [0, 1, None, 0, 2, 2, None], [2, None, 0, 0, None, 1, 1],
    ]
    labels = ["7-3", "11-7", "4-11"]
    body = f'<rect width="{w}" height="{h}" rx="18" fill="{c["accent"]}"/>'
    body += _window(24, 26, 492, 312)
    body += _t(44, 88, "Week of Oct 12", 15, "#10201D", 700)
    body += _pill(392, 72, 104, 26, c["primary"], "Publish rota", "#ffffff", 11)
    x0, y0, cw, rh = 96, 108, 57, 40
    for i, d in enumerate(days):
        body += _t(x0 + i * cw + cw / 2, y0 + 8, d, 11, "#64748B", 600, "middle")
    for r, name in enumerate(staff):
        yy = y0 + 20 + r * rh
        body += f'<circle cx="58" cy="{yy + 15}" r="12" fill="#E2E8F0"/>'
        body += _t(58, yy + 19, name[0], 11, "#334155", 700, "middle")
        body += _t(76, yy + 19, name, 11, "#334155", 500)
        for d, s in enumerate(plan[r]):
            if s is None:
                continue
            body += _pill(x0 + d * cw + 4, yy + 4, cw - 8, 24, colors[s], labels[s], "#ffffff", 10)
    body += '<g filter="url(#sh)"><rect x="300" y="318" width="214" height="78" rx="14" fill="#ffffff"/></g>'
    body += _t(318, 344, "Labor cost this week", 12, "#64748B")
    body += _t(318, 372, "24% of sales", 18, "#10201D", 700)
    body += f'<rect x="436" y="358" width="60" height="8" rx="4" fill="#E2E8F0"/>'
    body += f'<rect x="436" y="358" width="24" height="8" rx="4" fill="{c["primary"]}"/>'
    return _svg(w, h, body), w, h


def home(c, brand):
    w, h = 540, 420
    body = f'<rect width="{w}" height="{h}" rx="18" fill="{c["accent"]}"/>'
    body += '<ellipse cx="160" cy="350" rx="150" ry="22" fill="#000" opacity="0.06"/>'
    body += f'<path d="M30 200 L160 96 L290 200 Z" fill="{c["primary"]}"/>'
    body += '<rect x="52" y="196" width="216" height="152" fill="#ffffff"/>'
    body += '<rect x="142" y="262" width="40" height="86" rx="4" fill="#CBD5E1"/>'
    body += '<circle cx="174" cy="306" r="3" fill="#64748B"/>'
    for x in (72, 206):
        body += f'<rect x="{x}" y="222" width="44" height="40" rx="4" fill="#BFDBFE"/>'
        body += f'<path d="M{x + 22} 222 v40 M{x} 242 h44" stroke="#ffffff" stroke-width="3"/>'
    for (sx, sy, r) in [(292, 104, 14), (52, 116, 10), (298, 152, 7), (30, 262, 7)]:
        body += (
            f'<path d="M{sx} {sy - r} Q{sx} {sy} {sx + r} {sy} Q{sx} {sy} {sx} {sy + r} '
            f'Q{sx} {sy} {sx - r} {sy} Q{sx} {sy} {sx} {sy - r} Z" fill="#FBBF24"/>'
        )
    body += '<g filter="url(#sh)"><rect x="310" y="168" width="208" height="196" rx="16" fill="#ffffff"/></g>'
    body += _t(328, 198, "Your cleaning", 12, "#64748B")
    body += _t(328, 224, "Friday, 9:00 AM", 18, "#0D1B33", 700)
    body += _t(328, 250, "2-bed home · about 3 hours", 12, "#475569")
    body += _pill(328, 266, 92, 24, "#DCFCE7", "Confirmed", "#166534", 11)
    body += '<line x1="328" y1="306" x2="500" y2="306" stroke="#EEF1F6"/>'
    for i, ini in enumerate(["R", "L"]):
        body += f'<circle cx="{342 + i * 22}" cy="332" r="13" fill="{c["primary"]}" stroke="#fff" stroke-width="2"/>'
        body += _t(342 + i * 22, 336, ini, 11, "#ffffff", 700, "middle")
    body += _t(382, 336, "Rosa and Lee", 12, "#334155", 600)
    return _svg(w, h, body), w, h


# ------------------------------------------------------------ centered art

def logs(c, brand):
    w, h = 880, 400
    body = f'<rect width="{w}" height="{h}" rx="18" fill="#0E1729"/>'
    body += _window(30, 26, 820, 348, fill="#0B1222", bar="#131D33")
    body += '<rect x="52" y="76" width="560" height="34" rx="8" fill="#131D33" stroke="#22314F"/>'
    body += _t(70, 98, "service:api  level:error  last 7 days", 13, "#C7D2E4", 400, family=MONO)
    body += _pill(626, 76, 96, 34, c["primary"], "Search", c["primary_ink"], 13, 700)
    body += _t(742, 98, "0.38 s", 13, "#7DD3A8", 600, family=MONO)
    heights = [8, 10, 9, 12, 8, 7, 11, 9, 10, 13, 9, 8, 30, 46, 22, 10, 9, 8, 11, 10,
               9, 8, 12, 9, 10, 8, 9, 11, 10, 9, 8, 26, 12, 9, 10, 8, 9, 10, 11, 9]
    for i, hh in enumerate(heights):
        col = "#F87171" if hh > 20 else "#334A70"
        body += f'<rect x="{54 + i * 19.5}" y="{184 - hh * 1.4}" width="13" height="{hh * 1.4}" rx="2" fill="{col}"/>'
    body += '<line x1="52" y1="186" x2="828" y2="186" stroke="#22314F"/>'
    lines = [
        ("12:04:31", "ERROR", "#F87171", "api", "Timeout calling payments service (5012 ms)"),
        ("12:04:29", "WARN", "#FBBF24", "web", "Slow query on /checkout (1.8 s)"),
        ("12:04:27", "ERROR", "#F87171", "api", "Connection reset by peer: db-replica-2"),
        ("12:04:22", "INFO", "#7C8BA3", "worker", "Job 8841 finished in 212 ms"),
        ("12:04:19", "ERROR", "#F87171", "api", "Timeout calling payments service (5007 ms)"),
        ("12:04:11", "INFO", "#7C8BA3", "web", "GET /pricing 200 in 41 ms"),
    ]
    for i, (ts, lvl, col, svc, msg) in enumerate(lines):
        yy = 214 + i * 26
        body += _t(56, yy, ts, 12.5, "#7C8BA3", family=MONO)
        body += f'<rect x="128" y="{yy - 13}" width="54" height="18" rx="4" fill="{col}" opacity="0.18"/>'
        body += _t(155, yy, lvl, 11, col, 700, "middle", family=MONO)
        body += _t(196, yy, svc, 12.5, "#93C5FD", family=MONO)
        body += _t(262, yy, msg, 12.5, "#D7DFEC", family=MONO)
    return _svg(w, h, body), w, h


def shipping(c, brand):
    w, h = 880, 400
    body = f'<rect width="{w}" height="{h}" rx="18" fill="{c["accent"]}"/>'
    body += _window(28, 26, 500, 346)
    body += _t(50, 90, "Order #3021 · 2 items · 1.4 lb", 15, "#111733", 700)
    body += _t(50, 112, "Ships to Columbus, OH 43215", 12, "#64748B")
    opts = [("Ground", "3 to 5 days", "$8.12", True), ("Express", "1 to 2 days", "$14.90", False),
            ("Economy", "5 to 8 days", "$6.45", False)]
    for i, (n, d, p, sel) in enumerate(opts):
        yy = 132 + i * 62
        stroke = c["primary"] if sel else "#E1E5F2"
        body += f'<rect x="50" y="{yy}" width="456" height="50" rx="10" fill="#ffffff" stroke="{stroke}" stroke-width="{2 if sel else 1}"/>'
        body += f'<circle cx="74" cy="{yy + 25}" r="8" fill="none" stroke="{stroke}" stroke-width="2"/>'
        if sel:
            body += f'<circle cx="74" cy="{yy + 25}" r="4" fill="{c["primary"]}"/>'
        body += _t(94, yy + 22, n, 13, "#111733", 700) + _t(94, yy + 39, d, 11, "#64748B")
        body += _t(490, yy + 30, p, 15, "#111733", 700, "end")
    body += _pill(50, 324, 160, 34, c["primary"], "Buy and print label", "#ffffff", 12, 700)
    body += '<g filter="url(#sh)"><rect x="566" y="58" width="270" height="300" rx="10" fill="#ffffff"/></g>'
    body += _t(586, 88, "FROM", 10, "#94A3B8", 700) + _t(586, 104, "Pebble Paper", 12, "#111733", 600)
    body += _t(586, 132, "SHIP TO", 10, "#94A3B8", 700) + _t(586, 150, "Jordan Ellis", 14, "#111733", 700)
    body += _t(586, 168, "214 Maple Ave, Columbus OH", 12, "#334155")
    body += '<line x1="586" y1="186" x2="816" y2="186" stroke="#111733" stroke-width="2"/>'
    x = 588
    for i in range(46):
        bw = 2 if i % 3 else 4
        body += f'<rect x="{x}" y="200" width="{bw}" height="64" fill="#111733"/>'
        x += bw + 3
    body += _t(701, 286, "TRACKING  PP 4402 9921 7730", 11, "#111733", 600, "middle", family=MONO)
    body += _pill(650, 306, 102, 28, "#DCFCE7", "Label printed", "#166534", 11)
    return _svg(w, h, body), w, h


def sketchbook(c, brand):
    w, h = 880, 400
    body = f'<rect width="{w}" height="{h}" rx="18" fill="{c["accent"]}"/>'
    body += '<g filter="url(#sh)"><rect x="96" y="40" width="688" height="320" rx="10" fill="#FFFDF7"/></g>'
    body += '<line x1="440" y1="46" x2="440" y2="354" stroke="#E9E2D3" stroke-width="2"/>'
    for i in range(14):
        body += f'<circle cx="440" cy="{58 + i * 21.5}" r="4" fill="none" stroke="#9CA3AF" stroke-width="2"/>'
    g = 'stroke="#57534E" fill="none" stroke-linecap="round"'
    # coffee cup sketch
    body += f'<ellipse cx="268" cy="150" rx="82" ry="22" {g} stroke-width="2.4"/>'
    body += f'<path d="M186 150 L204 286 Q268 306 332 286 L350 150" {g} stroke-width="2.4"/>'
    body += f'<path d="M346 176 Q396 182 384 226 Q374 256 336 252" {g} stroke-width="2.4"/>'
    body += f'<ellipse cx="268" cy="290" rx="118" ry="20" {g} stroke-width="1.6" opacity="0.6"/>'
    body += f'<path d="M206 170 L222 280 M230 172 L240 284" {g} stroke-width="1" opacity="0.35"/>'
    body += f'<path d="M248 104 Q258 88 248 72 M276 108 Q288 90 276 72" {g} stroke-width="1.6" opacity="0.7"/>'
    # face construction
    body += f'<ellipse cx="612" cy="196" rx="86" ry="112" {g} stroke-width="2.2"/>'
    body += f'<path d="M526 196 H698 M612 84 V308" {g} stroke-width="1" opacity="0.4"/>'
    body += f'<path d="M532 236 H692 M546 266 H678" {g} stroke-width="1" opacity="0.35"/>'
    body += f'<path d="M566 190 Q580 180 594 190 M630 190 Q644 180 658 190" {g} stroke-width="2"/>'
    body += f'<path d="M612 204 L604 238 Q612 244 622 238" {g} stroke-width="1.8"/>'
    body += f'<path d="M586 268 Q612 282 640 268" {g} stroke-width="2"/>'
    # pencil
    body += '<g transform="rotate(-32 700 330)">'
    body += '<rect x="600" y="318" width="190" height="20" rx="3" fill="#FACC15"/>'
    body += '<rect x="772" y="318" width="22" height="20" fill="#F9A8D4"/>'
    body += '<rect x="764" y="318" width="10" height="20" fill="#A8A29E"/>'
    body += '<path d="M600 318 L572 328 L600 338 Z" fill="#F5DEB3"/><path d="M581 325 L572 328 L581 331 Z" fill="#44403C"/>'
    body += "</g>"
    return _svg(w, h, body), w, h


# ------------------------------------------------------------- product art

def bottle(c, brand):
    w, h = 520, 520
    body = f'<rect width="{w}" height="{h}" rx="22" fill="{c["accent"]}"/>'
    body += '<circle cx="260" cy="250" r="190" fill="#ffffff" opacity="0.55"/>'
    body += '<ellipse cx="250" cy="452" rx="190" ry="20" fill="#000" opacity="0.07"/>'
    body += '<rect x="172" y="70" width="56" height="34" rx="6" fill="#1F120A"/>'
    body += '<path d="M180 104 h40 v34 q44 18 44 70 v226 q0 22 -22 22 h-84 q-22 0 -22 -22 v-226 q0 -52 44 -70 z" fill="#5A2410"/>'
    body += '<path d="M150 214 h100 v170 h-100 z" fill="#FFF4E8"/>'
    body += _t(200, 252, brand.upper(), 13, "#3B1708", 700, "middle", family="Georgia, serif", extra='letter-spacing="0.5"')
    body += '<line x1="166" y1="264" x2="234" y2="264" stroke="#C08457" stroke-width="1.5"/>'
    body += _t(200, 290, "COLD BREW", 13, "#7C2D12", 700, "middle", extra='letter-spacing="1.5"')
    body += _t(200, 310, "concentrate", 12, "#7C2D12", 400, "middle")
    body += _t(200, 364, "32 FL OZ", 11, "#9A6B4F", 600, "middle")
    body += '<path d="M150 220 q-4 140 0 176" stroke="#ffffff" stroke-width="5" opacity="0.18" fill="none"/>'
    # glass
    body += '<path d="M300 220 h130 l-14 220 q-2 14 -16 14 h-70 q-14 0 -16 -14 z" fill="#ffffff" opacity="0.65" stroke="#E7D3BF"/>'
    body += '<path d="M308 268 h114 l-10 166 q-2 10 -12 10 h-70 q-10 0 -12 -10 z" fill="#8A4A24"/>'
    body += '<path d="M310 268 h110 v26 h-110 z" fill="#D9A97A" opacity="0.8"/>'
    for (x, y) in [(320, 286), (356, 300), (386, 282), (338, 330)]:
        body += f'<rect x="{x}" y="{y}" width="28" height="28" rx="6" fill="#ffffff" opacity="0.45" transform="rotate(12 {x + 14} {y + 14})"/>'
    body += '<path d="M392 150 l-16 240" stroke="#F97316" stroke-width="9" stroke-linecap="round"/>'
    return _svg(w, h, body), w, h


def hoodie(c, brand):
    w, h = 520, 520
    body = f'<rect width="{w}" height="{h}" rx="10" fill="#E9E5DC"/>'
    body += '<ellipse cx="250" cy="468" rx="200" ry="18" fill="#000" opacity="0.08"/>'
    body += (
        '<path d="M190 96 Q250 52 310 96 L322 126 Q382 140 418 196 L452 330 Q456 346 440 350 '
        'L404 356 Q392 356 390 342 L370 250 L370 440 Q370 456 354 456 L146 456 Q130 456 130 440 '
        'L130 250 L110 342 Q108 356 96 356 L60 350 Q44 346 48 330 L82 196 Q118 140 178 126 Z" fill="#3F444C"/>'
    )
    body += '<path d="M190 96 Q250 150 310 96 Q300 150 250 168 Q200 150 190 96 Z" fill="#2E3238"/>'
    body += '<path d="M236 168 l-6 70 M264 168 l6 70" stroke="#D6D3CB" stroke-width="3" stroke-linecap="round"/>'
    body += '<circle cx="230" cy="242" r="5" fill="#D6D3CB"/><circle cx="270" cy="242" r="5" fill="#D6D3CB"/>'
    body += '<path d="M170 330 h160 l18 78 h-196 z" fill="#353A41"/>'
    body += '<path d="M130 440 h240" stroke="#2E3238" stroke-width="8"/>'
    body += '<path d="M300 200 l20 4" stroke="#5B616B" stroke-width="2"/>'
    body += '<g filter="url(#sh)"><rect x="380" y="380" width="128" height="88" rx="14" fill="#ffffff"/></g>'
    body += '<rect x="396" y="396" width="38" height="56" rx="10" fill="#3F444C"/>'
    body += _t(444, 418, "Packs into", 11, "#5E5A52")
    body += _t(444, 436, "its own", 11, "#5E5A52")
    body += _t(444, 454, "pocket", 11, "#1C1B19", 700)
    return _svg(w, h, body), w, h


# ----------------------------------------------------------------- app art

def _phone(inner, w, h, c):
    px, py, pw, ph = (w - 250) / 2, 24, 250, h - 48
    s = f'<rect width="{w}" height="{h}" rx="22" fill="{c["accent"]}"/>'
    s += f'<g filter="url(#sh)"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="36" fill="#111827"/></g>'
    s += f'<rect x="{px + 10}" y="{py + 10}" width="{pw - 20}" height="{ph - 20}" rx="28" fill="#ffffff"/>'
    s += f'<rect x="{px + pw / 2 - 36}" y="{py + 18}" width="72" height="18" rx="9" fill="#111827"/>'
    s += _t(px + 30, py + 32, "9:41", 11, "#111827", 700)
    s += f'<g transform="translate({px + 10} {py + 46})">{inner}</g>'
    return s


def phone_budget(c, brand):
    w, h = 420, 520
    p = c["primary"]
    inner = _t(20, 26, "October budget", 16, "#1A1033", 700)
    inner += _t(20, 44, "Shared with Daniel", 11, "#6B7280")
    inner += '<circle cx="115" cy="122" r="52" fill="none" stroke="#EEE9F8" stroke-width="14"/>'
    inner += (
        f'<circle cx="115" cy="122" r="52" fill="none" stroke="{p}" stroke-width="14" '
        'stroke-dasharray="203 327" stroke-linecap="round" transform="rotate(-90 115 122)"/>'
    )
    inner += _t(115, 120, "62%", 22, "#1A1033", 700, "middle") + _t(115, 138, "spent", 11, "#6B7280", 400, "middle")
    inner += _t(115, 200, "$1,860 of $3,000", 12, "#374151", 600, "middle")
    rows = [("Rent, split 50/50", "$1,400"), ("Groceries", "$412"), ("Utilities", "$148")]
    for i, (a, b) in enumerate(rows):
        yy = 222 + i * 34
        inner += f'<rect x="14" y="{yy}" width="202" height="28" rx="8" fill="#F8F6FD"/>'
        inner += _t(24, yy + 18, a, 11, "#1A1033", 500) + _t(206, yy + 18, b, 11, "#1A1033", 700, "end")
    inner += f'<rect x="14" y="330" width="202" height="62" rx="12" fill="{c["accent"]}"/>'
    inner += _t(26, 352, "Trip to Lisbon", 12, "#1A1033", 700) + _t(204, 352, "70%", 12, p, 700, "end")
    inner += '<rect x="26" y="364" width="178" height="8" rx="4" fill="#ffffff"/>'
    inner += f'<rect x="26" y="364" width="125" height="8" rx="4" fill="{p}"/>'
    inner += _t(26, 386, "$2,100 of $3,000 saved", 10, "#6B7280")
    return _svg(w, h, _phone(inner, w, h, c)), w, h


def phone_plants(c, brand):
    w, h = 420, 520
    p = c["primary"]
    leaf = (
        f'<path d="M0 0 Q30 -40 70 -30 Q60 10 0 0 Z" fill="{p}" opacity="0.9"/>'
        '<path d="M0 0 Q34 -18 64 -28" stroke="#ffffff" stroke-width="1.5" fill="none" opacity="0.7"/>'
    )
    bg = f'<g transform="translate(36 380) rotate(-20)">{leaf}</g><g transform="translate(330 150) rotate(150) scale(1.4)">{leaf}</g>'
    inner = _t(20, 26, "Today", 18, "#0F2417", 700)
    inner += _t(20, 44, "3 plants need you this week", 11, "#6B7280")
    cards = [("Monstera", "Water today", "#FEF3C7", "#92400E"),
             ("Boston fern", "Mist in 2 days", "#E8F5EC", "#166534"),
             ("Snake plant", "Water in 9 days", "#E8F5EC", "#166534"),
             ("Pothos", "Feed on Sunday", "#E0F2FE", "#075985")]
    for i, (n, s, bgc, ink) in enumerate(cards):
        yy = 62 + i * 78
        inner += f'<rect x="14" y="{yy}" width="202" height="66" rx="14" fill="#F6FAF7"/>'
        inner += f'<circle cx="44" cy="{yy + 33}" r="18" fill="{c["accent"]}"/>'
        inner += f'<g transform="translate(34 {yy + 42}) scale(0.32)">{leaf}</g>'
        inner += _t(72, yy + 28, n, 13, "#0F2417", 700)
        inner += _pill(72, yy + 38, 112, 20, bgc, s, ink, 10)
    return _svg(w, h, bg + _phone(inner, w, h, c)), w, h


ART = {
    "invoices": invoices, "schedule": schedule, "home": home, "logs": logs,
    "shipping": shipping, "sketchbook": sketchbook, "bottle": bottle,
    "hoodie": hoodie, "phone_budget": phone_budget, "phone_plants": phone_plants,
}


# -------------------------------------------------------------- logo marks

def mark(kind, color, ink="#ffffff"):
    shapes = {
        "hawk": f'<path d="M3 17 L14 6 L25 17 L19 15 L14 20 L9 15 Z" fill="{ink}"/>',
        "clock": f'<circle cx="14" cy="14" r="8" fill="none" stroke="{ink}" stroke-width="2.4"/>'
                 f'<path d="M14 9 V14 L17.5 16" stroke="{ink}" stroke-width="2.4" fill="none" stroke-linecap="round"/>',
        "pine": f'<path d="M14 5 L21 15 H17 L22 21 H6 L11 15 H7 Z" fill="{ink}"/>',
        "parcel": f'<path d="M6 10 L14 6 L22 10 V19 L14 23 L6 19 Z" fill="none" stroke="{ink}" stroke-width="2.2"/>'
                  f'<path d="M6 10 L14 14 L22 10 M14 14 V23" stroke="{ink}" stroke-width="2.2" fill="none"/>',
        "bean": f'<ellipse cx="14" cy="14" rx="6.5" ry="9" fill="{ink}" transform="rotate(30 14 14)"/>'
                f'<path d="M11 8 Q16 14 12 20" stroke="{color}" stroke-width="1.8" fill="none"/>',
        "wave": f'<path d="M5 16 Q9.5 9 14 16 T23 16" stroke="{ink}" stroke-width="2.6" fill="none" stroke-linecap="round"/>',
        "coin": f'<circle cx="14" cy="14" r="8" fill="none" stroke="{ink}" stroke-width="2.4"/>'
                f'<path d="M14 9.5 V18.5 M11.5 12 H16 M11.5 16 H16" stroke="{ink}" stroke-width="2" fill="none"/>',
        "leaf": f'<path d="M7 20 Q7 8 21 7 Q21 20 7 20 Z" fill="{ink}"/>'
                f'<path d="M8 19 L17 11" stroke="{color}" stroke-width="1.6"/>',
        "pencil": f'<path d="M7 21 L8.5 16 L18 6.5 L21.5 10 L12 19.5 Z" fill="{ink}"/>',
        "sparkle": f'<path d="M14 5 Q15 13 23 14 Q15 15 14 23 Q13 15 5 14 Q13 13 14 5 Z" fill="{ink}"/>',
    }
    return (
        '<svg viewBox="0 0 28 28" width="28" height="28" aria-hidden="true">'
        f'<rect width="28" height="28" rx="8" fill="{color}"/>{shapes[kind]}</svg>'
    )
