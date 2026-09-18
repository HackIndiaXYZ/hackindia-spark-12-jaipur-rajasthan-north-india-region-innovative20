import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Chart.js script tag
if "chart.js" not in content:
    content = content.replace(
        '<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>',
        '<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>\n    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
    )

# 2. Add Code Executor to dropdown
if "execute_python" not in content:
    content = content.replace(
        '<option value="web_scraper">Web Scraper (Live)</option>',
        '<option value="web_scraper">Web Scraper (Live)</option>\n                    <option value="execute_python">Code Executor (Agent-Coder)</option>'
    )

# 3. Add Chart.js regex replacement in marked parsing
old_marked_regex = r"htmlContent = htmlContent.replace(/<pre><code class=\"language-mermaid\">([\s\S]*?)<\/code><\/pre>/g, '<div class=\"mermaid\">$1<\/div>');"

new_marked_regex = r"""htmlContent = htmlContent.replace(/<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/g, '<div class="mermaid">$1</div>');
                    htmlContent = htmlContent.replace(/<pre><code class="language-json_chart">([\s\S]*?)<\/code><\/pre>/g, '<div class="chart-container" style="position: relative; height:400px; width:100%; margin:20px 0; background:rgba(0,0,0,0.5); padding:10px; border-radius:8px;"><canvas class="dynamic-chart"></canvas><script type="application/json" class="chart-data">$1<\\/script></div>');"""

if "language-json_chart" not in content:
    content = content.replace(old_marked_regex, new_marked_regex)

# 4. Add Chart instantiation in setTimeout
old_timeout = r"try { mermaid.run({ querySelector: '.mermaid' }); } catch(e) { console.error(e); }"
new_timeout = r"""try { mermaid.run({ querySelector: '.mermaid' }); } catch(e) { console.error(e); }
                        document.querySelectorAll('.chart-container').forEach(container => {
                            try {
                                const canvas = container.querySelector('.dynamic-chart');
                                const dataStr = container.querySelector('.chart-data').textContent;
                                new Chart(canvas, JSON.parse(dataStr));
                            } catch(e) { console.error("Chart rendering error:", e); }
                        });"""
                        
if "new Chart(canvas" not in content:
    content = content.replace(old_timeout, new_timeout)

# 5. Tell the Oracle Agent it can output charts!
# Wait, the prompt is in agent.py. Let's patch agent.py next.

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("main.py patched successfully!")
