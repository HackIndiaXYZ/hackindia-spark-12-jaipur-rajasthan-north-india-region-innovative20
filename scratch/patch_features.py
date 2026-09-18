import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add html2pdf CDN to head
cdn_tag = """<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>"""
content = content.replace('<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>', cdn_tag)


# 2. Add Export PDF and Read Aloud buttons
old_export_block = """                    const exportBtn = document.createElement('button');
                    exportBtn.className = 'export-btn';
                    exportBtn.innerHTML = '💾 Export Mission Report';
                    exportBtn.onclick = () => downloadReport(data.text);
                    markdownContainer.appendChild(exportBtn);"""

new_export_block = """                    // Action Buttons Container
                    const actionContainer = document.createElement('div');
                    actionContainer.style.display = 'flex';
                    actionContainer.style.gap = '10px';
                    actionContainer.style.marginTop = '15px';

                    // MD Export Button
                    const exportBtn = document.createElement('button');
                    exportBtn.className = 'export-btn';
                    exportBtn.innerHTML = '💾 MD';
                    exportBtn.title = "Download Markdown";
                    exportBtn.onclick = () => downloadReport(data.text);
                    actionContainer.appendChild(exportBtn);

                    // PDF Export Button
                    const pdfBtn = document.createElement('button');
                    pdfBtn.className = 'export-btn';
                    pdfBtn.innerHTML = '📄 PDF';
                    pdfBtn.title = "Download PDF";
                    pdfBtn.style.background = 'linear-gradient(45deg, #cc0000, #ff3333)';
                    pdfBtn.onclick = () => {
                        const opt = {
                          margin:       10,
                          filename:     'Nexus_Mission_Report.pdf',
                          image:        { type: 'jpeg', quality: 0.98 },
                          html2canvas:  { scale: 2 },
                          jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
                        };
                        html2pdf().set(opt).from(markdownContainer).save();
                    };
                    actionContainer.appendChild(pdfBtn);

                    // Text-To-Speech Audio Button
                    const audioBtn = document.createElement('button');
                    audioBtn.className = 'export-btn';
                    audioBtn.innerHTML = '🔊 Read Aloud';
                    audioBtn.title = "Play AI Voice";
                    audioBtn.style.background = 'linear-gradient(45deg, #0088cc, #00bbff)';
                    let isPlaying = false;
                    audioBtn.onclick = () => {
                        if (isPlaying) {
                            window.speechSynthesis.cancel();
                            audioBtn.innerHTML = '🔊 Read Aloud';
                            isPlaying = false;
                        } else {
                            // Strip HTML tags and markdown for reading
                            const strippedText = data.text.replace(/<[^>]*>?/gm, '').replace(/#/g, '').replace(/\\*/g, '');
                            const utterance = new SpeechSynthesisUtterance(strippedText);
                            utterance.lang = 'en-US';
                            utterance.rate = 1.05;
                            window.speechSynthesis.speak(utterance);
                            audioBtn.innerHTML = '🛑 Stop Reading';
                            isPlaying = true;
                            
                            utterance.onend = () => {
                                audioBtn.innerHTML = '🔊 Read Aloud';
                                isPlaying = false;
                            };
                        }
                    };
                    actionContainer.appendChild(audioBtn);

                    markdownContainer.appendChild(actionContainer);"""

if "html2pdf" not in content:
    content = content.replace(old_export_block, new_export_block)

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected PDF Export and TTS Audio features!")
