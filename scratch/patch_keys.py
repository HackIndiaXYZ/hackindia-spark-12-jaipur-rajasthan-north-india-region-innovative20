with open("C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py", "r", encoding="utf-8") as f:
    content = f.read()

bad_groq_logic = """            if self.model_name.startswith("groq/"):
                api_key = os.environ.get("GROQ_API_KEY", "")
                if not api_key:
                    raise ValueError("GROQ_API_KEY is missing from environment. Add it to Render environment variables.")
                url = "https://api.groq.com/openai/v1/chat/completions"
                model_id = self.model_name.split("groq/")[1]"""

good_groq_logic = """            if self.model_name.startswith("groq/"):
                if self.groq_keys:
                    api_key = self.groq_keys[self.current_groq_idx]
                else:
                    api_key = os.environ.get("GROQ_API_KEY", "")
                if not api_key:
                    raise ValueError("GROQ_API_KEY is missing from environment. Add it to Render environment variables.")
                url = "https://api.groq.com/openai/v1/chat/completions"
                model_id = self.model_name.split("groq/")[1]"""

if bad_groq_logic in content:
    content = content.replace(bad_groq_logic, good_groq_logic)
    with open("C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed!")
else:
    print("Not found.")
