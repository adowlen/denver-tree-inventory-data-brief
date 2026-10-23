"""Composite the headline figure over the generated hero illustration.
Text sits on the clean dark sky field in the upper third; a soft dark
scrim band is added behind the text for legibility."""
import pathlib
from PIL import Image, ImageDraw, ImageFont

root = pathlib.Path(__file__).resolve().parent.parent
src = root / "hero_source" / "media-generation-hero-illustration-0-c34c0d5e-10a4-49f3-a02b-a36e2b650526.webp"
img = Image.open(src).convert("RGB")
W, H = img.size
scrim = Image.new("RGB", (W, int(H * 0.36)), (18, 18, 20))
img.paste(scrim, (0, 0))
d = ImageDraw.Draw(img)

def font(size, bold=True):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p, size)

d.text((60, 46), "33,479 ash trees", font=font(int(H * 0.105)), fill=(232, 163, 61))
d.text((62, 46 + int(H * 0.135)),
       "11.0% of the trees in Denver's own inventory are ash - the genus emerald ash borer kills.",
       font=font(int(H * 0.042), bold=False), fill=(242, 242, 242))
d.text((62, 46 + int(H * 0.20)),
       "Source: Denver Open Data, park and street tree inventory (359,263 records, pulled Oct 23, 2026)",
       font=font(int(H * 0.030), bold=False), fill=(170, 200, 195))
img.save(root / "hero.png")
print("hero", img.size)
