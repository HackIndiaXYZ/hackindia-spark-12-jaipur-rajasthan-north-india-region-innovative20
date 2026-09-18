import wikipedia
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json


import re
def web_scraper(url: str) -> str:
    """Scrapes raw text content from a given live website URL."""
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


import sys
import io
import contextlib
import traceback
import subprocess
import tempfile
import os

def execute_python(code: str) -> str:
    """
    Executes Python 3 code in a temporary sandbox and returns the stdout (print statements) or errors.
    Use this to perform calculations, data processing, or run algorithms.
    """
    # Remove markdown backticks if present
    code = code.strip()
    if code.startswith("```python"):
        code = code[9:]
    elif code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    code = code.strip()
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_path = temp_file.name

        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        os.remove(temp_path)
        
        output = result.stdout
        if result.stderr:
            output += "\nErrors:\n" + result.stderr
            
        if not output.strip():
            return "Code executed successfully, but there was no output. Did you forget to print()?"
        return f"Execution Output:\n{output[:4000]}"
    except subprocess.TimeoutExpired:
        if os.path.exists(temp_path): os.remove(temp_path)
        return "Error: Code execution timed out after 10 seconds."
    except Exception as e:
        return f"Error executing code: {str(e)}"

def wiki_search(query: str) -> str:
    """Searches Wikipedia for company information, research, and general knowledge."""
    try:
        results = wikipedia.search(query, results=2)
        if not results:
            return "No Wikipedia articles found."
        
        summary = wikipedia.summary(results[0], sentences=3)
        return f"Title: {results[0]}\nSummary: {summary}"
    except Exception as e:
        return f"Error searching Wikipedia: {e}"

def arxiv_search(query: str) -> str:
    """Searches the ArXiv database for academic research papers."""
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&start=0&max_results=3"
        response = urllib.request.urlopen(url)
        data = response.read()
        root = ET.fromstring(data)
        
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', ns)
        
        if not entries:
            return f"No research papers found on ArXiv for query: '{query}'."
        
        results = []
        for entry in entries:
            title = entry.find('atom:title', ns).text.replace('\n', ' ').strip()
            summary = entry.find('atom:summary', ns).text.replace('\n', ' ').strip()
            results.append(f"Title: {title}\nSummary: {summary[:300]}...")
            
        return "\n\n".join(results)
    except Exception as e:
        return f"Error fetching from ArXiv: {str(e)}"

def github_search(query: str) -> str:
    """Searches GitHub for open source competitor projects and tools."""
    try:
        url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&order=desc"
        req = urllib.request.Request(url, headers={'User-Agent': 'Nexus-AI-Hackathon'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        
        items = data.get('items', [])
        if not items:
            return f"No GitHub repositories found for query: '{query}'."
        
        results = []
        for item in items[:3]:
            name = item.get('full_name')
            desc = item.get('description', 'No description')
            stars = item.get('stargazers_count')
            url = item.get('html_url')
            results.append(f"Repo: {name} ({stars} stars)\nURL: {url}\nDescription: {desc}")
            
        return "\n\n".join(results)
    except Exception as e:
        return f"Error fetching from GitHub: {str(e)}"

# Tool registry
AVAILABLE_TOOLS = {
    "wiki_search": wiki_search,
    "arxiv_search": arxiv_search,
    "github_search": github_search,
    "web_scraper": web_scraper,
    "execute_python": execute_python
}
