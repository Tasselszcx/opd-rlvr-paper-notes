"""Render the index and articles from the canonical catalog."""
import html
import re
from bs4 import BeautifulSoup
from catalog import paths

escape = html.escape


def paragraphs(items):
    return ''.join(f'<p>{escape(item)}</p>' for item in items)


def table(columns, rows, kind=''):
    header = ''.join(f'<th scope="col">{escape(str(column))}</th>' for column in columns)
    body = ''.join('<tr>' + ''.join(f'<td>{escape(str(cell))}</td>' for cell in row) + '</tr>' for row in rows)
    return f'<div class="tablewrap"><table class="{kind}"><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table></div>'


def shell(title, content, total, page_class=''):
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>{escape(title)} · OPD 与 RLVR</title>
  <link rel="stylesheet" href="assets/reader.css">
  <link rel="stylesheet" href="assets/katex/katex.min.css">
  <script defer src="assets/katex/katex.min.js"></script>
  <script defer src="assets/katex/contrib/auto-render.min.js"></script>
  <script defer src="assets/mermaid.min.js"></script>
  <script defer src="assets/reader.js"></script>
</head>
<body>
  <header class="topbar"><nav class="top" aria-label="全站导航"><a class="brand" href="index.html">PAPER NOTES / OPD × RLVR</a><span>{total} 篇论文</span></nav></header>
  <main class="{page_class}">{content}</main>
  <footer>实验数据引自原论文；论文与代码来源见各篇文末。</footer>
</body>
</html>
'''


def count_body_hanzi(body):
    soup = BeautifulSoup(body, 'html.parser')
    for node in soup.select('.math, .mermaid, .source-line, .project-more'):
        node.decompose()
    return len(re.findall(r'[\u4e00-\u9fff]', soup.get_text(' ', strip=True)))


def implementation_html(implementation):
    if not implementation:
        return '<p>未找到可确认的作者实现仓库，方法说明以论文正文和附录为依据。</p>'
    result = f'<p><a href="{escape(implementation["url"])}">作者代码仓库 ↗</a> · {escape(implementation["description"])}</p>'
    for snippet in implementation['snippets']:
        label = f'{snippet["path"]}:{snippet["start"]} · {implementation["commit"][:7]}'
        result += f'''<div class="code-item"><h3>{escape(snippet['title'])}</h3><p>{escape(snippet['explanation'])}</p>
<pre class="source"><code>{escape(snippet['code'])}</code></pre><a class="code-link" href="{escape(snippet['url'])}">{escape(label)}</a></div>'''
    return result


def article(paper, index, papers):
    files = paths(paper, index)
    publication = paper['publication']
    source_url = 'https://arxiv.org/html/' + publication['arxiv']
    total = len(papers)
    authors = ', '.join(author.split(',')[0] for author in publication['authors'][:3])
    if len(publication['authors']) > 3:
        authors += ' et al.'
    venue = ''
    if publication.get('venue'):
        venue = f'<a href="{escape(publication["venue_url"])}">{escape(publication["venue"])} ↗</a>'
    header = f'''<section class="hero">
<p class="eyebrow">{index + 1:02d} / {total:02d} · {escape(paper['category'])}</p>
<h1>{escape(paper['name'])}：{escape(paper['headline'])}</h1>
<p class="original">{escape(publication['title'])}</p>
<div class="meta"><span>{escape(authors)}</span>{venue}<span>{escape(publication['updated'])} · {escape(publication['arxiv'])}</span><a href="https://arxiv.org/abs/{publication['arxiv']}">论文 ↗</a><a href="{escape(files['pdf'])}">本地 PDF ↗</a></div>
<button class="readbtn" data-paper="{escape(paper['id'])}" aria-pressed="false">标记为已读</button>
</section>'''
    toc_items = [('example', '先看例子'), ('method', '怎么做'), ('equations', '公式解释'), ('details', '容易混淆处'), ('results', '结果'), ('connections', '论文区别')]
    toc = '<nav class="article-toc" aria-label="本文目录">' + ''.join(f'<a href="#{anchor}">{label}</a>' for anchor, label in toc_items) + '</nav>'
    method = ''
    for step_index, step in enumerate(paper['steps'], 1):
        method += f'<section class="method-block"><h3>{step_index}. {escape(step["title"])}</h3>' + paragraphs(step['paragraphs'])
        equation = step.get('equation')
        if equation:
            method += f'<div class="equation" id="equations"><h4>{escape(equation["title"])}</h4><div class="math">$${escape(equation["tex"])}$$</div><p>{escape(equation["explanation"])}</p></div>'
        method += '</section>'
    clarifications = ''.join(f'<section class="practical-detail"><h3>{escape(item["title"])}</h3><p>{escape(item["text"])}</p></section>' for item in paper['clarifications'])
    experiment_note = ''
    if paper['experiment_note']:
        experiment_note = f'<details class="project-more"><summary>实验对照建议</summary><p>{escape(paper["experiment_note"])}</p></details>'
    example = paper['example']
    results = paper['results']
    body = f'''<article id="reading-content" class="article-body">
<div class="lede">{escape(paper['summary'])}</div>
<section id="problem" class="section"><aside id="example" class="worked-example"><p class="eyebrow">说明性例子</p><h2>{escape(example['title'])}</h2>{paragraphs(example['paragraphs'])}</aside></section>
<section id="method" class="section"><h2><span>01</span>具体怎么做</h2>{table(['谁 / 什么数据', '负责什么'], paper['participants'], 'setup')}
<figure class="diagram"><figcaption>训练流程</figcaption><pre class="mermaid">{escape(paper['diagram'])}</pre></figure>{method}<p class="source-line"><a href="{source_url}#{paper['references'][0]['anchor']}">原文方法 ↗</a></p></section>
<section id="details" class="section"><h2><span>02</span>容易弄混的地方</h2>{clarifications}</section>
<section id="results" class="section"><h2><span>03</span>结果怎么样</h2>{table(results['columns'], results['rows'])}<p class="note">{escape(results['note'])} <a href="{source_url}">原文表格 ↗</a></p>{paragraphs(results['paragraphs'])}<p class="source-line"><a href="{source_url}#{paper['references'][-1]['anchor']}">原文实验 ↗</a></p></section>
<section id="connections" class="section"><h2><span>04</span>和其他论文的区别</h2><p>{escape(paper['comparison']['paragraph'])}</p>{experiment_note}</section>
<p class="endnote">{escape(paper['takeaway'])}</p>
</article>'''
    count = count_body_hanzi(body)
    if count < 1500:
        raise ValueError(f'{paper["id"]}: body has only {count} Chinese characters')
    references = ''.join(f'<a href="{source_url}#{item["anchor"]}">{escape(item["title"])} ↗</a>' for item in paper['references'])
    sources = f'<details class="sources"><summary>论文与代码来源</summary><div class="evidence">{references}<a href="{files["source"]}/readable.txt">本地全文文字</a></div>{implementation_html(paper["implementation"])}</details>'
    pager = ''
    for target, label in [(index - 1, '上一篇'), (index + 1, '下一篇')]:
        if 0 <= target < total:
            href, name = paths(papers[target], target)['html'], papers[target]['name']
        else:
            href, name, label = 'index.html', '论文总览', '回到总览'
        pager += f'<a href="{escape(href)}"><small>{label}</small>{escape(name)}</a>'
    return shell(paper['name'], header + toc + body + sources + '<nav class="pager" aria-label="相邻论文">' + pager + '</nav>', total), count


def index(papers):
    cards = ''
    rows = []
    for number, paper in enumerate(papers):
        files = paths(paper, number)
        cards += f'''<a class="card" href="{files['html']}" data-paper="{escape(paper['id'])}" data-group="{escape(paper['category'])}"><div class="card-top"><span class="number">{number + 1:02d}</span><span class="tag">{escape(paper['category'])}</span></div><h2>{escape(paper['name'])}</h2><p class="chinese">{escape(paper['headline'])}</p><p>{escape(paper['summary'])}</p><div class="go">阅读详解 →</div></a>'''
        rows.append([paper['name']] + paper['comparison']['cells'])
    categories = ['全部'] + list(dict.fromkeys(paper['category'] for paper in papers))
    buttons = ''.join(f'<button class="filter{" active" if category == "全部" else ""}" aria-pressed="{"true" if category == "全部" else "false"}">{escape(category)}</button>' for category in categories)
    content = f'''<section class="hero"><p class="eyebrow">PAPER COLLECTION</p><h1>OPD 与 RLVR</h1><p class="intro">{len(papers)} 篇论文的具体做法、训练步骤与实验结果。</p></section>
<section class="glossary" aria-label="基本概念"><div><h2>OPD：学生自己写，老师给反馈</h2><p>学生生成回答，老师看着已生成的内容，给下一 token 的概率或目标。学生据此更新。</p></div><div><h2>RLVR：用可验证结果学习</h2><p>学生先回答或行动，再根据答案检查、代码测试或环境结果获得奖励，用这些奖励更新模型。</p></div></section>
<div class="toolbar" aria-label="论文筛选">{buttons}<input class="search" type="search" placeholder="搜索论文或关键词" aria-label="搜索论文"></div>
<section class="cards" aria-label="论文列表">{cards}</section><p class="noresults" hidden>没有匹配的论文。</p>
<section class="section compare"><h2>方法对照</h2>{table(['论文', '具体做什么', '老师或数据', '关键区别'], rows, 'comparison')}<p class="note">不同论文的模型、任务和训练量不同，这里比较做法，不直接比较分数。</p></section>'''
    return shell('论文总览', content, len(papers), 'index')
