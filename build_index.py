import os
import re
import urllib.parse
from datetime import datetime

# 1. 主页模板 (index.html)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>投研档案库</title>
    <style>
        :root { --primary: #2563eb; --bg: #f8fafc; --card: #ffffff; --text: #334155; --text-light: #64748b; --border: #e2e8f0; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); max-width: 1000px; margin: 0 auto; padding: 40px 20px; line-height: 1.6; }
        header { margin-bottom: 30px; }
        h1 { font-size: 2.2rem; color: #0f172a; margin-bottom: 8px; font-weight: 700; }
        .meta { color: var(--text-light); margin-bottom: 24px; font-size: 0.95rem; }
        .search-box { width: 100%; padding: 14px 18px; border: 1px solid var(--border); border-radius: 8px; font-size: 1rem; margin-bottom: 24px; box-sizing: border-box; background: var(--card); transition: all 0.2s; box-shadow: 0 1px 2px rgba(0,0,0,0.02); }
        .search-box:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
        .filters { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 30px; }
        .filter-btn { padding: 8px 18px; background: var(--card); border: 1px solid var(--border); border-radius: 20px; cursor: pointer; color: var(--text); font-size: 0.9rem; transition: all 0.2s; }
        .filter-btn:hover { background: #f1f5f9; }
        .filter-btn.active { background: var(--primary); color: white; border-color: var(--primary); }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; align-items: stretch; }
        .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 24px; text-decoration: none; color: inherit; display: flex; flex-direction: column; transition: transform 0.2s, box-shadow 0.2s; }
        .card:hover { transform: translateY(-4px); box-shadow: 0 12px 20px -8px rgba(0,0,0,0.1); border-color: #cbd5e1; }
        .card-cat { font-size: 0.8rem; background: #eff6ff; color: var(--primary); padding: 4px 10px; border-radius: 6px; align-self: flex-start; margin-bottom: 12px; font-weight: 500; }
        .card-title { font-size: 1.1rem; font-weight: 600; margin: 0 0 10px 0; color: #0f172a; line-height: 1.4; word-break: break-all; }
        .card-excerpt { font-size: 0.85rem; color: var(--text-light); flex-grow: 1; margin-bottom: 15px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
        .card-date { font-size: 0.85rem; color: var(--text-light); border-top: 1px solid var(--border); padding-top: 12px; display: flex; align-items: center; gap: 6px; }
        .hidden { display: none !important; }
        #no-results { display: none; text-align: center; color: var(--text-light); grid-column: 1 / -1; padding: 60px 20px; border: 1px dashed var(--border); border-radius: 12px; }
        footer { text-align: center; margin-top: 60px; color: var(--text-light); font-size: 0.9rem; }
    </style>
</head>
<body>
    <header>
        <h1>📚 投研档案库</h1>
        <div class="meta">已按时间倒序排列 · 共 __TOTAL__ 份报告</div>
        <input type="text" id="search" class="search-box" placeholder="🔍 搜索报告名称、内容或分类...">
    </header>
    <div class="filters">
        <button class="filter-btn active" data-filter="all">全部</button>
        __FILTERS__
    </div>
    <div class="grid" id="grid">
        __CARDS__
        <div id="no-results">📭 没有找到匹配的报告。</div>
    </div>
    <footer>最后更新：__TIME__</footer>
    <script>
        const search = document.getElementById('search');
        const btns = document.querySelectorAll('.filter-btn');
        const cards = document.querySelectorAll('.card');
        const noRes = document.getElementById('no-results');
        let curFilter = 'all';
        let q = '';
        function update() {
            let vis = 0;
            cards.forEach(c => {
                const matchF = (curFilter === 'all' || c.dataset.cat === curFilter);
                const matchQ = c.innerText.toLowerCase().includes(q);
                if (matchF && matchQ) { c.classList.remove('hidden'); vis++; }
                else { c.classList.add('hidden'); }
            });
            noRes.style.display = vis === 0 ? 'block' : 'none';
        }
        search.addEventListener('input', e => { q = e.target.value.toLowerCase(); update(); });
        btns.forEach(b => b.addEventListener('click', () => {
            btns.forEach(x => x.classList.remove('active'));
            b.classList.add('active');
            curFilter = b.dataset.filter;
            update();
        }));
    </script>
</body>
</html>
"""

# 2. 注入报告页面的导航栏代码
NAV_HTML = """
<nav id="auto-nav" style="padding: 15px 20px; background: #fff; border-bottom: 1px solid #e2e8f0; margin: -8px -8px 20px -8px; font-family: -apple-system, sans-serif; display: flex; align-items: center; position: sticky; top: 0; z-index: 999;">
    <a href="../index.html" style="text-decoration: none; color: #2563eb; font-weight: 600; display: flex; align-items: center; gap: 5px;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
        返回档案库主页
    </a>
</nav>
"""

def process_report_file(filepath):
    """为报告文件注入返回按钮"""
    title = os.path.basename(filepath).replace('.html', '')
    excerpt = "点击查看报告详情..."
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # 1. 提取摘要逻辑
        p_matches = re.findall(r'<p.*?>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
        for p in p_matches:
            clean_p = re.sub(r'<[^>]+>', '', p).strip()
            if len(clean_p) > 20:
                excerpt = clean_p[:120] + "..." if len(clean_p) > 120 else clean_p
                break
        
        # 2. 注入导航栏逻辑（如果还没注入过）
        if 'id="auto-nav"' not in content:
            # 在 <body> 标签后插入导航栏
            new_content = re.sub(r'(<body.*?>)', r'\1' + NAV_HTML, content, flags=re.IGNORECASE)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
    except Exception as e:
        print(f"处理文件 {filepath} 出错: {e}")
        
    return title, excerpt

def run():
    all_reports = []
    cats = set()
    
    for root, _, files in os.walk('.'):
        if '.git' in root or root == '.': continue
        cat = os.path.basename(root)
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                path = os.path.join(root, file)
                # 处理并注入导航
                title, excerpt = process_report_file(path)
                
                url = urllib.parse.quote(path.replace(os.sep, '/').removeprefix('./'))
                mtime = os.path.getmtime(path)
                date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                
                cats.add(cat)
                all_reports.append({
                    'title': title, 'url': url, 'date': date_str, 
                    'mtime': mtime, 'cat': cat, 'excerpt': excerpt
                })

    all_reports.sort(key=lambda x: x['mtime'], reverse=True)

    cards_html = ""
    for r in all_reports:
        cards_html += f'<a href="{r["url"]}" class="card" data-cat="{r["cat"]}"><div class="card-cat">{r["cat"]}</div><h3 class="card-title">{r["title"]}</h3><div class="card-excerpt">{r["excerpt"]}</div><div class="card-date">📅 {r["date"]}</div></a>'
    
    f_btns = "".join([f'<button class="filter-btn" data-filter="{c}">{c}</button>' for c in sorted(cats)])
    
    html = HTML_TEMPLATE.replace('__TOTAL__', str(len(all_reports))).replace('__FILTERS__', f_btns).replace('__CARDS__', cards_html).replace('__TIME__', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    with open('index.html', 'w', encoding='utf-8') as f: f.write(html)
    print(f"✅ 完成！共更新 {len(all_reports)} 份报告。所有页面已添加“返回主页”按钮。")

if __name__ == "__main__":
    run()
