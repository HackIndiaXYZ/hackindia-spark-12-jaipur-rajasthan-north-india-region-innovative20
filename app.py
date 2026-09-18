import streamlit as st
from agent import ReActAgent
import time

# --- Page Config ---
st.set_page_config(page_title="Competitor Tracking AI", page_icon="🕵️", layout="wide")

# --- Custom CSS for attractiveness ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .title-text {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3256/3256729.png", width=100)
    st.header("⚙️ Agent Settings")
    st.markdown("Customize your autonomous agent.")
    
    # Let the user input an API key dynamically if they don't have .env
    user_api_key = st.text_input("Gemini API Key (Optional if in .env)", type="password")
    
    max_turns = st.slider("Max Reasoning Loops", min_value=3, max_value=10, value=5)
    st.markdown("---")
    st.markdown("### Available Tools:")
    st.markdown("- 🌐 **Wikipedia Search**")
    st.markdown("- 📜 **Patent Database Search**")

# --- Main UI ---
st.markdown('<p class="title-text">Autonomous Research Agent</p>', unsafe_allow_html=True)
st.markdown("**Hackathon Edition** 🚀 — Enter a competitor to analyze, and watch the agent's brain work live.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("E.g., Research OpenAI and find their recent patents."):
    
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. Show agent response
    with st.chat_message("assistant", avatar="🤖"):
        
        # Use st.status for a beautiful "Agent is thinking" dropdown!
        with st.status("🕵️ Agent is initializing...", expanded=True) as status:
            try:
                # Use the API key from the sidebar if provided, otherwise it falls back to .env
                api_key_to_use = user_api_key if user_api_key else None
                agent = ReActAgent(api_key=api_key_to_use)
                
                full_log = ""
                final_answer = ""
                
                # Stream the thoughts live into the status box
                log_placeholder = st.empty()
                
                for update_type, text in agent.run_stream(prompt, max_turns=max_turns):
                    if update_type == "log":
                        # If the agent is executing a tool, update the status title to look cool
                        if "[Executing Tool:" in text:
                            tool_name = text.split("Executing Tool: ")[1].split(" ")[0]
                            status.update(label=f"🔧 Executing Tool: {tool_name}...", state="running")
                        elif "Thought:" in text:
                            status.update(label="🧠 Reasoning...", state="running")
                            
                        full_log += text + "\n"
                        log_placeholder.markdown(f"```text\n{full_log[-1000:]}\n```") 
                        
                    elif update_type == "answer":
                        final_answer = text
                
                # Close the status box beautifully
                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                
                # Print the final beautiful markdown
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
                
                # Add a download button for the report
                st.download_button(
                    label="📄 Download Report as Markdown",
                    data=final_answer,
                    file_name="competitor_report.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                status.update(label="❌ Error occurred", state="error")
                st.error(f"Error: {e}")
                if "API_KEY" in str(e):
                    st.warning("Please paste your Gemini API Key in the sidebar ⚙️")
