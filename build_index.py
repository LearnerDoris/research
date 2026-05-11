import os
import re
import urllib.parse
from datetime import datetime

# ==========================================
# 1. 核心 HTML 模板 (包含现代卡片 CSS 和筛选 JS)
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
        
        /* 头部样式 */
        header {{ border-bottom: 2px solid var(--border); padding-bottom: 20px; margin-bottom: 30px; }}
        h1 {{ color: var(--primary); font-size: 2.2em; margin: 0 0 10px 0; }}
        .site-meta {{ color: var(--text-light); font-size: 0.95em; }}
        
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
        
        footer {{ margin-top: 50px; text-align: center; color: var(--text-light); font-size: 0.85em; }}
        .hidden {{ display: none !important; }}
    </style>
</head>
<body>
    <header>
        <h1>📚 投研档案库</h1>
        <div class="site-meta">个人投研档案库 · 共 {total_count} 份报告</div>
    </header>

    <div class="filters">
        <button class="filter-btn active" data-filter="all">全部</button>
        {filter_buttons}
    </div>

    <div class="grid" id="card-grid">
        {cards_html}
    </div>

    <footer>
        最后更新：{update_time} · 由 build_index.py 自动生成
    </footer>

    <script>
        // 分类筛选逻辑
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                // 更新按钮状态
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // 筛选卡片
                const filter = btn.getAttribute('data-filter');
                document.querySelectorAll('.card').forEach(card => {{
                    if (filter === 'all' || card.getAttribute('data-category') === filter) {{
                        card.classList.remove('hidden');
                    }} else {{
                        card.classList.add('hidden');
                    }}
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
            # 找标题: <title> 或 <h1>
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE) or \
                          re.search(r'<h1.*?>(.*?)</h1>', content, re.IGNORECASE)
            if title_match and title_match.group(1).strip():
                title = title_match.group(1).strip()
            
            # 找摘要: 抓取第一个有实质内容的 <p> 标签
            p_matches = re.findall(r'<p.*?>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
            for p in p_matches:
                clean_p = re.sub(r'<[^>]+>', '', p).strip() # 移除嵌套的html标签
                if len(clean_p) > 20: # 找到第一个超过20个字符的段落
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
    
    # 遍历当前目录
    for root, dirs, files in os.walk('.'):
        if '.git' in root or '.github' in root or root == '.':
            continue
            
        folder_name = os.path.basename(root)
        
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                filepath = os.path.join(root, file)
                url_path = filepath.replace('\\', '/').removeprefix('./')
                safe_url = urllib.parse.quote(url_path)
                
                # 获取文件的最后修改时间
                mtime = os.path.getmtime(filepath)
                date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                
                # 提取内容
                title, excerpt = extract_meta_from_html(filepath)
                categories.add(folder_name)
                total_count += 1
                
                # 生成单张卡片
                cards_html += f"""
        <a href="{safe_url}" class="card" data-category="{folder_name}">
            <div class="card-category">{folder_name}</div>
            <h3 class="card-title">{title}</h3>
            <div class="card-excerpt">{excerpt}</div>
            <div class="card-footer">
                <span>📅 {date_str}</span>
            </div>
        </a>"""

    # 生成分类过滤按钮
    filter_buttons = ""
    for cat in sorted(categories):
        filter_buttons += f'<button class="filter-btn" data-filter="{cat}">{cat}</button>\n        '

    # 渲染最终 HTML
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    final_html = HTML_TEMPLATE.format(
        total_count=total_count,
        filter_buttons=filter_buttons,
        cards_html=cards_html,
        update_time=update_time
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✅ 成功生成精美主页！共处理 {total_count} 份报告。")

if __name__ == "__main__":
    generate_site()
