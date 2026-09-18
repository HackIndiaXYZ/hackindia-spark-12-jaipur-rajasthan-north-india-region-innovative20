import re
import urllib.request

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/tools.py', 'r', encoding='utf-8') as f:
    content = f.read()

scraper_code = r"""
import re
def web_scraper(url: str) -> str:
    \"\"\"Scrapes raw text content from a given live website URL.\"\"\"
    if not url.startswith('http'):
        url = 'https://' + url
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=5)
        html = response.read().decode('utf-8', errors='ignore')
        
        text = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL|re.IGNORECASE)
        text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL|re.IGNORECASE)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return f"Content from {url}:\n{text[:4000]}..." 
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"
"""

if "def web_scraper" not in content:
    content = content.replace("def wiki_search", scraper_code + "\ndef wiki_search")
    content = content.replace('"github_search": github_search', '"github_search": github_search,\n    "web_scraper": web_scraper')
    with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/tools.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Tools patched.")
