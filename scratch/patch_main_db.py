import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
if "from database import SessionLocal, ChatMessage, VectorChunk" not in content:
    content = content.replace("from agent import MultiAgentTeam", "from agent import MultiAgentTeam, get_gemini_embedding, search_vector_db\nfrom database import SessionLocal, ChatMessage, VectorChunk")

old_upload = """@app.post("/upload")
async def upload_file(request: Request):
    body = await request.body()
    UPLOAD_CACHE['latest'] = body.decode('utf-8', errors='ignore')
    return {"status": "ok"}"""

new_upload = """@app.post("/upload")
async def upload_file(request: Request):
    import json
    body = await request.body()
    text = body.decode('utf-8', errors='ignore')
    
    # Text chunking
    chunk_size = 1000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    db = SessionLocal()
    # Clear previous latest
    db.query(VectorChunk).filter(VectorChunk.document_name == 'latest_upload').delete()
    
    for c in chunks:
        emb = get_gemini_embedding(c)
        if emb:
            chunk_db = VectorChunk(document_name='latest_upload', chunk_text=c, embedding_json=json.dumps(emb))
            db.add(chunk_db)
            
    db.commit()
    db.close()
    return {"status": "ok", "chunks_processed": len(chunks)}"""

if "chunk_size = 1000" not in content:
    content = content.replace(old_upload, new_upload)

old_stream_start = """    chaos = chaos_mode == 'true'
    doc_context = UPLOAD_CACHE.get('latest', '')
    UPLOAD_CACHE['latest'] = ''  # Clear after reading
    if doc_context:
        task = f"ATTACHED DOCUMENT CONTENT:\\n{doc_context}\\n\\nUSER QUERY: {task}"
        
    async def event_generator():"""

new_stream_start = """    chaos = chaos_mode == 'true'
    
    # Check if a file was ingested in the prompt and run Vector Search
    if "[FILE INGESTED:" in task:
        # Extract the user's actual question
        clean_query = task.split("]")[-1].strip()
        relevant_context = search_vector_db(clean_query, "latest_upload", top_k=3)
        if relevant_context:
            task = f"RETRIEVED DOCUMENT CONTEXT:\\n{relevant_context}\\n\\nUSER QUERY: {clean_query}"
        
    async def event_generator():"""

if "search_vector_db" not in content:
    content = content.replace(old_stream_start, new_stream_start)

# Update sessions endpoints to use DB
old_sessions = """@app.get("/sessions")
async def get_sessions():
    \"\"\"Retrieves all active session IDs and their parsed titles for the sidebar list\"\"\"
    filepath = "agent_memory.json"
    import os
    if not os.path.exists(filepath):
        return {"sessions": []}
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            sessions = []
            for sid, sdata in data.items():
                title = "New Chat"
                if sdata.get("history"):
                    title = sdata["history"][0]["task"][:30] + "..."
                sessions.append({"id": sid, "title": title})
            return {"sessions": list(reversed(sessions))}
    except:
        return {"sessions": []}

@app.post("/sessions")
async def create_session():
    \"\"\"Creates a new unique session and returns the ID\"\"\"
    session_id = f"sess_{uuid.uuid4().hex[:8]}"
    return {"session_id": session_id}

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str = Path(..., description="The session ID to delete")):
    \"\"\"Deletes a specific session from memory database\"\"\"
    filepath = "agent_memory.json"
    import os
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if session_id in data:
                del data[session_id]
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
                return {"status": "deleted"}
        except:
            pass
    return {"status": "error"}

@app.get("/sessions/{session_id}")
async def get_session_history(session_id: str = Path(..., description="The session ID to fetch")):
    \"\"\"Retrieves the complete history of a specific session\"\"\"
    filepath = "agent_memory.json"
    import os
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if session_id in data:
                return {"history": data[session_id].get("history", [])}
        except:
            pass
    return {"history": []}"""

new_sessions = """@app.get("/sessions")
async def get_sessions():
    db = SessionLocal()
    messages = db.query(ChatMessage).all()
    
    sessions = {}
    for m in messages:
        if m.session_id not in sessions and m.role == 'user':
            sessions[m.session_id] = m.content[:30] + "..."
            
    db.close()
    return {"sessions": [{"id": k, "title": v} for k, v in reversed(list(sessions.items()))]}

@app.post("/sessions")
async def create_session():
    session_id = f"sess_{uuid.uuid4().hex[:8]}"
    return {"session_id": session_id}

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str = Path(...)):
    db = SessionLocal()
    db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
    db.commit()
    db.close()
    return {"status": "deleted"}

@app.get("/sessions/{session_id}")
async def get_session_history(session_id: str = Path(...)):
    db = SessionLocal()
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.id).all()
    db.close()
    
    history = []
    current_pair = {}
    for m in messages:
        if m.role == 'user':
            current_pair['task'] = m.content
        elif m.role == 'agent':
            current_pair['answer'] = m.content
            history.append(current_pair)
            current_pair = {}
            
    return {"history": history}"""

if "messages = db.query(ChatMessage).all()" not in content:
    content = content.replace(old_sessions, new_sessions)

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("main.py updated for DB!")
