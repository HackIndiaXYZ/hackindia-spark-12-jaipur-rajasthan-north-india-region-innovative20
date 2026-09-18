with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix CriticAgent signature
content = content.replace("def run_stream(self, task: str, raw_data: str):", "def run_stream(self, task: str, raw_data: str, chaos_mode: bool = False):", 1)

# Fix SynthesizerAgent signature
content = content.replace("def run_stream(self, original_task: str, raw_data: str):", "def run_stream(self, original_task: str, raw_data: str, chaos_mode: bool = False):", 1)

# Fix MultiAgentTeam calls
content = content.replace("self.critic.run_stream(task, raw_data)", "self.critic.run_stream(task, raw_data, chaos_mode)")
content = content.replace("self.lead.run_stream(enriched_task, raw_data)", "self.lead.run_stream(enriched_task, raw_data, chaos_mode)")

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed Agent Critic NameError bug!")
