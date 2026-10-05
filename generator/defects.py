"""Turn a clean base page into a one-defect twin or a harmless variant."""

import copy
import re

DESCRIPTIONS = {
    "missing_cta": "Every sign-up, download or purchase button was removed (navigation, hero, pricing cards and closing banner).",
    "hidden_price": "Paid prices were replaced with '{label}', so the page no longer says what the paid product costs.",
    "contradiction": "'{field}' now reads '{value}'. It conflicts with: {conflicts}",
    "vague_headline": "The headline '{old}' was replaced with '{new}'.",
    "typos": "Three words were misspelled in the hero: {pairs}.",
    "placeholder_text": "'{field}' now shows leftover template text: '{value}'.",
    "low_contrast": "The headline color was changed to {color}, a contrast ratio of about {ratio}:1 against the hero background.",
    "broken_image": "The hero image points to a file that does not exist, so the browser shows a broken image.",
    "blocking_popup": "A signup popup with a dark backdrop covers the first screen, including the main call to action.",
    "cut_off_text": "The headline box was given a fixed height, so its second line is cut off.",
}


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _lum(rgb):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = _lum(_hex(a)), _lum(_hex(b))
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def _mix(a, b, t):
    ra, rb = _hex(a), _hex(b)
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(ra, rb))


def low_contrast_color(theme, target=1.25):
    """Blend the headline color toward the hero background until the WCAG
    contrast ratio drops to `target`."""
    bg, fg = theme["hero_bg"], theme["text"]
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if contrast(_mix(bg, fg, mid), bg) < target:
            lo = mid
        else:
            hi = mid
    color = _mix(bg, fg, lo)
    return color, round(contrast(color, bg), 2)


def _get(spec, path):
    cur = spec
    for part in path.split("."):
        cur = cur[int(part)] if part.isdigit() else cur[part]
    return cur


def _set(spec, path, value):
    parts = path.split(".")
    if parts[-1] == "body" and parts[0] == "features":
        idx = int(parts[1])
        title, _ = spec["features"]["items"][idx]
        spec["features"]["items"][idx] = (title, value)
        return
    if parts[0] == "faq":
        idx = int(parts[1])
        q, a = spec["faq"][idx]
        spec["faq"][idx] = (value, a) if parts[2] == "q" else (q, value)
        return
    cur = spec
    for part in parts[:-1]:
        cur = cur[int(part)] if part.isdigit() else cur[part]
    cur[parts[-1]] = value


def _old_value(spec, path):
    parts = path.split(".")
    if parts[0] == "features" and parts[-1] == "body":
        return spec["features"]["items"][int(parts[1])][1]
    if parts[0] == "faq":
        q, a = spec["faq"][int(parts[1])]
        return q if parts[2] == "q" else a
    if path == "testimonial.attribution":
        t = spec["testimonial"]
        return f"{t['name']}, {t['role']}"
    return _get(spec, path)


def make_twin(base, category):
    """Return (spec, flags, info) for the twin of `base` with one defect."""
    spec = copy.deepcopy(base)
    flags = {}
    d = base["defects"]
    info = {"category": category}

    if category == "missing_cta":
        flags["no_primary_cta"] = True
        info["description"] = DESCRIPTIONS[category]

    elif category == "hidden_price":
        hp = d["hidden_price"]
        hidden = []
        for tier in spec["pricing"]["tiers"]:
            if tier["price"] != "$0":
                hidden.append(tier["price"])
                tier["price"] = hp["tier_label"]
                tier["period"] = ""
        for path, val in hp["replace"].items():
            if path == "hero.price_line" and spec["hero"].get("price_line"):
                hidden.append(spec["hero"]["price_line"][0])
            _set(spec, path, val)
        info["description"] = DESCRIPTIONS[category].format(label=hp["tier_label"])
        info["hidden_prices"] = hidden

    elif category == "contradiction":
        c = d["contradiction"]
        info["old_value"] = _old_value(spec, c["field"])
        _set(spec, c["field"], c["value"])
        info["description"] = DESCRIPTIONS[category].format(
            field=c["field"], value=c["value"], conflicts=c["conflicts_with"])
        info["claim"] = c["value"]
        info["conflicts_with"] = c["conflicts_with"]

    elif category == "vague_headline":
        old = spec["hero"]["headline"]
        spec["hero"]["headline"] = d["vague_headline"]
        info["description"] = DESCRIPTIONS[category].format(old=old, new=d["vague_headline"])

    elif category == "typos":
        pairs = []
        for field, good, bad in d["typos"]:
            text = spec["hero"][field]
            new, n = re.subn(rf"\b{re.escape(good)}\b", bad, text, count=1)
            if n != 1:
                raise ValueError(f"{base['id']}: '{good}' not found in hero.{field}")
            spec["hero"][field] = new
            pairs.append(f"{good} -> {bad}")
        info["description"] = DESCRIPTIONS[category].format(pairs=", ".join(pairs))
        info["typos"] = [bad for _, _, bad in d["typos"]]

    elif category == "placeholder_text":
        p = d["placeholder"]
        info["old_value"] = _old_value(spec, p["field"])
        _set(spec, p["field"], p["value"])
        info["description"] = DESCRIPTIONS[category].format(field=p["field"], value=p["value"])

    elif category == "low_contrast":
        color, ratio = low_contrast_color(spec["theme"])
        flags["headline_color"] = color
        info["description"] = DESCRIPTIONS[category].format(color=color, ratio=ratio)
        info["contrast_ratio"] = ratio

    elif category == "broken_image":
        flags["broken_image"] = True
        info["description"] = DESCRIPTIONS[category]

    elif category == "blocking_popup":
        flags["popup"] = d["popup"]
        info["description"] = DESCRIPTIONS[category]

    elif category == "cut_off_text":
        flags["headline_clip"] = True
        info["description"] = DESCRIPTIONS[category]

    else:
        raise KeyError(category)
    return spec, flags, info


def make_variant(base):
    """Return (spec, info) for a harmless variant that should not change quality."""
    spec = copy.deepcopy(base)
    hv = base["harmless"]
    if hv["type"] == "hue":
        old = spec["theme"]["primary"]
        spec["theme"].update(primary=hv["primary"], accent=hv["accent"], band_bg=hv["band_bg"])
        desc = (f"Brand color changed from {old} to {hv['primary']} everywhere. Button text contrast "
                f"stays at {contrast(hv['primary'], spec['theme']['primary_ink']):.1f}:1.")
    elif hv["type"] == "reorder":
        spec["features"]["items"] = list(reversed(spec["features"]["items"]))
        desc = "The three feature cards appear in reverse order."
    elif hv["type"] == "paraphrase":
        spec["hero"]["subhead"] = hv["subhead"]
        desc = "The hero subheadline was reworded with the same meaning and detail."
    else:
        raise KeyError(hv["type"])
    return spec, {"control_type": hv["type"], "description": desc}
