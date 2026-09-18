import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
if "from database import SessionLocal, ChatMessage, VectorChunk" not in content:
    content = content.replace("import json", "import json\nimport numpy as np\nfrom database import SessionLocal, ChatMessage, VectorChunk")

old_memory_manager = """class MemoryManager:
    \"\"\"Handles short-term and long-term memory persistence with Rolling Summary Compression and Session IDs.\"\"\"
    def __init__(self, team, model_name="gemini-3.6-flash", filepath="agent_memory.json"):
        self.team = team
        self.model_name = model_name
        self.filepath = filepath
        self.db = self._load() # Format: {"session_id": {"history": [], "summary": ""}}

    @property
    def client(self):
        if hasattr(self.team, "client"):
            return self.team.client
        return self.team

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
            except Exception:
                pass
        return {}

    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.db, f, indent=4)

    def get_context_string(self, session_id: str) -> tuple:
        \"\"\"Returns (context_string, history_count, has_summary)\"\"\"
        session = self.db.get(session_id, {"history": [], "summary": ""})
        if not session["history"] and not session["summary"]:
            return "No previous conversation history.", 0, False
        
        context = "--- PREVIOUS CONVERSATION CONTEXT ---\\n"
        if session["summary"]:
            context += f"COMPRESSED LONG-TERM MEMORY:\\n{session['summary']}\\n\\n"
        
        for i, entry in enumerate(session["history"]):
            context += f"Recent Query {i+1}: {entry['task']}\\n"
            ans = entry['answer']
            if len(ans) > 400: ans = ans[:400] + "...\\n(truncated)"
            context += f"Recent Answer {i+1}: {ans}\\n\\n"
        context += "--------------------------------------\\n"
        return context, len(session["history"]), bool(session["summary"])

    def add_entry(self, session_id: str, task: str, answer: str):
        if session_id not in self.db:
            self.db[session_id] = {"history": [], "summary": ""}
        
        self.db[session_id]["history"].append({"task": task, "answer": answer})
        
        # ROLLING COMPRESSION: If history > 2 items, compress the oldest into the summary
        if len(self.db[session_id]["history"]) > 2:
            oldest = self.db[session_id]["history"].pop(0)
            self._compress_memory(session_id, oldest)
            
        self._save()

    def _compress_memory(self, session_id: str, old_entry: dict):
        current_summary = self.db[session_id]["summary"]
        prompt = f"Update this memory summary: '{current_summary}'. Integrate this new past interaction -> User asked: '{old_entry['task']}'. AI replied: '{old_entry['answer'][:300]}'. Keep the final summary extremely dense and concise."
        messages = [{"role": "user", "parts": [{"text": prompt}]}]
        try:
            if hasattr(self.team, "generate_content"):
                res_text = self.team.generate_content(messages)
            else:
                res = self.team.models.generate_content(model=self.model_name, contents=messages)
                res_text = res.text
            if res_text:
                self.db[session_id]["summary"] = res_text
        except Exception as e:
            print(f"Compression error: {e}")"""

new_memory_manager = """class MemoryManager:
    \"\"\"Handles short-term memory persistence using SQLAlchemy SQLite DB.\"\"\"
    def __init__(self, team, model_name="gemini-3.6-flash"):
        self.team = team
        self.model_name = model_name

    def get_context_string(self, session_id: str) -> tuple:
        \"\"\"Returns (context_string, history_count, has_summary)\"\"\"
        db = SessionLocal()
        messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.id).all()
        db.close()
        
        if not messages:
            return "No previous conversation history.", 0, False
            
        context = "--- PREVIOUS CONVERSATION CONTEXT ---\\n"
        history_pairs = []
        current_pair = {}
        for m in messages:
            if m.role == "user":
                current_pair["task"] = m.content
            elif m.role == "agent":
                current_pair["answer"] = m.content
                history_pairs.append(current_pair)
                current_pair = {}
                
        # Only take last 3 pairs for context
        history_pairs = history_pairs[-3:]
        for i, entry in enumerate(history_pairs):
            context += f"Recent Query {i+1}: {entry.get('task', '')}\\n"
            ans = entry.get('answer', '')
            if len(ans) > 400: ans = ans[:400] + "...\\n(truncated)"
            context += f"Recent Answer {i+1}: {ans}\\n\\n"
        context += "--------------------------------------\\n"
        return context, len(history_pairs), False

    def add_entry(self, session_id: str, task: str, answer: str):
        db = SessionLocal()
        # Ensure we don't save the document attachments to the chat history explicitly
        clean_task = task.split("USER QUERY: ")[-1] if "USER QUERY: " in task else task
        user_msg = ChatMessage(session_id=session_id, role="user", content=clean_task)
        agent_msg = ChatMessage(session_id=session_id, role="agent", content=answer)
        db.add(user_msg)
        db.add(agent_msg)
        db.commit()
        db.close()

def get_gemini_embedding(text: str) -> list:
    \"\"\"Gets vector embedding using Gemini API.\"\"\"
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return []
    import requests
    url = f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key={api_key}"
    data = {"model": "models/text-embedding-004", "content": {"parts": [{"text": text[:5000]}]}}
    try:
        res = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
        if res.status_code == 200:
            return res.json().get("embedding", {}).get("values", [])
    except Exception as e:
        print("Embedding error:", e)
    return []

def search_vector_db(query: str, document_name: str, top_k: int = 3) -> str:
    \"\"\"Searches the SQLite VectorChunk table using cosine similarity.\"\"\"
    db = SessionLocal()
    chunks = db.query(VectorChunk).filter(VectorChunk.document_name == document_name).all()
    db.close()
    
    if not chunks:
        return ""
        
    query_emb = np.array(get_gemini_embedding(query))
    if query_emb.size == 0:
        return ""
        
    results = []
    for c in chunks:
        c_emb = np.array(json.loads(c.embedding_json))
        if c_emb.size == 0: continue
        # Cosine similarity
        sim = np.dot(query_emb, c_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(c_emb))
        results.append((sim, c.chunk_text))
        
    results.sort(key=lambda x: x[0], reverse=True)
    best_chunks = [r[1] for r in results[:top_k]]
    return "\\n\\n".join(best_chunks)
"""

if "class MemoryManager" in content and "SQLAlchemy SQLite DB" not in content:
    content = content.replace(old_memory_manager, new_memory_manager)

# Fix MemoryManager initialization
content = content.replace("self.memory_manager = MemoryManager(self, self.model_name, filepath=\"agent_memory.json\")", "self.memory_manager = MemoryManager(self, self.model_name)")
content = content.replace("self.memory_manager = MemoryManager(self, self.model_name)", "self.memory_manager = MemoryManager(self, self.model_name)")

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("agent.py updated for DB!")
