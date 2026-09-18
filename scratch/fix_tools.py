import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/tools.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('\\"\\"\\"', '"""')

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/tools.py', 'w', encoding='utf-8') as f:
    f.write(content)
