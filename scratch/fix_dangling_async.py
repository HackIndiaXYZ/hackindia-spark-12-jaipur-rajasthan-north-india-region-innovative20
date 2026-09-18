import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the dangling async
content = content.replace("        async \n        // Chaos Mode Toggle", "        // Chaos Mode Toggle")
content = content.replace("        async \n\n        // Chaos Mode Toggle", "        // Chaos Mode Toggle")

# Just in case it's formatted differently, use regex
content = re.sub(r'async\s*// Chaos Mode Toggle', '// Chaos Mode Toggle', content)

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed dangling async!")
