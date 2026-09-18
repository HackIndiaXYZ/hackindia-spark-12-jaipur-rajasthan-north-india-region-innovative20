import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Debate protocol to add error handling and delays
old_debate = """        is_debate = "debate" in task.lower() or " vs " in task.lower()
        if is_debate:
            yield "log", "--- [System] INITIATING MULTI-AGENT DEBATE PROTOCOL ---"
            yield "log", "[Agent-Alpha] Formulating Argument A..."
            sys_prompt_a = "You are Agent-Alpha. Argue strongly in favor of the FIRST concept mentioned in the user's debate prompt."
            msg_a = [{"role": "user", "parts": [{"text": sys_prompt_a + "\\n\\nDebate Topic: " + task}]}]
            arg_a = self._generate_content(msg_a)
            yield "log", "\\n[Agent-Alpha] " + arg_a[:200] + "..."
            
            yield "log", "\\n--- [Agent-Beta] Formulating Argument B ---"
            sys_prompt_b = "You are Agent-Beta. Argue strongly in favor of the SECOND concept mentioned or counter Agent-Alpha."
            msg_b = [{"role": "user", "parts": [{"text": sys_prompt_b + "\\n\\nDebate Topic: " + task + "\\n\\nAgent-Alpha's Argument:\\n" + arg_a}]}]
            arg_b = self._generate_content(msg_b)
            yield "log", "\\n[Agent-Beta] " + arg_b[:200] + "..."
            
            yield "log", "\\n--- [Agent-Lead (Oracle)] Synthesizing Debate Winner ---"
            sys_prompt_lead = get_synthesizer_prompt(chaos_mode)
            prompt = f"User asked for a debate: {task}\\n\\nAgent-Alpha said:\\n{arg_a}\\n\\nAgent-Beta said:\\n{arg_b}\\n\\nDeclare a clear winner and explain why in a beautiful markdown report."
            msg_lead = [{"role": "user", "parts": [{"text": sys_prompt_lead + "\\n\\n" + prompt}]}]
            final_res = self._generate_content(msg_lead)
            if final_res:
                yield "log", "\\n[Agent-Lead] Debate Synthesis Complete!"
                yield "answer", final_res
            return"""
            
new_debate = """        is_debate = "debate" in task.lower() or " vs " in task.lower()
        if is_debate:
            try:
                yield "log", "--- [System] INITIATING MULTI-AGENT DEBATE PROTOCOL ---"
                yield "log", "[Agent-Alpha] Formulating Argument A..."
                sys_prompt_a = "You are Agent-Alpha. Argue strongly in favor of the FIRST concept mentioned in the user's debate prompt."
                msg_a = [{"role": "user", "parts": [{"text": sys_prompt_a + "\\n\\nDebate Topic: " + task}]}]
                arg_a = self._generate_content(msg_a)
                yield "log", "\\n[Agent-Alpha] " + arg_a[:200] + "..."
                
                time.sleep(2) # Prevent rapid API rate limit
                
                yield "log", "\\n--- [Agent-Beta] Formulating Argument B ---"
                sys_prompt_b = "You are Agent-Beta. Argue strongly in favor of the SECOND concept mentioned or counter Agent-Alpha."
                msg_b = [{"role": "user", "parts": [{"text": sys_prompt_b + "\\n\\nDebate Topic: " + task + "\\n\\nAgent-Alpha's Argument:\\n" + arg_a}]}]
                arg_b = self._generate_content(msg_b)
                yield "log", "\\n[Agent-Beta] " + arg_b[:200] + "..."
                
                time.sleep(2) # Prevent rapid API rate limit
                
                yield "log", "\\n--- [Agent-Lead (Oracle)] Synthesizing Debate Winner ---"
                sys_prompt_lead = get_synthesizer_prompt(chaos_mode)
                prompt = f"User asked for a debate: {task}\\n\\nAgent-Alpha said:\\n{arg_a}\\n\\nAgent-Beta said:\\n{arg_b}\\n\\nDeclare a clear winner and explain why in a beautiful markdown report."
                msg_lead = [{"role": "user", "parts": [{"text": sys_prompt_lead + "\\n\\n" + prompt}]}]
                
                # Attempt final generation with failover if needed
                for _ in range(3):
                    try:
                        final_res = self._generate_content(msg_lead)
                        if final_res:
                            yield "log", "\\n[Agent-Lead] Debate Synthesis Complete!"
                            yield "answer", final_res
                            return
                    except Exception as lead_e:
                        if hasattr(self.team, "rotate_key") and ("403" in str(lead_e) or "429" in str(lead_e)):
                            self.team.rotate_key(for_groq=self.model_name.startswith('groq/'))
                        time.sleep(2)
                        continue
                        
                yield "log", "\\n[Agent-Lead] Synthesis failed due to API rate limit."
                yield "answer", "Debate crashed due to API rate limits. Please try again."
                return
            except Exception as e:
                yield "log", f"\\n[System] Debate Protocol Error: {str(e)}"
                yield "answer", f"Debate protocol crashed due to an API error: {str(e)}"
                return"""

if "try:" not in old_debate and "old_debate" not in content:
    content = content.replace(old_debate, new_debate)

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added error handling and rate limit delays to Debate Protocol!")
