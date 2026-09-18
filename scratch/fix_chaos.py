import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add ID to Chaos Mode checkbox
old_chaos_html = """            <div class="settings-row">
                <span>Chaos Mode</span>
                <label class="toggle-switch">
                    <input type="checkbox">
                    <span class="toggle-slider"></span>
                </label>
            </div>"""

new_chaos_html = """            <div class="settings-row">
                <span>Chaos Mode</span>
                <label class="toggle-switch">
                    <input type="checkbox" id="chaos-toggle">
                    <span class="toggle-slider"></span>
                </label>
            </div>"""

if "id=\"chaos-toggle\"" not in content:
    content = content.replace(old_chaos_html, new_chaos_html)

# 2. Fix the JS event listener
old_js = "const chaosToggle = document.querySelector('input[type=\"checkbox\"]');"
new_js = "const chaosToggle = document.getElementById('chaos-toggle');"

if new_js not in content:
    content = content.replace(old_js, new_js)

# 3. Ensure sendMessage gets the right chaos value
old_send = "chaos_mode=${document.querySelector('input[type=\"checkbox\"]').checked}"
new_send = "chaos_mode=${document.getElementById('chaos-toggle').checked}"

if new_send not in content:
    content = content.replace(old_send, new_send)

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed Chaos toggle!")
