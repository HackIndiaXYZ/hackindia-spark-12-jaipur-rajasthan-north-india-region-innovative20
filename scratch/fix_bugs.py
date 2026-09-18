import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix Python Request import
if "from fastapi import FastAPI, Request" not in content:
    content = content.replace("from fastapi import FastAPI", "from fastapi import FastAPI, Request")

# 2. Fix the Javascript HTML ending bug (replace script with div)
old_json_chart = r"""htmlContent = htmlContent.replace(/<pre><code class="language-json_chart">([\\s\\S]*?)<\/code><\/pre>/g, '<div class="chart-container" style="position: relative; height:400px; width:100%; margin:20px 0; background:rgba(0,0,0,0.5); padding:10px; border-radius:8px;"><canvas class="dynamic-chart"></canvas><script type="application/json" class="chart-data">$1<\/script></div>');"""

new_json_chart = r"""htmlContent = htmlContent.replace(/<pre><code class="language-json_chart">([\\s\\S]*?)<\/code><\/pre>/g, '<div class="chart-container" style="position: relative; height:400px; width:100%; margin:20px 0; background:rgba(0,0,0,0.5); padding:10px; border-radius:8px;"><canvas class="dynamic-chart"></canvas><div class="chart-data" style="display:none">$1</div></div>');"""

if '<div class="chart-data" style="display:none">' not in content:
    content = content.replace(old_json_chart, new_json_chart)

# 3. Wait, is there any other `<script>` tag I injected? No.

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed backend Request import and frontend script tag bug!")
