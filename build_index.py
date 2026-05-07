import os
import urllib.parse

# 1. 定义首页的 HTML 模板 (可以自己加 CSS 美化)
html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>投研报告 HTML 归档</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.6; color: #333; }}
        h1 {{ border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 12px 0; padding: 10px; background: #f9f9f9; border-radius: 6px; }}
        a {{ text-decoration: none; color: #0366d6; font-weight: 500; display: block; }}
        a:hover {{ color: #0056b3; text-decoration: underline; }}
        .folder-name {{ font-size: 0.85em; color: #666; margin-bottom: 4px; }}
    </style>
</head>
<body>
    <h1>📊 投研报告 HTML 归档</h1>
    <p>自动生成的静态报告目录。</p>
    <ul>
        {links}
    </ul>
</body>
</html>
"""

def generate_index():
    links_html = ""
    
    # 2. 遍历当前目录及子目录寻找 HTML 文件
    for root, dirs, files in os.walk('.'):
        # 排除隐藏文件夹 (如 .git)
        if '.git' in root or '.github' in root:
            continue
            
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                # 获取相对路径
                filepath = os.path.join(root, file)
                # 将 Windows 的反斜杠替换为 URL 的正斜杠
                url_path = filepath.replace('\\', '/').removeprefix('./')
                # 处理 URL 中的中文和空格
                safe_url = urllib.parse.quote(url_path)
                
                # 获取文件夹名，用于分类展示
                folder_name = os.path.dirname(url_path)
                if not folder_name:
                    folder_name = "根目录"
                
                # 去掉 .html 后缀作为显示标题
                display_name = file.replace('.html', '')
                
                # 拼接单个列表项的 HTML
                links_html += f"""
                <li>
                    <div class="folder-name">📂 {folder_name}</div>
                    <a href="{safe_url}" target="_blank">{display_name}</a>
                </li>\n"""

    # 3. 将生成的链接填入模板并写入 index.html
    final_html = html_template.format(links=links_html)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print("✅ index.html 生成成功！共收录报告。")

if __name__ == "__main__":
    generate_index()