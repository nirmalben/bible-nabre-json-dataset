import re, json, time, os, requests
from pathlib import Path
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
VCLS = re.compile(r"^[A-Za-z0-9]+-(\d+)-(\d+[a-z]*)$")

CHAPTERS_FILE = Path("data/bible-nabre-book-chapters.json")
OUTPUT_DIR = Path("generated_data/books")
OUTPUT_FILE = Path("generated_data/nabre.json")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Verses that Bible Gateway embeds at the end of the previous chapter's last verse.
# (book, from_chapter, from_verse, to_chapter, to_verse, text)
EMBEDDED_VERSES = [
    ("Wisdom", 11, 26, 12, 1,
     "for your imperishable spirit is in all things!"),
    ("Daniel", 10, 21, 11, 1,
     "and in the first year of Darius the Mede I stood to strengthen him and be his refuge."),
]


def fetch_chapter(book, ch):
    r = requests.get("https://www.biblegateway.com/passage/",
                     params={"search": f"{book} {ch}", "version": "NABRE"},
                     headers=HEADERS, timeout=30)
    r.raise_for_status()
    passage = BeautifulSoup(r.text, "html.parser").select_one(".passage-text")
    if not passage:
        raise RuntimeError(f"No passage-text for {book} {ch}")
    for el in passage.select("sup.footnote, sup.crossreference, .footnotes, .crossrefs, h3, h4"):
        el.decompose()

    verses = {}  # int verse number -> list of text parts
    for span in passage.select("span.text"):
        m = next((VCLS.match(c) for c in span.get("class", []) if VCLS.match(c)), None)
        if not m:
            continue
        for n in span.select(".versenum, .chapternum"):
            n.decompose()
        txt = " ".join(span.get_text(" ").split())
        # "1a", "1b" etc. are folded into verse 1
        num = int(re.match(r"\d+", m.group(2)).group())
        verses.setdefault(num, []).append(txt)

    return [{"verse": v, "text": " ".join(parts)} for v, parts in sorted(verses.items())]


def apply_embedded_fixes(book, chapters):
    """Split verses that the site glued onto the end of the previous verse."""
    by_num = {c["chapter"]: c for c in chapters}
    for b, from_ch, from_v, to_ch, to_v, tail in EMBEDDED_VERSES:
        if b != book:
            continue
        src, dst = by_num.get(from_ch), by_num.get(to_ch)
        if not src or not dst:
            continue

        if any(v["verse"] == to_v for v in dst["verses"]):
            continue  # already present, nothing to do

        src_verse = next((v for v in src["verses"] if v["verse"] == from_v), None)
        if src_verse and src_verse["text"].rstrip().endswith(tail):
            src_verse["text"] = src_verse["text"].rstrip()[:-len(tail)].rstrip()
            print(f"  [FIX] moved {book} {to_ch}:{to_v} out of {from_ch}:{from_v}")
        else:
            print(f"  [FIX] {book} {to_ch}:{to_v} not found at end of {from_ch}:{from_v}; "
                  f"inserting anyway, check {from_ch}:{from_v} manually")

        dst["verses"].insert(0, {"verse": to_v, "text": tail})
        dst["verses"].sort(key=lambda v: v["verse"])


def save_bible(bible):
    """Write the combined file atomically so it is always valid JSON."""
    tmp = OUTPUT_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(bible, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, OUTPUT_FILE)


meta = json.load(open(CHAPTERS_FILE))
bible = []

for entry in meta:
    book, n = entry["Book"], int(entry["Chapters"])
    book_file = OUTPUT_DIR / f"{book}.json"

    # Resume: reuse books that were already scraped
    if book_file.exists():
        print(f"Skipping {book} (already saved)")
        bible.append(json.loads(book_file.read_text(encoding="utf-8")))
        save_bible(bible)
        continue

    print(f"Processing Book: {book}")
    chapters = []

    for ch in range(1, n + 1):
        print(f"  Chapter {ch}", end="", flush=True)
        try:
            verses = fetch_chapter(book, ch)
        except Exception as e:
            print(f"  [ERROR] {e}")
            verses = []
        else:
            print(f"  ({len(verses)} verses)" + ("  [WARN] empty" if not verses else ""))
        chapters.append({"chapter": ch, "verses": verses})
        time.sleep(0.3)

    apply_embedded_fixes(book, chapters)

    book_json = {"book": book, "chapters": chapters}
    bible.append(book_json)

    # Save this book, then update the main bible file before moving on
    book_file.write_text(json.dumps(book_json, ensure_ascii=False, indent=2), encoding="utf-8")
    save_bible(bible)
    print(f"  -> saved {book} ({len(bible)} books in {OUTPUT_FILE})")

print(f"Done. Wrote {OUTPUT_FILE}")