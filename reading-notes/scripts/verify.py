"""Check the final collection, its sources, and desktop/mobile rendering."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from catalog import ROOT, load_papers, paths
from render import count_body_hanzi

EXPECTED = ['rise', 'soar', 'near-future', 'sequential', 'opw', 'metaopd', 'pear', 'dr-opd', 'op-short', 'rl-before-rl', 'atesd']
PROCESS_TEXT = ['原编号', '排名', '新增论文', '新增三篇', '新增 3 篇', '按你给定', '阅读顺序', '直白讲解版', '方法详解版', '原文件编号', '已确认并读取', '下方保留原来的']
OUT = ROOT / 'qa'


def verify_files(papers):
    assert [paper['id'] for paper in papers] == EXPECTED
    expected_pages = {'index.html'} | {paths(paper, i)['html'] for i, paper in enumerate(papers)}
    assert {path.name for path in ROOT.glob('*.html')} == expected_pages
    manifest = json.loads((ROOT / 'sources/manifest.json').read_text())
    assert set(manifest['outputs']) == expected_pages
    assert [row['id'] for row in manifest['papers']] == EXPECTED
    assert len(list((ROOT / '原文PDF').glob('*.pdf'))) == len(papers)
    index = BeautifulSoup((ROOT / 'index.html').read_text(), 'html.parser')
    assert [node['data-paper'] for node in index.select('.card')] == EXPECTED
    for number, paper in enumerate(papers):
        files = paths(paper, number)
        pdf = ROOT / files['pdf']
        assert hashlib.sha256(pdf.read_bytes()).hexdigest() == paper['pdf']['sha256']
        assert (ROOT / files['source'] / 'html.html').is_file()
        soup = BeautifulSoup((ROOT / files['html']).read_text(), 'html.parser')
        body = soup.select_one('#reading-content')
        assert count_body_hanzi(str(body)) >= 1500
        assert len(body.select('.method-block')) == 5
        assert len(body.select('.equation')) == 1
        assert str(body).index('id="example"') < str(body).index('id="method"')
        previous = paths(papers[number - 1], number - 1)['html'] if number else 'index.html'
        following = paths(papers[number + 1], number + 1)['html'] if number + 1 < len(papers) else 'index.html'
        assert [link['href'] for link in soup.select('.pager a')] == [previous, following]
        assert soup.find('a', href=files['pdf'])
    for filename in expected_pages:
        soup = BeautifulSoup((ROOT / filename).read_text(), 'html.parser')
        assert soup.html['lang'] == 'zh-CN' and len(soup.find_all('h1')) == 1
        visible_text = soup.get_text(' ', strip=True)
        for phrase in PROCESS_TEXT:
            assert phrase not in visible_text, (filename, phrase)
        styles = [link['href'] for link in soup.select('link[rel="stylesheet"]')]
        assert styles == ['assets/reader.css', 'assets/katex/katex.min.css']
        for tag, attribute in [('a', 'href'), ('link', 'href'), ('script', 'src')]:
            for node in soup.find_all(tag):
                url = urlsplit(node.get(attribute, ''))
                if url.scheme or url.netloc:
                    continue
                if url.path:
                    assert (ROOT / unquote(url.path)).exists(), (filename, url.path)
                elif url.fragment:
                    assert soup.find(id=unquote(url.fragment)), (filename, url.fragment)
    scripts = {path.name for path in (ROOT / 'scripts').glob('*.py')}
    assert scripts == {'build.py', 'catalog.py', 'render.py', 'verify.py', 'subset_font.py', 'download_originals.py'}
    assert not (ROOT / 'assets/style.css').exists()
    assert not (ROOT / 'assets/app.js').exists()


def verify_browser(papers):
    OUT.mkdir(exist_ok=True)
    snapshots = set()
    results = []
    pages = ['index.html'] + [paths(paper, i)['html'] for i, paper in enumerate(papers)]
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless=True, timeout=20000)
        for width, height, label in [(1440, 1050, 'desktop'), (390, 844, 'mobile')]:
            context = browser.new_context(viewport={'width': width, 'height': height}, device_scale_factor=1)
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            for filename in pages:
                errors.clear()
                page.goto((ROOT / filename).as_uri(), wait_until='load', timeout=20000)
                page.wait_for_function("document.body.dataset.ready === 'true'", timeout=20000)
                state = page.evaluate('''() => ({width:innerWidth, scroll:document.documentElement.scrollWidth, diagrams:document.querySelectorAll('.mermaid svg').length, mathErrors:document.querySelectorAll('.katex-error').length, formula:document.querySelectorAll('.katex').length, fontLoaded:document.fonts.check('16px "Paper Sans"'), bodyFont:document.querySelector('.article-body')?getComputedStyle(document.querySelector('.article-body')).fontSize:null})''')
                assert not errors, (filename, errors)
                assert state['scroll'] <= width, (filename, label, state)
                assert state['fontLoaded']
                if filename != 'index.html':
                    assert state['diagrams'] == 1 and state['formula'] == 1 and state['mathErrors'] == 0
                    assert state['bodyFont'] == '16px'
                    state['formulaOverflow'] = page.locator('.math').evaluate_all('(nodes)=>nodes.map(node=>node.scrollWidth>node.clientWidth)')
                    assert not any(state['formulaOverflow']), (filename, label, 'formula overflow')
                    page.locator('.article-toc a[href="#method"]').click()
                    page.wait_for_function("Math.abs(document.querySelector('#method').getBoundingClientRect().top-parseFloat(getComputedStyle(document.querySelector('#method')).scrollMarginTop))<4", timeout=5000)
                    page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
                    page.get_by_role('button', name='标记为已读', exact=True).click()
                    assert page.get_by_role('button', name='已读 ✓', exact=True).get_attribute('aria-pressed') == 'true'
                    page.get_by_role('button', name='已读 ✓', exact=True).click()
                else:
                    for category in dict.fromkeys(paper['category'] for paper in papers):
                        page.get_by_role('button', name=category, exact=True).click()
                        assert page.locator('.card:not([hidden])').count() == sum(paper['category'] == category for paper in papers)
                    page.get_by_role('button', name='全部', exact=True).click()
                    page.get_by_role('searchbox').fill('RISE')
                    assert page.locator('.card:not([hidden])').count() == 1
                    page.get_by_role('searchbox').fill('')
                    assert page.locator('.card:not([hidden])').count() == len(papers)
                page.evaluate('document.activeElement.blur()')
                image = f'{Path(filename).stem}-{label}.png'
                page.screenshot(path=str(OUT / image), full_page=True)
                snapshots.add(image)
                results.append({'file': filename, 'viewport': label, **state})
                print(filename, label, 'PASS', flush=True)
            context.close()
        browser.close()
    for path in OUT.glob('*'):
        if path.is_file() and path.name not in snapshots | {'verification.json'}:
            path.unlink()
    (OUT / 'verification.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    print('PASS: canonical catalog, final file names, 24 viewport checks, local links, 16px text, and PDF checksums.')


if __name__ == '__main__':
    papers = load_papers()
    verify_files(papers)
    verify_browser(papers)
