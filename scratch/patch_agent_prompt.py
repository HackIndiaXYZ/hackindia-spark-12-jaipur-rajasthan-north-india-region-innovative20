import re

with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_prompt = """If the user is just chatting or asking about something established in the PREVIOUS CONVERSATION CONTEXT (like their name), you don't need a huge report. Just give a natural, friendly, formatted response answering their query.
  
  Do NOT mention that you are an AI or talk about the process. Just output the final polished response.
  \"\"\""""

new_prompt = """If the user is just chatting or asking about something established in the PREVIOUS CONVERSATION CONTEXT (like their name), you don't need a huge report. Just give a natural, friendly, formatted response answering their query.
  
  VISUALIZATIONS:
  - You can draw flowcharts using markdown block ```mermaid
  - You can render interactive data charts (bar, pie, line) by outputting a markdown block ```json_chart
    Inside the json_chart block, provide valid JSON matching the Chart.js data structure. For example:
    ```json_chart
    {
      "type": "bar",
      "data": { "labels": ["A", "B"], "datasets": [{"label": "Data", "data": [10, 20], "backgroundColor": "#0f0"}] }
    }
    ```
  
  Do NOT mention that you are an AI or talk about the process. Just output the final polished response.
  \"\"\""""

if "VISUALIZATIONS:" not in content:
    content = content.replace(old_prompt, new_prompt)
    with open('C:/Users/ayush/.gemini/antigravity/scratch/hackathon_agent/agent.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Agent prompt patched!")
else:
    print("Already patched.")
