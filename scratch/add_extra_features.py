import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CSS
css_add = r'''
        /* Mission Feed */
        .mission-feed {
            position: fixed; bottom: 0; left: 0; width: 100%;
            background: #000; border-top: 1px solid var(--accent-primary);
            color: var(--accent-primary); font-family: var(--font-mono); font-size: 10px;
            padding: 4px 0; overflow: hidden; z-index: 100;
        }
        .feed-content {
            white-space: nowrap; animation: scrollFeed 30s linear infinite;
        }
        @keyframes scrollFeed { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

        /* Hacker Terminal */
        #hacker-terminal {
            position: fixed; right: 340px; bottom: 40px;
            width: 350px; height: 250px;
            background: rgba(0, 20, 0, 0.9);
            border: 1px solid #0f0; border-radius: 4px;
            flex-direction: column; z-index: 90;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
            backdrop-filter: blur(5px);
        }
        .term-header {
            background: #0f0; color: #000;
            font-family: var(--font-mono); font-size: 10px; font-weight: bold;
            padding: 4px 8px; text-transform: uppercase;
        }
        .term-body {
            flex: 1; overflow-y: auto;
            color: #0f0; font-family: var(--font-mono); font-size: 10px;
            padding: 8px; white-space: pre-wrap; word-wrap: break-word;
        }
'''
if "/* Mission Feed */" not in content:
    content = content.replace("</style>", css_add + "\n    </style>")

# 2. HTML elements (Feed & Terminal)
html_add = r'''
    <!-- HACKER TERMINAL -->
    <div id="hacker-terminal" style="display: none;">
        <div class="term-header">RAW PAYLOAD STREAM</div>
        <div class="term-body" id="term-body">Awaiting connection...</div>
    </div>

    <!-- MISSION FEED TICKER -->
    <div class="mission-feed">
        <div class="feed-content" id="feed-content">
            [LIVE] Agent Oracle compiling generative dataset in Tokyo... &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; 
            [LIVE] Scout navigating ArXiv repositories... &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; 
            [ALERT] Security Sentinel blocked unauthorized payload... &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
            [LIVE] Forge synthesizing React components... &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
            [LIVE] Global Network Status: OPTIMAL
        </div>
    </div>
'''
if "<!-- HACKER TERMINAL -->" not in content:
    content = content.replace("<!-- 3D Mascot Widget -->", html_add + "\n    <!-- 3D Mascot Widget -->")

# 3. Settings Toggle
term_toggle_html = r'''
            <div class="settings-row">
                <span>Hacker Terminal</span>
                <label class="toggle-switch">
                    <input type="checkbox" id="term-toggle">
                    <span class="toggle-slider"></span>
                </label>
            </div>'''
if "id=\"term-toggle\"" not in content:
    content = content.replace('<div class="settings-row">\n                <span>Show Mascot</span>', term_toggle_html + '\n            <div class="settings-row">\n                <span>Show Mascot</span>')

# 4. Web Scraper tool dropdown
scraper_opt = '<option value="web_scraper">Web Scraper (Live)</option>'
if scraper_opt not in content:
    content = content.replace('<option value="github_search">GitHub</option>', '<option value="github_search">GitHub</option>\n                    ' + scraper_opt)

# 5. JS Audio & Term Logic
js_add = r'''
        document.getElementById('term-toggle').addEventListener('change', function() {
            document.getElementById('hacker-terminal').style.display = this.checked ? 'flex' : 'none';
        });

        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playSound(type) {
            if(audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            if (type === 'click') {
                osc.type = 'square'; osc.frequency.setValueAtTime(800, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(400, audioCtx.currentTime + 0.1);
                gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
                osc.start(); osc.stop(audioCtx.currentTime + 0.1);
            } else if (type === 'receive') {
                osc.type = 'sine'; osc.frequency.setValueAtTime(1500, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.02, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
                osc.start(); osc.stop(audioCtx.currentTime + 0.1);
            }
        }
        
        document.addEventListener('click', (e) => {
            if (e.target.tagName === 'BUTTON' || e.target.closest('button')) playSound('click');
        });
'''
if "const audioCtx" not in content:
    content = content.replace('let isGenerating = false;', 'let isGenerating = false;\n' + js_add)

# 6. Stream logic
# We need to find evtSource.onmessage = function(event) {
stream_patch_search = 'evtSource.onmessage = function(event) {'
stream_patch_replace = r'''evtSource.onmessage = function(event) {
                const termBody = document.getElementById('term-body');
                if(termBody && event.data) {
                    termBody.innerText += "\n> " + event.data;
                    termBody.scrollTop = termBody.scrollHeight;
                }
                playSound('receive');
'''
if "termBody.innerText +=" not in content:
    content = content.replace(stream_patch_search, stream_patch_replace)

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("All 4 Features added successfully.")
