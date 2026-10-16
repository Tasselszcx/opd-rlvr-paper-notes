"""Build the complete collection from data/papers.json."""
import hashlib
import json
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup
from catalog import ROOT, load_papers, paths
from render import article, index
from subset_font import write_font


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    papers = load_papers()
    documents = {'index.html': index(papers)}
    source_records, pdf_records = [], []
    for number, paper in enumerate(papers):
        files = paths(paper, number)
        pdf = ROOT / files['pdf']
        assert pdf.is_file(), pdf
        digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
        assert digest == paper['pdf']['sha256'], (paper['id'], 'PDF checksum mismatch')
        source_dir = ROOT / files['source']
        source_html = BeautifulSoup((source_dir / 'html.html').read_text(), 'html.parser')
        anchors = {tag['id'] for tag in source_html.select('[id]')}
        for reference in paper['references']:
            assert reference['anchor'] in anchors, (paper['id'], reference)
        document, count = article(paper, number, papers)
        documents[files['html']] = document
        source_records.append({
            'id': paper['id'], 'file': files['html'], 'name': paper['name'],
            'title': paper['publication']['title'], 'version': paper['publication']['arxiv'],
            'source': 'https://arxiv.org/html/' + paper['publication']['arxiv'],
            'source_directory': files['source'], 'main_hanzi': count,
        })
        pdf_records.append({
            'file': pdf.name, 'title': paper['publication']['title'],
            'version': paper['publication']['arxiv'],
            'url': 'https://arxiv.org/pdf/' + paper['publication']['arxiv'],
            'pages': paper['pdf']['pages'], 'bytes': pdf.stat().st_size, 'sha256': digest,
        })

    # Check the complete output set before replacing any public page.
    for filename, document in documents.items():
        soup = BeautifulSoup(document, 'html.parser')
        for tag, attribute in [('a', 'href'), ('link', 'href'), ('script', 'src')]:
            for node in soup.find_all(tag):
                url = urlsplit(node.get(attribute, ''))
                if url.scheme or url.netloc:
                    continue
                target = unquote(url.path)
                if target and target not in documents:
                    assert (ROOT / target).exists(), (filename, target)
                if not target and url.fragment:
                    assert soup.find(id=unquote(url.fragment)), (filename, url.fragment)
    write_font(documents.values())
    manifest_path = ROOT / 'sources/manifest.json'
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    previous_outputs = previous.get('outputs', []) if isinstance(previous, dict) else []
    with tempfile.TemporaryDirectory(prefix='.build-', dir=ROOT) as temporary:
        staging = Path(temporary)
        for filename, document in documents.items():
            (staging / filename).write_text(document)
        for filename in documents:
            (staging / filename).replace(ROOT / filename)
    for filename in previous_outputs:
        if filename not in documents:
            path = ROOT / filename
            assert path.parent == ROOT and path.suffix == '.html'
            path.unlink(missing_ok=True)
    write_json(manifest_path, {'outputs': list(documents), 'papers': source_records})
    write_json(ROOT / '原文PDF/manifest.json', pdf_records)
    for row in source_records:
        print(row['file'], row['main_hanzi'], '正文汉字')
    print('Built', len(documents), 'HTML files from one catalog.')


if __name__ == '__main__':
    main()
