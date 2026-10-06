"""Draw the post cover (charts/cover.png, 1000 x 420) from a real PageTwins pair."""

from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = Path("C:/Windows/Fonts")
W, H = 1000, 420
BG, INK, MUTED, RED = "#0f172a", "#f8fafc", "#cbd5e1", "#ef4444"
BOX = (560, 100, 1240, 460)          # hero of the product page, in first-screen pixels
HEADLINE = (100, 132, 612, 238)      # the clipped headline inside BOX


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def main(title, subtitle):
    pairs = pd.read_csv(ROOT / "dataset" / "pairs.csv")
    pair = pairs[(pairs.base_id == "B05") & (pairs.category == "cut_off_text")].iloc[0]
    tile_w = 440
    scale = tile_w / (BOX[2] - BOX[0])
    tiles = []
    for page_id in (pair.clean_page_id, pair.other_page_id):
        im = Image.open(ROOT / "dataset" / "pages" / page_id / "first_screen.png").convert("RGB").crop(BOX)
        tiles.append(im.resize((tile_w, round(im.height * scale)), Image.LANCZOS))

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((40, 22), title, font=font("segoeuib.ttf", 50), fill=INK)
    d.text((42, 92), subtitle, font=font("segoeui.ttf", 23), fill=MUTED)

    gap, y0 = 40, 172
    x0 = (W - 2 * tile_w - gap) // 2
    for i, (tile, label) in enumerate(zip(tiles, ("Original", "Evil twin, one defect"))):
        x = x0 + i * (tile_w + gap)
        d.text((x, y0 - 32), label, font=font("seguisb.ttf", 19), fill=RED if i else INK)
        img.paste(tile, (x, y0))
    tx = x0 + tile_w + gap
    hx0, hy0, hx1, hy1 = (round(v * scale) for v in HEADLINE)
    d.rectangle((tx + hx0 - 5, y0 + hy0 - 5, tx + hx1 + 5, y0 + hy1 + 5), outline=RED, width=3)
    out = ROOT / "charts" / "cover.png"
    img.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main("PageTwins", "100 landing pages, one planted defect each. Did the AI graders notice?")
