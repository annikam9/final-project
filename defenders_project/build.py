"""
build.py  —  run with: python build.py
Output: output/index.html
"""
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

sys.path.insert(0, str(Path(__file__).parent))
from utils.data_processing import load_all

BASE_DIR = Path(__file__).parent

DEFENDERS_CSV = BASE_DIR.parent / "utils" / "defenders_data.csv"
OC23_CSV      = BASE_DIR.parent / "utils" / "oc_index2023.csv"
OC25_CSV      = BASE_DIR.parent / "utils" / "oc_index2025.csv"
TEMPLATE_DIR  = "templates"
TEMPLATE_FILE = "index.html.jinja2"
OUTPUT_DIR    = Path("output")
OUTPUT_FILE   = OUTPUT_DIR / "index.html"

def main():
    print("📂  Loading and processing data …")
    data = load_all(DEFENDERS_CSV, OC23_CSV, OC25_CSV)
    print(f"    ✓ {len(data['latam_countries'])} countries · OCI 2023 + 2025 loaded")
    print("🖼   Rendering template …")
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)
    html = env.get_template(TEMPLATE_FILE).render(**data)
    OUTPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(html, encoding="utf-8")
    print(f"    ✓ Written to {OUTPUT_FILE}")
    print("\n✅  Done!  Open output/index.html in your browser.")

if __name__ == "__main__":
    main()
