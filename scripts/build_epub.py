#!/usr/bin/env python3
"""Build a single EPUB from the chapter PDFs in chapters/.

README.md's chapter table is the source of truth for chapter order,
titles, and authors -- this script does not hardcode a chapter list.

Usage:
    pip install -r scripts/requirements.txt
    python3 scripts/build_epub.py

Re-run this any time a PDF in chapters/ is added or replaced, or the
README chapter table changes: it always rebuilds the EPUB from scratch.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import uuid
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("Missing dependency: run 'pip install -r scripts/requirements.txt' first (PyMuPDF).")

try:
    from ebooklib import epub
except ImportError:
    sys.exit("Missing dependency: run 'pip install -r scripts/requirements.txt' first (EbookLib).")

REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"
DEFAULT_OUTPUT = REPO_ROOT / "epub" / "Hands-on-ML-Azerbaijani.epub"
BOOK_IDENTIFIER_SEED = "https://github.com/Lala2398/Hands_on_ML_Azerbaijani"

# PyMuPDF span flag bits (see: page.get_text("dict") docs)
ITALIC_FLAG = 1 << 1
BOLD_FLAG = 1 << 4

# Embedded PNGs from the source PDFs are lossless screenshots/plots and can
# run 300-1000+ KB each; with ~370 of them across all chapters that would put
# the combined EPUB well past GitHub's 100 MB per-file limit. Downscaling and
# re-encoding as JPEG keeps things readable while landing in the tens of MB.
MAX_IMAGE_DIM = 1400
JPEG_QUALITY = 80

# Matches rows like: | 1 | The Machine Learning Landscape | [PDF](chapters/Chapter_01.pdf) | Some Author |
TABLE_ROW_RE = re.compile(
    r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*\[PDF\]\(([^)]+)\)\s*\|\s*([^|]+?)\s*\|\s*$",
    re.MULTILINE,
)
TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


@dataclass
class Chapter:
    number: str  # "—" for the introduction, otherwise "1".."19"
    title: str
    pdf_path: Path
    authors: str

    @property
    def asset_prefix(self) -> str:
        return "intro" if self.number == "—" else f"ch{int(self.number):02d}"

    @property
    def nav_label(self) -> str:
        label = "Giriş" if self.number == "—" else f"Fəsil {self.number}"
        return f"{label} — {self.title}"


def parse_readme(readme_text: str) -> tuple[str, list[Chapter]]:
    title_match = TITLE_RE.search(readme_text)
    book_title = (
        title_match.group(1).strip()
        if title_match
        else "Hands-on Machine Learning — Azerbaijani Notes & Summaries"
    )

    chapters = []
    for match in TABLE_ROW_RE.finditer(readme_text):
        number, title, pdf_rel, authors = (g.strip() for g in match.groups())
        pdf_path = (REPO_ROOT / pdf_rel).resolve()
        if not pdf_path.is_file():
            continue
        chapters.append(Chapter(number=number, title=title, pdf_path=pdf_path, authors=authors))
    return book_title, chapters


def render_line(spans: list[dict]) -> str:
    parts = []
    for span in spans:
        text = span.get("text", "")
        if not text:
            continue
        text = html.escape(text)
        if span["flags"] & BOLD_FLAG:
            text = f"<b>{text}</b>"
        if span["flags"] & ITALIC_FLAG:
            text = f"<i>{text}</i>"
        parts.append(text)
    return "".join(parts)


def optimize_image(data: bytes) -> tuple[bytes, str]:
    """Downscale + re-encode an embedded image to keep the EPUB a reasonable
    size. Falls back to the original bytes untouched if anything goes wrong
    (e.g. an unusual colorspace), so a single odd image can't break the build.
    """
    try:
        pix = fitz.Pixmap(data)
        if pix.alpha:
            pix = fitz.Pixmap(pix, 0)  # drop alpha channel, JPEG has none
        if pix.colorspace is None or pix.colorspace.n not in (1, 3):
            pix = fitz.Pixmap(fitz.csRGB, pix)  # normalize e.g. CMYK -> RGB
        max_dim = max(pix.width, pix.height)
        if max_dim > MAX_IMAGE_DIM:
            scale = MAX_IMAGE_DIM / max_dim
            pix = fitz.Pixmap(pix, max(1, round(pix.width * scale)), max(1, round(pix.height * scale)))
        return pix.tobytes("jpeg", jpg_quality=JPEG_QUALITY), "jpg"
    except Exception:
        return data, ""


def extract_chapter_body(
    pdf_path: Path, asset_prefix: str, optimize_images: bool = True
) -> tuple[str, list[tuple[str, bytes]]]:
    """Walk a PDF in reading order, turning text into headings/paragraphs
    (using font size/weight as heuristics) and embedded images into <img>
    tags, so the result is a reflowable EPUB chapter rather than page scans.
    """
    doc = fitz.open(pdf_path)

    size_counter: Counter[int] = Counter()
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["text"].strip():
                        size_counter[round(span["size"])] += len(span["text"])
    body_size = size_counter.most_common(1)[0][0] if size_counter else 12

    html_parts: list[str] = []
    images: list[tuple[str, bytes]] = []
    img_index = 0

    for page in doc:
        blocks = sorted(page.get_text("dict")["blocks"], key=lambda b: (round(b["bbox"][1]), b["bbox"][0]))
        for block in blocks:
            if block["type"] == 1:
                data = block.get("image")
                if not data:
                    continue
                img_index += 1
                ext = (block.get("ext") or "png").lower()
                if optimize_images:
                    data, new_ext = optimize_image(data)
                    ext = new_ext or ext
                fname = f"{asset_prefix}_{img_index:03d}.{ext}"
                images.append((fname, data))
                html_parts.append(f'<div class="figure"><img src="images/{fname}" alt="" /></div>')
                continue

            # Buffer consecutive lines of the same kind (heading level, or
            # body text) so a heading/paragraph that wraps across several
            # PDF lines becomes one <h2>/<h3>/<p>, not one tag per line.
            buffer: list[str] = []
            buffer_tag = "p"

            def flush() -> None:
                if buffer:
                    html_parts.append(f"<{buffer_tag}>{' '.join(buffer)}</{buffer_tag}>")
                    buffer.clear()

            for line in block["lines"]:
                spans = [s for s in line["spans"] if s.get("text")]
                text_only = "".join(s["text"] for s in spans).strip()
                if not text_only:
                    flush()
                    buffer_tag = "p"
                    continue

                max_size = max(round(s["size"]) for s in spans)
                is_bold = all(s["flags"] & BOLD_FLAG for s in spans)
                is_heading = len(text_only) <= 120 and (
                    max_size >= body_size + 3 or (is_bold and max_size >= body_size)
                )
                tag = ("h2" if max_size >= body_size + 8 else "h3") if is_heading else "p"

                if buffer and tag != buffer_tag:
                    flush()
                buffer_tag = tag
                buffer.append(render_line(spans))
            flush()

    doc.close()
    return "\n".join(html_parts), images


CSS = """
body { font-family: serif; line-height: 1.5; margin: 1em; }
h1 { text-align: center; }
h2, h3 { margin-top: 1.5em; }
.byline { font-style: italic; color: #555; margin-bottom: 2em; text-align: center; }
.figure { text-align: center; margin: 1em 0; }
.figure img { max-width: 100%; height: auto; }
"""

IMAGE_MEDIA_TYPES = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}


def build_epub(
    book_title: str, chapters: list[Chapter], output_path: Path, optimize_images: bool = True
) -> None:
    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid5(uuid.NAMESPACE_URL, BOOK_IDENTIFIER_SEED)))
    book.set_title(book_title)
    book.set_language("az")
    book.add_author("Hands-on ML Azerbaijani contributors")

    css_item = epub.EpubItem(
        uid="style", file_name="style/style.css", media_type="text/css", content=CSS
    )
    book.add_item(css_item)

    epub_chapters = []
    for chapter in chapters:
        print(f"  {chapter.pdf_path.relative_to(REPO_ROOT)} -> {chapter.nav_label}", file=sys.stderr)
        body_html, images = extract_chapter_body(chapter.pdf_path, chapter.asset_prefix, optimize_images)

        item = epub.EpubHtml(
            title=chapter.nav_label,
            file_name=f"{chapter.asset_prefix}.xhtml",
            lang="az",
        )
        item.content = (
            f"<h1>{html.escape(chapter.nav_label)}</h1>\n"
            f'<p class="byline">{html.escape(chapter.authors)}</p>\n'
            f"{body_html}"
        )
        item.add_item(css_item)
        book.add_item(item)
        epub_chapters.append(item)

        for fname, data in images:
            ext = fname.rsplit(".", 1)[-1].lower()
            image_item = epub.EpubItem(
                uid=f"img_{fname}",
                file_name=f"images/{fname}",
                media_type=IMAGE_MEDIA_TYPES.get(ext, "image/png"),
                content=data,
            )
            book.add_item(image_item)

    book.toc = tuple(epub_chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav"] + epub_chapters

    output_path.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(output_path), book)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--readme", type=Path, default=README_PATH, help="Path to README.md (default: repo README)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output .epub path")
    parser.add_argument(
        "--only",
        type=str,
        default=None,
        help="Comma-separated chapter numbers to build, e.g. '—,1,2' (for quick testing)",
    )
    parser.add_argument(
        "--no-optimize-images",
        action="store_true",
        help="Keep original embedded images as-is instead of downscaling/re-encoding them (much larger output)",
    )
    args = parser.parse_args()

    readme_text = args.readme.read_text(encoding="utf-8")
    book_title, chapters = parse_readme(readme_text)

    if not chapters:
        sys.exit(f"No chapters found in {args.readme} matching the expected table format.")

    if args.only:
        wanted = {n.strip() for n in args.only.split(",")}
        chapters = [c for c in chapters if c.number in wanted]

    print(f"Found {len(chapters)} chapter(s) to build.", file=sys.stderr)
    build_epub(book_title, chapters, args.output, optimize_images=not args.no_optimize_images)
    try:
        shown_path = args.output.relative_to(REPO_ROOT)
    except ValueError:
        shown_path = args.output
    print(f"Wrote {shown_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
