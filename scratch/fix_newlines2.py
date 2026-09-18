with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'context = "--- PREVIOUS CONVERSATION CONTEXT ---' in line:
        if line.endswith('"\n') or line.endswith('"'):
            pass
        else:
            lines[i] = '        context = "--- PREVIOUS CONVERSATION CONTEXT ---\\n"\n'
            # remove next line if it's just a quote
            if lines[i+1].strip() == '"' or lines[i+1].strip() == '""':
                lines[i+1] = ""
    elif 'context += f"Recent Query {i+1}: {entry.get(\'task\', \'\')}' in line:
        if line.endswith('"\n') or line.endswith('"'):
            pass
        else:
            lines[i] = '            context += f"Recent Query {i+1}: {entry.get(\'task\', \'\')}\\n"\n'
            if lines[i+1].strip() == '"': lines[i+1] = ""
    elif 'ans[:400] + "...' in line:
        if line.endswith('"\n') or line.endswith('"'):
            pass
        else:
            lines[i] = '            if len(ans) > 400: ans = ans[:400] + "...\\n(truncated)"\n'
            if lines[i+1].strip() == '"': lines[i+1] = ""
    elif 'context += f"Recent Answer {i+1}: {ans}' in line:
        if line.endswith('"\n') or line.endswith('"'):
            pass
        else:
            lines[i] = '            context += f"Recent Answer {i+1}: {ans}\\n\\n"\n'
            if lines[i+1].strip() == '"': lines[i+1] = ""
    elif 'context += "--------------------------------------' in line:
        if line.endswith('"\n') or line.endswith('"'):
            pass
        else:
            lines[i] = '        context += "--------------------------------------\\n"\n'
            if lines[i+1].strip() == '"': lines[i+1] = ""
    elif 'return "\\n\\n".join(best_chunks)' in line:
        if line.endswith(')\n') or line.endswith(')'):
            pass
        else:
            lines[i] = '    return "\\n\\n".join(best_chunks)\n'
            if lines[i+1].strip() == '"': lines[i+1] = ""

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
