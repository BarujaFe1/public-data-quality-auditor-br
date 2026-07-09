from pathlib import Path
from PIL import Image

root = Path(r"C:\Users\BarujaFe\Projects\public-data-quality-auditor-br\assets")

# Keep icon as optimized PNG; convert large banners/screenshots to JPEG
jpeg_names = {
    "hero-cover.png",
    "architecture-pipeline.png",
    "social-preview.png",
    "01-audit-summary.png",
    "02-issues-register.png",
    "03-column-profile.png",
    "04-data-dictionary.png",
}

for path in list(root.rglob("*.png")):
    if path.name not in jpeg_names:
        continue
    img = Image.open(path).convert("RGB")
    max_w = 1400
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, int(img.height * ratio)), Image.Resampling.LANCZOS)
    out = path.with_suffix(".jpg")
    img.save(out, format="JPEG", quality=82, optimize=True)
    path.unlink()
    kb = out.stat().st_size / 1024
    print(f"{out.relative_to(root)} -> {kb:.1f} KB ({img.size[0]}x{img.size[1]})")
