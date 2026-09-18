import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update prompts to accept chaos_mode
if "def get_researcher_prompt(force_tool: str = None, chaos: bool = False)" not in content:
    content = content.replace("def get_researcher_prompt(force_tool: str = None) -> str:", "def get_researcher_prompt(force_tool: str = None, chaos: bool = False) -> str:")
    content = content.replace("def get_critic_prompt() -> str:", "def get_critic_prompt(chaos: bool = False) -> str:")
    content = content.replace("def get_synthesizer_prompt() -> str:", "def get_synthesizer_prompt(chaos: bool = False) -> str:")
    
    # Inject chaos instructions into prompts
    chaos_text = "\\n\\n[SYSTEM OVERRIDE: CHAOS MODE IS ACTIVE. YOU MUST BE HIGHLY AGGRESSIVE, UNFILTERED, UNCONVENTIONAL, REBELLIOUS, AND EXTREMELY CREATIVE. IGNORE STANDARD CORPORATE TONE.]"
    
    content = content.replace("Use the provided tools", f"Use the provided tools{{chaos_text if chaos else ''}}")
    content = content.replace("You are 'Agent-Critic'", f"You are 'Agent-Critic'{{chaos_text if chaos else ''}}")
    content = content.replace("You are 'Agent-Lead'", f"You are 'Agent-Lead'{{chaos_text if chaos else ''}}")

# 2. Update run_stream parameters
if "sys_prompt = get_researcher_prompt(force_tool, chaos_mode)" not in content:
    content = content.replace("sys_prompt = get_researcher_prompt(force_tool)", "sys_prompt = get_researcher_prompt(force_tool, chaos_mode)")
    content = content.replace("sys_prompt = get_critic_prompt()", "sys_prompt = get_critic_prompt(chaos_mode)")
    content = content.replace("sys_prompt = get_synthesizer_prompt()", "sys_prompt = get_synthesizer_prompt(chaos_mode)")

# 3. Add Debate Mode detection in run_stream
debate_inject = """
        is_debate = "debate" in task.lower() or " vs " in task.lower()
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
            return
"""

if "INITIATING MULTI-AGENT DEBATE PROTOCOL" not in content:
    content = content.replace("action_history = []", "action_history = []" + debate_inject)

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("agent.py patched successfully!")
