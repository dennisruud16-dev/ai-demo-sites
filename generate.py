import csv
import os
import re
from datetime import datetime
from string import Template

TEMPLATE_PATH = "template/index.html"
OUTPUT_DIR = "output"
CSV_PATH = "leads.csv"

def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")[:80] or "demo"

def phone_raw(phone: str) -> str:
    # keep + and digits only
    p = phone.strip()
    p = re.sub(r"(?!^\+)[^\d]", "", p)
    return p

def rating_text(rating: str) -> str:
    r = (rating or "").strip()
    return f"{r} på Google" if r else "Google rating"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        tpl = Template(f.read())

    year = str(datetime.now().year)

    made = 0
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("business_name", "").strip()
            city = row.get("city", "").strip()
            phone = row.get("phone", "").strip()
            address = row.get("address", "").strip()
            rating = row.get("rating", "").strip()
            maps_url = row.get("maps_url", "").strip() or "https://www.google.com/maps"

            if not name or not city:
                continue

            slug = slugify(f"{name}-{city}")
            out_dir = os.path.join(OUTPUT_DIR, slug)
            os.makedirs(out_dir, exist_ok=True)

            html = tpl.safe_substitute(
                business_name=name,
                city=city,
                phone=phone or "—",
                phone_raw=phone_raw(phone or ""),
                address=address or "—",
                rating_text=rating_text(rating),
                maps_url=maps_url,
                year=year,
            )

            with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as out:
                out.write(html)

            made += 1

    print(f"Generated {made} demo site(s) into ./{OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
