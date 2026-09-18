import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_async = """                reader.onload = async function(evt) {
                    await fetch('/upload', { method: 'POST', body: evt.target.result });
                    const p = document.getElementById('prompt');
                    p.value = "[FILE INGESTED: " + file.name + "] " + p.value;
                    playSound('receive');
                };"""
                
new_async = """                reader.onload = function(evt) {
                    fetch('/upload', { method: 'POST', body: evt.target.result }).then(() => {
                        const p = document.getElementById('prompt');
                        p.value = "[FILE INGESTED: " + file.name + "] " + p.value;
                        playSound('receive');
                    });
                };"""

if old_async in content:
    content = content.replace(old_async, new_async)

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed async to be browser-safe!")
