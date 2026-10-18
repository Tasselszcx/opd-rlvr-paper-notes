"""Bundle only the glyphs used by the collection, for offline reading."""
from fontTools import subset
from fontTools.ttLib import TTFont
from bs4 import BeautifulSoup
from catalog import ROOT


def write_font(documents):
    text = ''.join(BeautifulSoup(document, 'html.parser').get_text() for document in documents)
    text += (ROOT / 'assets/reader.js').read_text()
    text += ''.join(chr(i) for i in range(32, 127)) + '已读标记为再看一遍阅读详解✓→↗上一篇下一篇总览'
    options = subset.Options()
    options.flavor = 'woff2'
    options.name_IDs = ['*']
    options.name_languages = ['*']
    font = TTFont(ROOT / 'assets/fonts/NotoSansSC-variable.ttf', recalcTimestamp=False)
    worker = subset.Subsetter(options=options)
    worker.populate(text=text)
    worker.subset(font)
    font.flavor = 'woff2'
    font.save(ROOT / 'assets/fonts/paper-sans-sc.woff2')


if __name__ == '__main__':
    write_font(path.read_text() for path in ROOT.glob('*.html'))
