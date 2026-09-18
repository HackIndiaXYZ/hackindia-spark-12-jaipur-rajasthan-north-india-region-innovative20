import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_voice = r'''        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
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
        }'''

new_voice = r'''        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition;
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US'; // Force language
            
            recognition.onstart = () => {
                const btn = document.getElementById('mic-btn');
                btn.classList.add('listening');
                btn.style.color = '#f85149'; // Turn red to indicate recording
            };
            
            recognition.onend = () => {
                const btn = document.getElementById('mic-btn');
                btn.classList.remove('listening');
                btn.style.color = 'var(--text-muted)'; // Reset color
            };
            
            recognition.onresult = (e) => {
                if (e.results && e.results[0] && e.results[0][0]) {
                    const transcript = e.results[0][0].transcript;
                    document.getElementById('prompt').value = transcript;
                    sendMessage();
                }
            };
            
            recognition.onerror = (e) => {
                console.error("Speech Recognition Error:", e.error);
                if (e.error === 'no-speech') alert("Nexus: No speech detected. Please check if your microphone is muted.");
                else if (e.error === 'audio-capture') alert("Nexus: No microphone hardware found.");
                else if (e.error === 'not-allowed') alert("Nexus: Microphone permission was denied by your browser.");
            };
        }
        
        function startDictation() {
            if(recognition) {
                try {
                    recognition.start();
                } catch(e) {
                    console.log("Recognition already started or error:", e);
                }
            }
            else alert("Voice recognition is not supported in this browser (Use Chrome or Edge).");
        }'''

if old_voice in content:
    content = content.replace(old_voice, new_voice)
    with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Voice command logic updated!")
else:
    print("Could not find the exact old voice logic block.")
