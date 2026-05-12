import os
import re
import urllib.parse
from datetime import datetime

# ==========================================
# 1. 核心 HTML 模板 (已新增搜索框 CSS 与核心 JS 逻辑)
# ==========================================
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>投研档案库</title>
    <style>
        :root {{ --primary: #0f172a; --bg: #f8fafc; --card-bg: #ffffff; --text: #334155; --text-light: #64748b; --border: #e2e8f0; --hover: #f1f5f9; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: var(--bg); color: var(--text); max-width: 1000px; margin: 0 auto; padding: 40px 20px; line-height: 1.6; }}
        
        /* 头部与搜索栏样式 */
        header {{ border-bottom: 2px solid var(--border); padding-bottom: 20px; margin-bottom: 20px; }}
        h1 {{ color: var(--primary); font-size: 2.2em; margin: 0 0 10px 0; }}
        .site-meta {{ color: var(--text-light); font-size: 0.95em; margin-bottom: 15px; }}
        
        .search-container {{ margin-bottom: 20px; }}
        .search-input {{ width: 100%; max-width: 100%; box-sizing: border-box; padding: 12px 20px; border: 1px solid var(--border); border-radius: 8px; font-size: 1rem; color: var(--text); background-color: var(--card-bg); transition: all 0.2s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }}
        .search-input:focus {{ outline: none; border-color: #94a3b8; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
        
        /* 分类过滤器 */
        .filters {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 30px; }}
        .filter-btn {{ padding: 8px 16px; border: 1px solid var(--border); background: var(--card-bg); border-radius: 20px; cursor: pointer; font-size: 0.9em; font-weight: 500; color: var(--text); transition: all 0.2s ease; }}
        .filter-btn:hover {{ background: var(--hover); }}
        .filter-btn.active {{ background: var(--primary); color: white; border-color: var(--primary); }}
        
        /* 卡片网格布局 */
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        
        /* 单个卡片样式 */
        .card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 20px; transition: transform 0.2s ease, box-shadow 0.2s ease; display: flex; flex-direction: column; text-decoration: none; color: inherit; }}
        .card:hover {{ transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); border-color: #cbd5e1; }}
        
        .card-category {{ font-size: 0.8em; font-weight: 600; color: var(--primary); background: var(--hover); padding: 4px 10px; border-radius: 12px; display: inline-block; align-self: flex-start; margin-bottom: 12px; }}
        .card-title {{ font-size: 1.25em; font-weight: 600; color: var(--primary); margin: 0 0 10px 0; line-height: 1.4; }}
        .card-excerpt {{ font-size: 0.9em; color: var(--text-light); flex-grow: 1; margin-bottom: 15px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
        .card-footer {{ font-size: 0.85em; color: var(--text-light); border-top: 1px solid var(--border); padding-top: 12px; display: flex; justify-content: space-between; }}
        
        /* 无结果提示 */
        #no-results {{ display: none; text-align: center; padding: 40px; color: var(--text-light); font-size: 1.1em; width: 100%; grid-column: 1 / -1; }}
        
        footer {{ margin-top: 50px; text-align: center; color: var(--text-light); font-size: 0.85em; }}
        .hidden {{ display: none !important; }}
    </style>
</head>
<body>
    <header>
        <h1>📚 投研档案库</h1>
        <div class="site-meta">个人投研档案库 · 共 {total_count} 份报告</div>
        
        <div class="search-container">
            <input type="text" id="search-input" class="search-input" placeholder="🔍 搜索报告标题、摘要或关键词...">
        </div>
    </header>

    <div class="filters">
        <button class="filter-btn active" data-filter="all">全部</button>
        {filter_buttons}
    </div>

    <div class="grid" id="card-grid">
        {cards_html}
        <div id="no-results">📭 没有找到匹配的报告，请尝试其他关键词。</div>
    </div>

    <footer>
        最后更新：{update_time} · 由 build_index.py 自动生成
    </footer>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const searchInput = document.getElementById('search-input');
            const filterBtns = document.querySelectorAll('.filter-btn');
            const cards = document.querySelectorAll('.card');
            const noResults = document.getElementById('no-results');
            
            let currentFilter = 'all';
            let searchQuery = '';

            // 核心过滤函数：同时验证“分类”和“搜索词”
            function updateCards() {{
                let visibleCount = 0;
                
                cards.forEach(card => {{
                    const category = card.getAttribute('data-category');
                    const title = card.querySelector('.card-title').textContent.toLowerCase();
                    const excerpt = card.querySelector('.card-excerpt').textContent.toLowerCase();
                    
                    const matchesFilter = (currentFilter === 'all' || category === currentFilter);
                    const matchesSearch = (title.includes(searchQuery) || excerpt.includes(searchQuery));
                    
                    if (matchesFilter && matchesSearch) {{
                        card.classList.remove('hidden');
                        visibleCount++;
                    }} else {{
                        card.classList.add('hidden');
                    }}
                }});
                
                // 控制无结果提示的显示
                if (visibleCount === 0) {{
                    noResults.style.display = 'block';
                }} else {{
                    noResults.style.display = 'none';
                }}
            }}

            // 1. 监听搜索框输入
            searchInput.addEventListener('input', (e) => {{
                searchQuery = e.target.value.toLowerCase();
                updateCards();
            }});

            // 2. 监听分类按钮点击
            filterBtns.forEach(btn => {{
                btn.addEventListener('click', () => {{
                    // 更新按钮高亮状态
                    filterBtns.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    
                    // 更新当前过滤条件并执行过滤
                    currentFilter = btn.getAttribute('data-filter');
                    updateCards();
                }});
            }});
        }});
    </script>
</body>
</html>
"""

# ==========================================
# 2. 解析辅助函数
# ==========================================
def extract_meta_from_html(filepath):
    """尝试从 HTML 文件中提取标题和第一段文本作为摘要"""
    title = os.path.basename(filepath).replace('.html', '')
    excerpt = "点击查看完整数据与分析报告..."
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE) or \
                          re.search(r'<h1.*?>(.*?)</h1>', content, re.IGNORECASE)
            if title_match and title_match.group(1).strip():
                title = title_match.group(1).strip()
            
            p_matches = re.findall(r'<p.*?>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
            for p in p_matches:
                clean_p = re.sub(r'<[^>]+>', '', p).strip()
                if len(clean_p) > 20:
                    excerpt = clean_p[:150] + "..." if len(clean_p) > 150 else clean_p
                    break
    except Exception:
        pass
        
    return title, excerpt

# ==========================================
# 3. 主生成逻辑
# ==========================================
def generate_site():
    cards_html = ""
    categories = set()
    total_count = 0
    
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '.github' in root or root == '.':
            continue
            
        folder_name = os.path.basename(root)
        
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                filepath = os.path.join(root, file)
                url_path = filepath.replace('\\', '/').removeprefix('./')
                safe_url = urllib.parse.quote(url_path)
                
                mtime = os.path.getmtime(filepath)
                date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                
                title, excerpt = extract_meta_from_html(filepath)
                categories.add(folder_name)
                total_count += 1
                
                cards_html += f"""
        <a href="{safe_url}" class="card" data-category="{folder_name}">
            <div class="card-category">{folder_name}</div>
            <h3 class="card-title">{title}</h3>
            <div class="card-excerpt">{excerpt}</div>
            <div class="card-footer">
                <span>📅 {date_str}</span>
            </div>
        </a>"""

    filter_buttons = ""
    for cat in sorted(categories):
        filter_buttons += f'<button class="filter-btn" data-filter="{cat}">{cat}</button>\n        '

    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    final_html = HTML_TEMPLATE.format(
        total_count=total_count,
        filter_buttons=filter_buttons,
        cards_html=cards_html,
        update_time=update_time
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✅ 成功生成带搜索功能的精美主页！共处理 {total_count} 份报告。")

if __name__ == "__main__":
    generate_site()
