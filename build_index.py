import os
import re
import urllib.parse
from datetime import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>投研档案库 | Data Terminal</title>
    <style>
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
            background-image: linear-gradient(var(--grid-line) 1px, transparent 1px), 
                              linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
            background-size: 40px 40px;
            color: var(--text-main); 
            max-width: 1100px; 
            margin: 0 auto; 
            padding: 50px 20px; 
            line-height: 1.6; 
        }}
        
        header {{ border-bottom: 1px solid var(--card-border); padding-bottom: 25px; margin-bottom: 30px; position: relative; }}
        h1 {{ color: #ffffff; font-size: 2.5em; margin: 0 0 10px 0; font-weight: 700; letter-spacing: 1px; text-shadow: 0 0 20px rgba(88, 166, 255, 0.4); }}
        .site-meta {{ color: var(--accent-cyan); font-family: 'Courier New', Courier, monospace; font-size: 0.9em; margin-bottom: 20px; }}
        
        .search-container {{ margin-bottom: 25px; position: relative; }}
        .search-input {{ width: 100%; box-sizing: border-box; padding: 14px 20px 14px 45px; border: 1px solid var(--card-border); border-radius: 6px; font-size: 1rem; color: #fff; background-color: var(--card-bg); backdrop-filter: blur(10px); transition: all 0.3s ease; }}
        .search-input:focus {{ outline: none; border-color: var(--accent-glow); box-shadow: 0 0 15px rgba(88, 166, 255, 0.2), inset 0 0 5px rgba(88, 166, 255, 0.1); }}
        .search-container::before {{ content: "⌕"; position: absolute; left: 15px; top: 50%; transform: translateY(-50%); font-size: 1.5em; color: var(--text-muted); pointer-events: none; }}
        
        .filters {{ display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 40px; }}
        .filter-btn {{ padding: 6px 18px; border: 1px solid var(--card-border); background: transparent; border-radius: 4px; cursor: pointer; font-size: 0.85em; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; transition: all 0.2s ease; }}
        .filter-btn:hover {{ border-color: var(--text-muted); color: var(--text-main); }}
        .filter-btn.active {{ background: rgba(88, 166, 255, 0.1); color: var(--accent-glow); border-color: var(--accent-glow); box-shadow: 0 0 10px rgba(88, 166, 255, 0.2); }}
        
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 24px; }}
        
        .card {{ background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 8px; padding: 24px; transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); display: flex; flex-direction: column; text-decoration: none; color: inherit; position: relative; overflow: hidden; backdrop-filter: blur(5px); }}
        .card::before {{ content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, var(--accent-glow), transparent); opacity: 0; transition: opacity 0.3s ease; }}
        .card:hover {{ transform: translateY(-5px); border-color: #4b5563; box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5); background: var(--hover-bg); }}
        .card:hover::before {{ opacity: 1; }}
        
        .card-category {{ font-family: 'Courier New', Courier, monospace; font-size: 0.75em; color: var(--accent-glow); border: 1px solid rgba(88, 166, 255, 0.3); background: rgba(88, 166, 255, 0.05); padding: 4px 8px; border-radius: 4px; display: inline-block; align-self: flex-start; margin-bottom: 16px; }}
        .card-title {{ font-size: 1.2em; font-weight: 600; color: #ffffff; margin: 0 0 12px 0; line-height: 1.4; }}
        .card-excerpt {{ font-size: 0.9em; color: var(--text-muted); flex-grow: 1; margin-bottom: 20px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
        .card-footer {{ font-family: 'Courier New', Courier, monospace; font-size: 0.8em; color: var(--text-muted); border-top: 1px solid var(--card-border); padding-top: 15px; display: flex; justify-content: space-between; align-items: center; }}
        .card-footer::after {{ content: ""; display: block; width: 8px; height: 8px; background-color: var(--accent-cyan); border-radius: 50%; box-shadow: 0 0 8px var(--accent-cyan); }}
        
        #no-results {{ display: none; text-align: center; padding: 50px; color: var(--text-muted); font-size: 1.1em; width: 100%; grid-column: 1 / -1; border: 1px dashed var(--card-border); border-radius: 8px; }}
        footer {{ margin-top: 60px; text-align: center; color: var(--text-muted); font-size: 0.85em; font-family: 'Courier New', Courier, monospace; }}
        .hidden {{ display: none !important; }}
    </style>
</head>
<body>
    <header>
        <h1>SYS.DATA_TERMINAL</h1>
        <div class="site-meta">> INITIALIZING... STATUS: ONLINE | RECORDS: {total_count}</div>
        <div class="search-container"><input type="text" id="search-input" class="search-input" placeholder="Query data core (Title / Abstract / Keywords)..."></div>
    </header>

    <div class="filters">
        <button class="filter-btn active" data-filter="all">ALL_DATA</button>
        {filter_buttons}
    </div>

    <div class="grid" id="card-grid">
        {cards_html}
        <div id="no-results">> ERROR_404: No matching records found in data core.</div>
    </div>

    <footer>
        > LAST_SYNC: {update_time} | GENERATED_BY: build_index.py v2.0
    </footer>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const searchInput = document.getElementById('search-input');
            const filterBtns = document.querySelectorAll('.filter-btn');
            const cards = document.querySelectorAll('.card');
            const noResults = document.getElementById('no-results');
            
            let currentFilter = 'all';
            let searchQuery = '';

            function updateCards() {{
                let visibleCount = 0;
                cards.forEach(card
