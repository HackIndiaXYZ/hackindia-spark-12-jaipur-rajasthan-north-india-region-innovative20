import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add UPLOAD_CACHE to the top
if "UPLOAD_CACHE =" not in content:
    content = content.replace("app = FastAPI()", "app = FastAPI()\nUPLOAD_CACHE = {'latest': ''}")

# 2. Add /upload endpoint
upload_endpoint = """
@app.post("/upload")
async def upload_file(request: Request):
    body = await request.body()
    UPLOAD_CACHE['latest'] = body.decode('utf-8', errors='ignore')
    return {"status": "ok"}
"""
if "@app.post(\"/upload\")" not in content:
    content = content.replace("@app.get(\"/stream\")", upload_endpoint + "\n@app.get(\"/stream\")")

# 3. Read UPLOAD_CACHE in /stream and clear it
stream_patch_old = """    chaos = chaos_mode == 'true'
    
    async def event_generator():"""

stream_patch_new = """    chaos = chaos_mode == 'true'
    doc_context = UPLOAD_CACHE.get('latest', '')
    UPLOAD_CACHE['latest'] = ''  # Clear after reading
    if doc_context:
        task = f"ATTACHED DOCUMENT CONTENT:\\n{doc_context}\\n\\nUSER QUERY: {task}"
        
    async def event_generator():"""

if "UPLOAD_CACHE.get('latest'" not in content:
    content = content.replace(stream_patch_old, stream_patch_new)

# 4. Inject frontend CSS for chaos mode and dropzone
css_injection = """
        /* Chaos Mode */
        body.chaos-active {
            --accent-primary: #ff003c !important;
            --bg-base: #1a0000 !important;
            --bg-panel: #3a0005 !important;
            animation: redAlert 1.5s infinite alternate;
        }
        body.chaos-active * {
            border-color: #ff003c !important;
        }
        @keyframes redAlert {
            0% { box-shadow: inset 0 0 0px rgba(255,0,60,0.5); }
            100% { box-shadow: inset 0 0 100px rgba(255,0,60,0.8); }
        }
        
        /* Dropzone overlay */
        #drop-overlay {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 255, 0, 0.2); border: 5px dashed var(--accent-primary);
            z-index: 9999; justify-content: center; align-items: center; pointer-events: none;
            color: var(--accent-primary); font-size: 30px; font-family: var(--font-mono); font-weight: bold;
        }
"""
if "body.chaos-active" not in content:
    content = content.replace("</style>", css_injection + "\n    </style>")

# 5. Inject Dropzone HTML
drop_html = '<div id="drop-overlay">DROP FILE TO INGEST</div>'
if "id=\"drop-overlay\"" not in content:
    content = content.replace("<body>", "<body>\n    " + drop_html)

# 6. Inject Frontend JS for Chaos toggle and Drag/Drop
js_injection = r"""
        // Chaos Mode Toggle
        const chaosToggle = document.querySelector('input[type="checkbox"]'); // The first toggle is Chaos Mode in UI
        if(chaosToggle) {
            chaosToggle.addEventListener('change', function() {
                if(this.checked) document.body.classList.add('chaos-active');
                else document.body.classList.remove('chaos-active');
            });
        }

        // File Drag & Drop RAG
        const dropOverlay = document.getElementById('drop-overlay');
        document.body.addEventListener('dragover', (e) => { e.preventDefault(); dropOverlay.style.display = 'flex'; });
        document.body.addEventListener('dragleave', (e) => { if(e.target === document.body) dropOverlay.style.display = 'none'; });
        document.body.addEventListener('drop', (e) => {
            e.preventDefault();
            dropOverlay.style.display = 'none';
            const file = e.dataTransfer.files[0];
            if(file) {
                const reader = new FileReader();
                reader.onload = async function(evt) {
                    await fetch('/upload', { method: 'POST', body: evt.target.result });
                    const p = document.getElementById('prompt');
                    p.value = "[FILE INGESTED: " + file.name + "] " + p.value;
                    playSound('receive');
                };
                reader.readAsText(file);
            }
        });
"""
if "File Drag & Drop RAG" not in content:
    content = content.replace("function sendMessage() {", js_injection + "\n        function sendMessage() {")

# 7. Update the chaos mode URL parameter in sendMessage
if "chaos_mode=${chaosToggle ? chaosToggle.checked : false}" not in content:
    content = content.replace("chaos_mode=${false}", "chaos_mode=${document.querySelector('input[type=\"checkbox\"]').checked}")


with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("main.py patched with Chaos Mode, Drag-and-Drop RAG, and UI updates!")
