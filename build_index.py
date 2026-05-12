import os
import re
import urllib.parse
from datetime import datetime

# ==========================================
# 1. 极简专业风 HTML 模板 (白底/清晰/去干扰)
# ==========================================
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
        
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        
        .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 24px; text-decoration: none; color: inherit; display: flex; flex-direction: column; transition: transform 0.2s, box-shadow 0.2s; }
        .card:hover { transform: translateY(-4px); box-shadow: 0 12px 20px -8px rgba(0,0,0,0.1); border-color: #cbd5e1; }
        
        .card-cat { font-size: 0.8rem; background: #eff6ff; color: var(--primary); padding: 4px 10px; border-radius: 6px; align-self: flex-start; margin-bottom: 12px; font-weight: 500; }
        .card-title { font-size: 1.15rem; font-weight: 600; margin: 0 0 12px 0; color: #0f172a; line-height: 1.4; }
        .card-excerpt { font-size: 0.9rem; color: var(--text-light); flex-grow: 1; margin-bottom: 15px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
        .card-date { font-size: 0.85rem; color: var(--text-light); border-top: 1px solid var(--border); padding-top: 12px; display: flex; align-items: center; gap: 6px; }
        
        .hidden { display: none !important; }
        #no-results { display: none; text-align: center; color: var(--text-light); grid-column: 1 / -1; padding: 60px 20px; border: 1px dashed var(--border); border-radius: 12px; }
        footer { text-align: center; margin-top: 60px; color: var(--text-light); font-size: 0.9rem; }
    </style>
</head>
<body>
    <header>
        <h1>📚 投研档案库</h1>
        <div class="meta">个人知识管理 · 共 __TOTAL__ 份深度报告</div>
        <input type="text" id="search" class="search-box" placeholder="🔍 搜索报告标题、摘要或关键词...">
    </header>

    <div class="filters">
        <button class="filter-btn active" data-filter="all">全部</button>
        __FILTERS__
    </div>

    <div class="grid" id="grid">
        __CARDS__
        <div id="no-results">📭 没有找到匹配的报告，请尝试其他
