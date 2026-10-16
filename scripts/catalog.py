"""Load the paper collection. List order is the collection's only ordering source."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_papers():
    papers = json.loads((ROOT / 'data/papers.json').read_text())
    ids = [paper['id'] for paper in papers]
    arxiv = [paper['publication']['arxiv'] for paper in papers]
    if len(ids) != len(set(ids)) or len(arxiv) != len(set(arxiv)):
        raise ValueError('Duplicate paper in the catalog')
    return papers


def paths(paper, index):
    stem = f'{index + 1:02d}-{paper["id"]}'
    return {
        'stem': stem,
        'html': stem + '.html',
        'pdf': '原文PDF/' + stem + '--' + paper['publication']['arxiv'] + '.pdf',
        'source': 'sources/' + stem,
    }
