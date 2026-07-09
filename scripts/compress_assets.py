from pathlib import Path
from PIL import Image

root = Path(r"C:\Users\BarujaFe\Projects\public-data-quality-auditor-br\assets")
for path in root.rglob("*.png"):
    img = Image.open(path).convert("RGBA")
    max_w = 512 if path.name == "icon.png" else 1600
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, int(img.height * ratio)), Image.Resampling.LANCZOS)
    img.save(path, format="PNG", optimize=True)
    kb = path.stat().st_size / 1024
    print(f"{path.relative_to(root)} -> {kb:.1f} KB ({img.size[0]}x{img.size[1]})")
