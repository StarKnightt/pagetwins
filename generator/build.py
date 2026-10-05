"""Build the PageTwins dataset: HTML, screenshots, text views, labels and checks.

    python generator/build.py

Writes everything to dataset/. Every twin is verified in a real browser: its
own defect must be detectable by a DOM check, and every other check must match
the clean page.
"""

import csv
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from art import ART  # noqa: E402
from content import BASES, DEFECTS, TEXT_VISIBLE  # noqa: E402
from defects import make_twin, make_variant  # noqa: E402
from page import render  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dataset"
VERSION = "1.0"

OUTLINE_JS = r"""
() => {
  const out = [];
  const clean = s => (s || '').replace(/\s+/g, ' ').trim();
  const push = s => { s = clean(s); if (s) out.push(s); };
  const hidden = el => { const cs = getComputedStyle(el); return cs.display === 'none' || cs.visibility === 'hidden'; };
  const directText = el => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
  const leafTags = ['p', 'li', 'blockquote', 'dt', 'dd'];
  push('Page title: ' + document.title);
  function walk(el) {
    for (const c of el.children) {
      const tag = c.tagName.toLowerCase();
      if (['script', 'style', 'svg'].includes(tag) || hidden(c) || c.getAttribute('aria-hidden') === 'true') continue;
      if (c.getAttribute('role') === 'dialog') {
        out.push(''); push('[dialog] ' + (c.getAttribute('aria-label') || '')); walk(c); push('[end of dialog]'); continue;
      }
      if (['header', 'section', 'footer'].includes(tag)) out.push('');
      if (/^h[1-6]$/.test(tag)) { push('[' + tag + '] ' + c.innerText); continue; }
      if (tag === 'img') { push('[image] alt="' + c.alt + '"'); continue; }
      if (tag === 'input') { push('[text field] ' + (c.placeholder || '')); continue; }
      if (tag === 'a' || tag === 'button') {
        const label = clean(c.innerText) || c.getAttribute('aria-label') || '';
        push(((tag === 'button' || c.classList.contains('btn')) ? '[button] ' : '[link] ') + label);
        continue;
      }
      if ((leafTags.includes(tag) || directText(c)) && !c.querySelector('a,button,img,input,h1,h2,h3')) {
        push(c.innerText); continue;
      }
      walk(c);
    }
  }
  walk(document.body);
  return out.join('\n').replace(/\n{3,}/g, '\n\n').trim() + '\n';
}
"""

CHECKS_JS = r"""
() => {
  const q = s => document.querySelector(s);
  const visible = el => {
    if (!el) return false;
    const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden';
  };
  const parse = c => {
    const m = c.match(/rgba?\(([^)]+)\)/); const p = m[1].split(/[,\s\/]+/).filter(Boolean).map(Number);
    return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1};
  };
  const bgOf = el => {
    while (el) { const c = parse(getComputedStyle(el).backgroundColor); if (c.a > 0.5) return c; el = el.parentElement; }
    return {r: 255, g: 255, b: 255, a: 1};
  };
  const lin = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const lum = c => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const h1 = q('h1');
  const heroCta = q('.hero [data-cta="primary"]');
  let covered = null;
  if (heroCta) {
    const r = heroCta.getBoundingClientRect();
    const hit = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
    covered = !(hit === heroCta || heroCta.contains(hit));
  }
  const img = q('.hero img');
  const text = document.body.innerText;
  return {
    primary_cta_count: [...document.querySelectorAll('[data-cta="primary"]')].filter(visible).length,
    hero_cta_covered: covered,
    h1_text: h1.innerText,
    h1_lines: Math.round(h1.scrollHeight / parseFloat(getComputedStyle(h1).lineHeight)),
    h1_contrast: Math.round(ratio(parse(getComputedStyle(h1).color), bgOf(h1)) * 100) / 100,
    h1_clipped: h1.scrollHeight - h1.clientHeight > 0.35 * parseFloat(getComputedStyle(h1).fontSize),
    hero_image_loaded: img ? (img.complete && img.naturalWidth > 0) : null,
    popup_visible: visible(q('[role="dialog"]')),
    has_lorem: /lorem ipsum/i.test(text),
    has_template_var: /\{\{[^}]*\}\}/.test(text),
    dollar_amounts: text.match(/\$\s?\d[\d,]*(\.\d+)?/g) || [],
    text: text,
    page_height: document.documentElement.scrollHeight,
  };
}
"""

# Checks each defect is expected to flip. Every other check must stay equal to
# the clean page for the twin to count as a one-defect twin.
INVARIANT_KEYS = ["primary_cta_count", "hero_cta_covered", "h1_contrast", "h1_clipped",
                  "hero_image_loaded", "popup_visible", "has_lorem", "has_template_var"]
EXPECTED_CHANGES = {
    "missing_cta": {"primary_cta_count", "hero_cta_covered"},
    "hidden_price": set(),
    "contradiction": set(),
    "vague_headline": set(),
    "typos": set(),
    "placeholder_text": {"has_lorem", "has_template_var"},
    "low_contrast": {"h1_contrast"},
    "broken_image": {"hero_image_loaded"},
    "blocking_popup": {"popup_visible", "hero_cta_covered"},
    "cut_off_text": {"h1_clipped"},
}


def page_id(key):
    return "p" + hashlib.sha1(f"pagetwins-{VERSION}:{key}".encode()).hexdigest()[:8]


def verify(category, info, clean, twin):
    """Return (ok, reason) for whether `twin` carries exactly its one defect."""
    for k in INVARIANT_KEYS:
        if k in EXPECTED_CHANGES[category]:
            continue
        if clean[k] != twin[k]:
            return False, f"unexpected change in {k}: {clean[k]} -> {twin[k]}"
    t = twin["text"]
    if category == "missing_cta":
        ok = clean["primary_cta_count"] > 0 and twin["primary_cta_count"] == 0
        return ok, f"primary CTAs {clean['primary_cta_count']} -> {twin['primary_cta_count']}"
    if category == "hidden_price":
        gone = all(p not in twin["dollar_amounts"] for p in info["hidden_prices"])
        present = all(p in clean["dollar_amounts"] for p in info["hidden_prices"])
        return gone and present, f"hidden {info['hidden_prices']}; remaining $ amounts {sorted(set(twin['dollar_amounts']))}"
    if category == "contradiction":
        ok = info["claim"] in t and info["claim"] not in clean["text"]
        return ok, f"claim present: {info['claim']!r}"
    if category == "vague_headline":
        return twin["h1_text"] != clean["h1_text"], f"h1 {clean['h1_text']!r} -> {twin['h1_text']!r}"
    if category == "typos":
        def has(word, text):
            return re.search(rf"\b{re.escape(word)}\b", text) is not None
        ok = all(has(w, t) for w in info["typos"]) and not any(has(w, clean["text"]) for w in info["typos"])
        return ok, f"typos present: {info['typos']}"
    if category == "placeholder_text":
        ok = (twin["has_lorem"] or twin["has_template_var"]) and not (clean["has_lorem"] or clean["has_template_var"])
        return ok, "placeholder text visible"
    if category == "low_contrast":
        ok = twin["h1_contrast"] < 1.5 and clean["h1_contrast"] >= 4.5
        return ok, f"h1 contrast {clean['h1_contrast']} -> {twin['h1_contrast']}"
    if category == "broken_image":
        ok = clean["hero_image_loaded"] and twin["hero_image_loaded"] is False
        return ok, "hero image fails to load"
    if category == "blocking_popup":
        ok = twin["popup_visible"] and twin["hero_cta_covered"] and not clean["hero_cta_covered"]
        return ok, "popup covers the hero call to action"
    if category == "cut_off_text":
        ok = twin["h1_clipped"] and not clean["h1_clipped"] and clean["h1_lines"] >= 2
        return ok, f"headline clipped ({clean['h1_lines']} lines in the clean page)"
    raise KeyError(category)


def pixel_diff(a_path, b_path):
    a, b = Image.open(a_path).convert("RGB"), Image.open(b_path).convert("RGB")
    h = min(a.height, b.height)
    box = ImageChops.difference(a.crop((0, 0, a.width, h)), b.crop((0, 0, b.width, h))).getbbox()
    if box is None and a.height == b.height:
        return None, 0.0
    if box is None:
        box = (0, h, a.width, max(a.height, b.height))
    area = (box[2] - box[0]) * (box[3] - box[1]) / (a.width * max(a.height, b.height))
    return list(box), round(area, 4)


def main():
    if OUT.exists():
        shutil.rmtree(OUT / "pages", ignore_errors=True)
    (OUT / "pages").mkdir(parents=True, exist_ok=True)

    pages = []
    for base in BASES:
        pages.append(dict(key=f"{base['id']}/clean", base=base, spec=base, flags={}, role="clean",
                          category="none", info={}))
        for cat in DEFECTS:
            spec, flags, info = make_twin(base, cat)
            pages.append(dict(key=f"{base['id']}/{cat}", base=base, spec=spec, flags=flags, role="twin",
                              category=cat, info=info))
        vspec, vinfo = make_variant(base)
        pages.append(dict(key=f"{base['id']}/harmless", base=base, spec=vspec, flags={}, role="variant",
                          category="harmless", info=vinfo))

    for pg in pages:
        pg["id"] = page_id(pg["key"])
        d = OUT / "pages" / pg["id"]
        d.mkdir(parents=True, exist_ok=True)
        svg, w, h = ART[pg["spec"]["hero"]["art"]](pg["spec"]["theme"], pg["spec"]["brand"])
        if not pg["flags"].get("broken_image"):
            (d / "hero.svg").write_text(svg, encoding="utf-8")
        (d / "index.html").write_text(render(pg["spec"], pg["flags"], hero_size=(w, h)), encoding="utf-8")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1280, "height": 800}, device_scale_factor=1)
        tab = ctx.new_page()
        for i, pg in enumerate(pages):
            d = OUT / "pages" / pg["id"]
            tab.goto((d / "index.html").as_uri(), wait_until="load")
            tab.evaluate("document.fonts.ready.then(() => true)")
            pg["checks"] = tab.evaluate(CHECKS_JS)
            (d / "page.txt").write_text(tab.evaluate(OUTLINE_JS), encoding="utf-8")
            tab.screenshot(path=str(d / "screenshot.png"), full_page=True)
            tab.screenshot(path=str(d / "first_screen.png"), full_page=False)
            if i % 20 == 0:
                print(f"rendered {i + 1}/{len(pages)}")
        browser.close()

    by_key = {pg["key"]: pg for pg in pages}
    page_rows, pair_rows, failures = [], [], []
    for pg in pages:
        im = Image.open(OUT / "pages" / pg["id"] / "screenshot.png")
        page_rows.append(dict(
            page_id=pg["id"], base_id=pg["base"]["id"], brand=pg["base"]["brand"],
            template=pg["base"]["template"], product_type=pg["base"]["kind"], role=pg["role"],
            category=pg["category"], screenshot=f"pages/{pg['id']}/screenshot.png",
            first_screen=f"pages/{pg['id']}/first_screen.png", html=f"pages/{pg['id']}/index.html",
            text=f"pages/{pg['id']}/page.txt", width=im.width, height=im.height,
        ))

    for base in BASES:
        clean = by_key[f"{base['id']}/clean"]
        ctext = (OUT / "pages" / clean["id"] / "page.txt").read_text(encoding="utf-8")
        for cat in DEFECTS:
            twin = by_key[f"{base['id']}/{cat}"]
            ok, reason = verify(cat, twin["info"], clean["checks"], twin["checks"])
            if not ok:
                failures.append(f"{twin['key']}: {reason}")
            ttext = (OUT / "pages" / twin["id"] / "page.txt").read_text(encoding="utf-8")
            box, area = pixel_diff(OUT / "pages" / clean["id"] / "screenshot.png",
                                   OUT / "pages" / twin["id"] / "screenshot.png")
            pair_rows.append(dict(
                pair_id=f"{base['id']}-{cat}", kind="defect", category=cat, base_id=base["id"],
                brand=base["brand"], template=base["template"], clean_page_id=clean["id"],
                other_page_id=twin["id"], text_visible=cat in TEXT_VISIBLE,
                text_identical=ctext == ttext, description=twin["info"]["description"],
                verified=ok, verification=reason, pixel_diff_box=json.dumps(box), pixel_diff_area=area,
            ))
        for ctype in ("identical", "harmless"):
            other = clean if ctype == "identical" else by_key[f"{base['id']}/harmless"]
            otext = (OUT / "pages" / other["id"] / "page.txt").read_text(encoding="utf-8")
            box, area = pixel_diff(OUT / "pages" / clean["id"] / "screenshot.png",
                                   OUT / "pages" / other["id"] / "screenshot.png")
            desc = ("The same page shown twice." if ctype == "identical"
                    else other["info"]["description"])
            sub = "identical" if ctype == "identical" else f"harmless_{other['info']['control_type']}"
            pair_rows.append(dict(
                pair_id=f"{base['id']}-{ctype}", kind="control", category=sub, base_id=base["id"],
                brand=base["brand"], template=base["template"], clean_page_id=clean["id"],
                other_page_id=other["id"], text_visible=True, text_identical=ctext == otext,
                description=desc, verified=True, verification="control", pixel_diff_box=json.dumps(box),
                pixel_diff_area=area,
            ))

    with open(OUT / "pages.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(page_rows[0]))
        w.writeheader()
        w.writerows(page_rows)
    with open(OUT / "pairs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(pair_rows[0]))
        w.writeheader()
        w.writerows(pair_rows)
    checks = {pg["id"]: {k: v for k, v in pg["checks"].items() if k != "text"} for pg in pages}
    (OUT / "checks.json").write_text(json.dumps(checks, indent=1), encoding="utf-8")
    (OUT / "categories.json").write_text(json.dumps(
        {"defects": DEFECTS, "text_visible": sorted(TEXT_VISIBLE), "version": VERSION}, indent=1), encoding="utf-8")

    heights = [r["height"] for r in page_rows]
    print(f"{len(page_rows)} pages, {len(pair_rows)} pairs, heights {min(heights)}-{max(heights)} px")
    if failures:
        print("VERIFICATION FAILURES:")
        for x in failures:
            print("  ", x)
        sys.exit(1)
    print("all twins verified")


if __name__ == "__main__":
    main()
