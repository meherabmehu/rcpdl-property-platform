"""Extract only image/logo regions; never render a screenshot as working UI."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "static/images"
OUT.mkdir(parents=True, exist_ok=True)
SOURCES = {
    "hero.jpg": ("01-home.png", (355, 102, 1024, 437)),
    "project-01.jpg": ("03-project-01-details.png", (76, 289, 685, 527)),
    "project-01-wide.jpg": ("05-gallery.png", (797, 248, 1093, 418)),
    "project-01-post.jpg": ("03-project-01-details.png", (490, 562, 683, 646)),
    "project-02.jpg": ("04-project-02-details.png", (56, 180, 806, 437)),
    "project-02-wide.jpg": ("05-gallery.png", (612, 470, 1093, 642)),
    "project-02-wall.jpg": ("04-project-02-details.png", (614, 807, 878, 917)),
    "aerial-01.jpg": ("05-gallery.png", (526, 248, 787, 417)),
    "aerial-02.jpg": ("04-project-02-details.png", (894, 807, 1157, 917)),
    "about.jpg": ("08-about-contact.png", (337, 114, 756, 456)),
    "community.jpg": ("08-about-contact.png", (284, 475, 503, 615)),
    "sunset.jpg": ("08-about-contact.png", (516, 475, 726, 615)),
    "map.jpg": ("03-project-01-details.png", (724, 665, 1021, 773)),
}
for name, (source, box) in SOURCES.items():
    Image.open(ROOT / "docs/references" / source).crop(box).save(OUT / name, quality=96)
# Cleanest full supplied logo in board 12 (no re-drawing).
Image.open(ROOT / "docs/references/12-staff-faqs-contacts.png").crop((36, 34, 395, 107)).save(OUT / "logo.png")
Image.open(ROOT / "docs/references/01-home.png").crop((38, 1479, 199, 1516)).save(OUT / "logo-white.png")
print(f"Extracted {len(SOURCES) + 2} assets")
