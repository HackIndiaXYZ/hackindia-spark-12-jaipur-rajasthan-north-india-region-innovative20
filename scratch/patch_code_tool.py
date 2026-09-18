import re
import sys
import io
import contextlib
import traceback

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/tools.py', 'r', encoding='utf-8') as f:
    content = f.read()

python_tool_code = r"""
import sys
import io
import contextlib
import traceback
import subprocess
import tempfile
import os

def execute_python(code: str) -> str:
    \"\"\"
    Executes Python 3 code in a temporary sandbox and returns the stdout (print statements) or errors.
    Use this to perform calculations, data processing, or run algorithms.
    \"\"\"
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
"""

if "def execute_python" not in content:
    content = content.replace("def wiki_search", python_tool_code + "\ndef wiki_search")
    content = content.replace('"web_scraper": web_scraper', '"web_scraper": web_scraper,\n    "execute_python": execute_python')
    with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/tools.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Code Execution Tool Patched!")
else:
    print("Already exists.")
