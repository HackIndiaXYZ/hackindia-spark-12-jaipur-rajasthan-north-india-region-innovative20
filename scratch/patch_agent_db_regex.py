import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

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
    import json
    import numpy as np
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

if "SQLAlchemy SQLite DB" not in content:
    content = re.sub(r'class MemoryManager:.*?(?=class ResearcherAgent:)', new_memory_manager + '\n', content, flags=re.DOTALL)
    with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("agent.py updated via regex!")
else:
    print("Already updated.")
