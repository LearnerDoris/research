# ==========================================
# 1. 核心 HTML 模板 (深色科技风 UI + 搜索)
# ==========================================
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>投研档案库 | Data Terminal</title>
    <style>
        /* 科技感深色主题变量 */
        :root {{ 
            --bg-color: #0d1117; 
            --grid-line: rgba(48, 54, 61, 0.5);
            --card-bg: rgba(22, 27, 34, 0.8);
            --card-border: #30363d;
            --text-main: #c9d1d9;
            --text-muted: #8b949e;
            --accent-glow: #58a6ff;
            --accent-cyan: #39d353;
            --hover-bg: #1f242c;
        }}
        
        body {{ 
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
            background-color: var(--bg-color); 
            /* 科技感网格背景 */
            background-image: linear-gradient(var(--grid-line) 1px, transparent 1px), 
                              linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
            background-size: 40px 40px;
            color: var(--text-main); 
            max-width: 1100px; 
            margin: 0 auto; 
            padding: 50px 20px; 
            line-height: 1.6; 
        }}
        
        /* 头部样式：终端风格 */
        header {{ 
            border-bottom: 1px solid var(--card-border); 
            padding-bottom: 25px; 
            margin-bottom: 30px; 
            position: relative;
        }}
        
        h1 {{ 
            color: #ffffff; 
            font-size: 2.5em; 
            margin: 0 0 10px 0; 
            font-weight: 700;
            letter-spacing: 1px;
            text-shadow: 0 0 20px rgba(88, 166, 255, 0.4);
