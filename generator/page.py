"""Render a page spec to a self-contained HTML document.

A spec is one of the dicts in content.BASES (possibly edited by a defect or a
harmless variant). `flags` carries the defects that are easier to express as
rendering switches than as copy edits.
"""

from html import escape

from art import mark

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-font-smoothing:antialiased}
body{font-family:var(--font-body);color:var(--text);background:var(--bg);font-size:16px;line-height:1.55;position:relative}
a{color:inherit;text-decoration:none}
.wrap{max-width:1140px;margin:0 auto;padding:0 40px}
.nav{background:var(--hero-bg);border-bottom:1px solid var(--border)}
.nav .wrap{height:70px;display:flex;align-items:center;justify-content:space-between}
.logo{display:flex;align-items:center;gap:10px;font-family:var(--font-head);font-weight:700;font-size:20px;letter-spacing:-.01em}
.nav-links{display:flex;gap:30px;font-size:15px;color:var(--muted)}
.nav-actions{display:flex;align-items:center;gap:20px;font-size:15px}
.btn{display:inline-flex;align-items:center;justify-content:center;border-radius:calc(var(--radius) * .7);font-weight:600;font-size:16px;padding:14px 24px;border:1.5px solid transparent;white-space:nowrap;line-height:1.2;font-family:var(--font-body)}
.btn-primary{background:var(--primary);color:var(--primary-ink);box-shadow:0 8px 20px -10px var(--primary)}
.btn-ghost{background:transparent;color:var(--text);border-color:var(--border)}
.btn-sm{padding:9px 16px;font-size:14px;box-shadow:none}
.hero{background:var(--hero-bg);padding:72px 0 70px}
.hero-grid{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center}
.tpl-app .hero-grid{grid-template-columns:1.2fr .8fr}
.tpl-product .hero-grid{grid-template-columns:1fr 1fr}
.tpl-centered .hero-copy{text-align:center;max-width:840px;margin:0 auto}
.tpl-centered .hero-visual{margin:50px auto 0;max-width:880px}
.eyebrow{display:inline-block;font-size:12.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--primary);background:var(--accent);padding:6px 12px;border-radius:999px;margin-bottom:22px}
.headline{font-family:var(--font-head);font-size:54px;line-height:1.08;letter-spacing:-.02em;font-weight:800;color:var(--text);margin-bottom:20px}
.tpl-centered .headline{font-size:58px;max-width:780px;margin-left:auto;margin-right:auto}
.subhead{font-size:19px;line-height:1.6;color:var(--muted);margin-bottom:30px;max-width:560px}
.tpl-centered .subhead{margin-left:auto;margin-right:auto;max-width:660px}
.hero-ctas{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:18px}
.tpl-centered .hero-ctas{justify-content:center}
.hero-note{font-size:14px;color:var(--muted)}
.price-line{display:flex;align-items:baseline;gap:12px;margin-bottom:24px}
.price-line strong{font-size:34px;font-family:var(--font-head);letter-spacing:-.01em}
.price-line span{color:var(--muted);font-size:15px}
.hero-visual img{display:block;width:100%;height:auto;border-radius:var(--radius)}
.tpl-app .hero-visual img{max-width:400px;margin-left:auto}
.proof{padding:30px 0;border-bottom:1px solid var(--border);background:var(--bg)}
.proof .wrap{display:flex;align-items:center;justify-content:center;gap:34px;flex-wrap:wrap}
.proof-label{font-size:14.5px;color:var(--muted);font-weight:600}
.logos{display:flex;gap:34px}
.logos span{font-family:var(--font-head);font-weight:700;font-size:18px;color:var(--muted);opacity:.8;letter-spacing:-.01em}
.stars{color:#F59E0B;font-size:19px;letter-spacing:3px}
section.block{padding:64px 0}
.section-title{font-family:var(--font-head);font-size:34px;line-height:1.2;letter-spacing:-.015em;font-weight:700;text-align:center;margin-bottom:38px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:28px}
.icon{width:40px;height:40px;border-radius:10px;background:var(--accent);color:var(--primary);display:flex;align-items:center;justify-content:center;margin-bottom:16px;font-weight:800;font-size:17px}
.card h3{font-size:18px;margin-bottom:8px;font-family:var(--font-head)}
.card p{color:var(--muted);font-size:15.5px}
.testimonial{background:var(--surface);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.testimonial blockquote{max-width:780px;margin:0 auto;text-align:center;font-family:var(--font-head);font-size:25px;line-height:1.45;font-weight:500}
.person{display:flex;align-items:center;justify-content:center;gap:12px;margin-top:24px;text-align:left}
.avatar{width:46px;height:46px;border-radius:50%;background:var(--primary);color:var(--primary-ink);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px}
.person strong{display:block;font-size:15px}
.person span{font-size:14px;color:var(--muted)}
.tiers{display:grid;gap:22px;justify-content:center}
.tiers.n2{grid-template-columns:repeat(2,350px)}
.tiers.n3{grid-template-columns:repeat(3,1fr)}
.tier{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:30px;position:relative;display:flex;flex-direction:column}
.tier.popular{border:2px solid var(--primary)}
.badge{position:absolute;top:-13px;left:28px;background:var(--primary);color:var(--primary-ink);font-size:12px;font-weight:700;padding:4px 11px;border-radius:999px}
.tier h3{font-size:17px;margin-bottom:10px}
.price{font-family:var(--font-head);font-size:40px;font-weight:800;letter-spacing:-.02em;line-height:1.1}
.price small{font-size:15px;color:var(--muted);font-weight:500;font-family:var(--font-body);letter-spacing:0;margin-left:6px}
.tier ul{list-style:none;margin:20px 0 24px;display:grid;gap:10px;font-size:15px;color:var(--muted)}
.tier li::before{content:"\\2713";color:var(--primary);font-weight:800;margin-right:10px}
.tier .btn{margin-top:auto}
.pricing-note{text-align:center;color:var(--muted);font-size:14px;margin-top:26px}
.faq{display:grid;grid-template-columns:repeat(2,1fr);gap:26px 40px;max-width:980px;margin:44px auto 0;padding-top:36px;border-top:1px solid var(--border)}
.faq dt{font-weight:700;margin-bottom:6px;font-size:16px}
.faq dd{color:var(--muted);font-size:15.5px}
.band{background:var(--band-bg);color:var(--band-ink);padding:60px 0;text-align:center}
.band h2{font-family:var(--font-head);font-size:34px;letter-spacing:-.015em;margin-bottom:24px}
.band .btn-primary{box-shadow:none}
.band-ctas{display:flex;gap:12px;justify-content:center}
.footer{padding:28px 0;font-size:14px;color:var(--muted);background:var(--bg)}
.footer .wrap{display:flex;justify-content:space-between;align-items:center}
.footer nav{display:flex;gap:22px}
.popup-layer{position:absolute;top:0;left:0;right:0;height:800px;background:rgba(10,15,30,.68);display:flex;align-items:center;justify-content:center;z-index:100}
.popup{background:#fff;color:#111827;width:540px;border-radius:18px;padding:42px 46px;text-align:center;position:relative;box-shadow:0 30px 80px rgba(0,0,0,.35)}
.popup h3{font-size:27px;line-height:1.25;margin-bottom:10px;font-family:var(--font-head)}
.popup p{color:#4B5563;margin-bottom:22px;font-size:16px}
.popup form{display:flex;gap:10px}
.popup input{flex:1;padding:13px 14px;border:1px solid #D1D5DB;border-radius:10px;font-size:15px;font-family:var(--font-body)}
.popup .btn{box-shadow:none}
.popup .close{position:absolute;top:12px;right:18px;font-size:26px;line-height:1;color:#9CA3AF;background:none;border:0}
.popup .dismiss{display:inline-block;margin-top:16px;font-size:14px;color:#6B7280;text-decoration:underline}
"""


def _theme_vars(t):
    return (
        ":root{"
        f"--primary:{t['primary']};--primary-ink:{t['primary_ink']};--accent:{t['accent']};"
        f"--bg:{t['bg']};--hero-bg:{t['hero_bg']};--surface:{t['surface']};--text:{t['text']};"
        f"--muted:{t['muted']};--border:{t['border']};--band-bg:{t['band_bg']};--band-ink:{t['band_ink']};"
        f"--font-head:{t['font_head']};--font-body:{t['font_body']};--radius:{t['radius']};"
        "}"
    )


def _initials(name):
    parts = [p for p in name.replace(" and ", " ").split() if p[:1].isalpha()]
    return (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()


def _btn(label, cls, primary, flags, extra=""):
    if primary and flags.get("no_primary_cta"):
        return ""
    data = ' data-cta="primary"' if primary else ""
    return f'<a href="#" class="btn {cls}"{data}{extra}>{escape(label)}</a>'


def render(spec, flags=None, hero_src="hero.svg", hero_size=(540, 420)):
    flags = flags or {}
    t = spec["theme"]
    h = spec["hero"]
    tpl = spec["template"]
    e = escape

    # ---- nav
    nav = (
        '<header class="nav"><div class="wrap">'
        f'<a href="#" class="logo">{mark(t["mark"], t["primary"], t["primary_ink"])}<span>{e(spec["brand"])}</span></a>'
        '<nav class="nav-links">' + "".join(f'<a href="#">{e(x)}</a>' for x in spec["nav_links"]) + "</nav>"
        '<div class="nav-actions"><a href="#" class="login">Log in</a>'
        + _btn(spec["nav_cta"], "btn-primary btn-sm", True, flags)
        + "</div></div></header>"
    )

    # ---- hero
    headline_style = ""
    if flags.get("headline_color"):
        headline_style += f"color:{flags['headline_color']};"
    if flags.get("headline_clip"):
        headline_style += "height:1.6em;overflow:hidden;"
    style_attr = f' style="{headline_style}"' if headline_style else ""

    price_line = ""
    if h.get("price_line"):
        price_line = (
            f'<div class="price-line"><strong>{e(h["price_line"][0])}</strong>'
            f'<span>{e(h["price_line"][1])}</span></div>'
        )
    ctas = (
        _btn(h["cta"], "btn-primary", True, flags)
        + _btn(h["cta2"], "btn-primary" if h.get("cta2_primary") else "btn-ghost",
               bool(h.get("cta2_primary")), flags)
    )
    copy = (
        '<div class="hero-copy">'
        f'<span class="eyebrow">{e(h["eyebrow"])}</span>'
        f'<h1 class="headline"{style_attr}>{e(h["headline"])}</h1>'
        f'<p class="subhead">{e(h["subhead"])}</p>'
        f"{price_line}"
        f'<div class="hero-ctas">{ctas}</div>'
        f'<p class="hero-note">{e(h["note"])}</p>'
        "</div>"
    )
    src = "img/hero-final@2x.png" if flags.get("broken_image") else hero_src
    w, hh = hero_size
    visual = (
        f'<div class="hero-visual"><img src="{src}" alt="{e(h["image_alt"])}" '
        f'width="{w}" height="{hh}"></div>'
    )
    if tpl == "centered":
        hero_inner = copy + visual
    elif tpl == "product":
        hero_inner = f'<div class="hero-grid">{visual}{copy}</div>'
    else:
        hero_inner = f'<div class="hero-grid">{copy}{visual}</div>'
    hero = f'<section class="hero"><div class="wrap">{hero_inner}</div></section>'

    # ---- proof
    p = spec["proof"]
    if p["logos"]:
        proof_inner = (
            f'<p class="proof-label">{e(p["label"])}</p>'
            '<div class="logos">' + "".join(f"<span>{e(x)}</span>" for x in p["logos"]) + "</div>"
        )
    else:
        proof_inner = f'<span class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span><p class="proof-label">{e(p["label"])}</p>'
    proof = f'<section class="proof"><div class="wrap">{proof_inner}</div></section>'

    # ---- features
    f = spec["features"]
    cards = "".join(
        f'<div class="card"><div class="icon" aria-hidden="true">{i + 1}</div>'
        f"<h3>{e(title)}</h3><p>{e(body)}</p></div>"
        for i, (title, body) in enumerate(f["items"])
    )
    features = (
        '<section class="block" id="features"><div class="wrap">'
        f'<h2 class="section-title">{e(f["title"])}</h2><div class="grid3">{cards}</div>'
        "</div></section>"
    )

    # ---- testimonial
    tm = spec["testimonial"]
    attribution = tm.get("attribution")
    if attribution:
        person_text = f"<strong>{e(attribution)}</strong>"
    else:
        person_text = f'<strong>{e(tm["name"])}</strong><span>{e(tm["role"])}</span>'
    initials = _initials(tm["name"])
    testimonial = (
        '<section class="block testimonial"><div class="wrap">'
        f'<blockquote>"{e(tm["quote"])}"</blockquote>'
        f'<div class="person"><div class="avatar" aria-hidden="true">{e(initials)}</div><div>{person_text}</div></div>'
        "</div></section>"
    )

    # ---- pricing + faq
    pr = spec["pricing"]
    tier_html = ""
    for tier in pr["tiers"]:
        badge = '<span class="badge">Most popular</span>' if tier.get("popular") else ""
        period = f'<small>{e(tier["period"])}</small>' if tier.get("period") else ""
        items = "".join(f"<li>{e(x)}</li>" for x in tier["features"])
        btn = _btn(tier["cta"], "btn-primary" if tier.get("popular") else "btn-ghost", True, flags)
        tier_html += (
            f'<div class="tier{" popular" if tier.get("popular") else ""}">{badge}'
            f'<h3>{e(tier["name"])}</h3><div class="price">{e(tier["price"])}{period}</div>'
            f"<ul>{items}</ul>{btn}</div>"
        )
    note = f'<p class="pricing-note">{e(pr["note"])}</p>' if pr.get("note") else ""
    faq = "".join(f"<div><dt>{e(q)}</dt><dd>{e(a)}</dd></div>" for q, a in spec["faq"])
    pricing = (
        '<section class="block" id="pricing"><div class="wrap">'
        f'<h2 class="section-title">{e(pr["title"])}</h2>'
        f'<div class="tiers n{len(pr["tiers"])}">{tier_html}</div>{note}'
        f'<dl class="faq">{faq}</dl>'
        "</div></section>"
    )

    # ---- band + footer
    b = spec["band"]
    band_ctas = _btn(b["cta"], "btn-primary", True, flags)
    if h.get("cta2_primary") and tpl == "app":
        band_ctas += _btn(h["cta2"], "btn-primary", True, flags)
    band_btns = f'<div class="band-ctas">{band_ctas}</div>' if band_ctas else ""
    band = (
        '<section class="band"><div class="wrap">'
        f'<h2>{e(b["title"])}</h2>{band_btns}</div></section>'
    )
    ft = spec["footer"]
    footer = (
        '<footer class="footer"><div class="wrap">'
        f'<span>&copy; 2026 {e(ft["company"])} · {e(ft["place"])}</span>'
        '<nav><a href="#">Privacy</a><a href="#">Terms</a><a href="#">Contact</a></nav>'
        "</div></footer>"
    )

    # ---- popup
    popup = ""
    if flags.get("popup"):
        pp = flags["popup"]
        popup = (
            '<div class="popup-layer" role="dialog" aria-modal="true" aria-label="Signup offer">'
            '<div class="popup"><button class="close" aria-label="Close">&times;</button>'
            f'<h3>{e(pp["title"])}</h3><p>{e(pp["body"])}</p>'
            '<form><input type="email" placeholder="you@example.com" aria-label="Email address">'
            f'<a href="#" class="btn btn-primary">{e(pp["button"])}</a></form>'
            '<a href="#" class="dismiss">No thanks</a></div></div>'
        )

    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{e(spec['title'])}</title>"
        f"<style>{_theme_vars(t)}{CSS}</style></head>"
        f'<body class="tpl-{tpl}">{nav}<main>{hero}{proof}{features}{testimonial}{pricing}{band}</main>'
        f"{footer}{popup}</body></html>\n"
    )
