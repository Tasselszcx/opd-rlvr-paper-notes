"""Download the catalog's pinned original PDFs with paper-search pacing."""
import hashlib
import re
import unicodedata
from pathlib import Path
from pypdf import PdfReader
from paper_search_mcp.academic_platforms.arxiv import ArxivSearcher
from catalog import ROOT, load_papers, paths


def normalize(text):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', text).lower())


def main():
    destination = ROOT / '原文PDF'
    destination.mkdir(exist_ok=True)
    source = ArxivSearcher()
    for number, paper in enumerate(load_papers()):
        target = ROOT / paths(paper, number)['pdf']
        if not target.exists():
            downloaded = Path(source.download_pdf(paper['publication']['arxiv'], str(destination)))
            reader = PdfReader(downloaded)
            text = (reader.pages[0].extract_text() or '') + str(reader.metadata.title or '')
            assert normalize(paper['publication']['title']) in normalize(text)
            assert hashlib.sha256(downloaded.read_bytes()).hexdigest() == paper['pdf']['sha256']
            downloaded.rename(target)
        assert hashlib.sha256(target.read_bytes()).hexdigest() == paper['pdf']['sha256']
        print(target.name, 'verified', flush=True)


if __name__ == '__main__':
    main()
