import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Mermaid script
content = content.replace(
    '<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>',
    '<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>\n    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>'
)

# 2. Add CSS
css_addition = r'''
        .mic-btn {
            background: transparent;
            color: var(--text-muted);
            border: 1px solid var(--border);
            width: 40px; height: 40px;
            border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            cursor: pointer; transition: all 0.2s;
            margin-bottom: 2px;
        }
        .mic-btn:hover, .mic-btn.listening {
            color: var(--accent-primary);
            border-color: var(--accent-primary);
            box-shadow: var(--glow-primary);
        }
        .mic-btn svg { width: 18px; height: 18px; fill: currentColor; }
        
        .export-btn {
            margin-top: 16px;
            background: rgba(0, 200, 255, 0.1);
            border: 1px solid var(--accent-secondary);
            color: var(--accent-secondary);
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 12px; font-family: var(--font-mono);
            cursor: pointer; transition: all 0.2s;
            display: inline-flex; align-items: center; gap: 8px;
        }
        .export-btn:hover {
            background: rgba(0, 200, 255, 0.2);
            box-shadow: 0 0 15px rgba(0,200,255,0.3);
        }
'''
content = content.replace('/* --- Chat Input Dock --- */', css_addition + '/* --- Chat Input Dock --- */')

# 3. Add Mic Button HTML
mic_html = '''<button class="mic-btn" onclick="startDictation()" id="mic-btn" title="Voice Command">
                        <svg viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>
                    </button>
                    <button class="send-btn"'''
content = content.replace('<button class="send-btn"', mic_html)

# 4. Add JS Logic (Init Mermaid & Voice)
js_init = r'''
        mermaid.initialize({ startOnLoad: false, theme: 'dark' });

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition;
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.onstart = () => document.getElementById('mic-btn').classList.add('listening');
            recognition.onend = () => document.getElementById('mic-btn').classList.remove('listening');
            recognition.onresult = (e) => {
                document.getElementById('prompt').value = e.results[0][0].transcript;
                sendMessage();
            };
        }
        function startDictation() {
            if(recognition) recognition.start();
            else alert("Voice recognition not supported in this browser.");
        }
        
        function downloadReport(text) {
            const blob = new Blob([text], {type: "text/markdown"});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "Nexus_Mission_Report.md";
            a.click();
            URL.revokeObjectURL(url);
        }

        // Auto-growing textarea
'''
content = content.replace('// Auto-growing textarea', js_init)

# 5. Modify JS Answer rendering logic
old_answer_logic = r'''                else if (data.type === "answer") {
                    accordion.removeAttribute('open');
                    markdownContainer.style.display = 'block';
                    markdownContainer.innerHTML = marked.parse(data.text);
                    addCodeCopyButtons(agentRow);
                    scrollToBottom();
                    evtSource.close();'''

new_answer_logic = r'''                else if (data.type === "answer") {
                    accordion.removeAttribute('open');
                    markdownContainer.style.display = 'block';
                    
                    let htmlContent = marked.parse(data.text);
                    htmlContent = htmlContent.replace(/<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/g, '<div class="mermaid">$1</div>');
                    markdownContainer.innerHTML = htmlContent;
                    
                    const exportBtn = document.createElement('button');
                    exportBtn.className = 'export-btn';
                    exportBtn.innerHTML = '📥 Export Mission Report';
                    exportBtn.onclick = () => downloadReport(data.text);
                    markdownContainer.appendChild(exportBtn);
                    
                    addCodeCopyButtons(agentRow);
                    
                    setTimeout(() => {
                        try { mermaid.run({ querySelector: '.mermaid' }); } catch(e) { console.error(e); }
                        scrollToBottom();
                    }, 100);
                    
                    evtSource.close();'''

if old_answer_logic in content:
    content = content.replace(old_answer_logic, new_answer_logic)
else:
    print("Warning: Could not find old answer logic.")

# Modify history loading answer logic as well
old_hist_logic = 'markdownContainer.innerHTML = marked.parse(entry.answer);'
new_hist_logic = r'''let htmlContent = marked.parse(entry.answer);
                            htmlContent = htmlContent.replace(/<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/g, '<div class="mermaid">$1</div>');
                            markdownContainer.innerHTML = htmlContent;
                            setTimeout(() => { try { mermaid.run({ querySelector: '.mermaid' }); } catch(e) {} }, 100);'''

if 'markdownContainer.innerHTML = marked.parse(entry.answer);' in content:
    print("Warning: Found alternative old hist logic")
else:
    # Let's target the exact line in history
    old_hist_2 = '<div class="bubble-content markdown-body">${marked.parse(entry.answer)}</div>'
    new_hist_2 = r'''<div class="bubble-content markdown-body">${marked.parse(entry.answer).replace(/<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/g, '<div class="mermaid">$1</div>')}</div>'''
    content = content.replace(old_hist_2, new_hist_2)

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Features added successfully.")
