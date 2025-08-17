import streamlit as st
import requests
import json
from datetime import datetime
import time

# Configure the page
st.set_page_config(
    page_title="NeuroSphere AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for fancy styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid;
        animation: fadeIn 0.5s ease-in;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .assistant-message {
        background-color: #f1f8e9;
        border-left-color: #4caf50;
    }
    
    .error-message {
        background-color: #ffebee;
        border-left-color: #f44336;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .model-selector {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🧠 NeuroSphere AI</h1>
    <h3>Advanced Language Model Testing Interface</h3>
    <p>Developed by Daniel Kasonde • Test multiple LLMs seamlessly</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0

# Sidebar configuration
with st.sidebar:
    st.markdown('<div class="model-selector"><h2>🚀 Configuration</h2></div>', unsafe_allow_html=True)
    
    # Default API Key - Replace with your actual API key
    DEFAULT_API_KEY = "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"  # Replace this with your actual API key
    
    # API Key input with default value
    api_key = st.text_input(
        "OpenRouter API Key", 
        value=DEFAULT_API_KEY if DEFAULT_API_KEY != "YOUR_OPENROUTER_API_KEY_HERE" else "",
        type="password", 
        help="Enter your OpenRouter API key (or use the default one set in code)"
    )
    
    # Model selection
    model_options = [
        "deepseek/deepseek-r1:free",
        "meta-llama/llama-3.2-3b-instruct:free",
        "microsoft/phi-3-mini-128k-instruct:free",
        "google/gemma-2-9b-it:free",
        "qwen/qwen-2-7b-instruct:free",
        "openchat/openchat-7b:free",
        "gryphe/mythomist-7b:free",
        "huggingfaceh4/zephyr-7b-beta:free"
    ]
    
    selected_model = st.selectbox(
        "Select Language Model",
        model_options,
        help="Choose the LLM you want to test"
    )
    
    # Additional parameters
    st.markdown("### 🔧 Model Parameters")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1, help="Controls randomness in responses")
    max_tokens = st.slider("Max Tokens", 100, 4000, 1000, 100, help="Maximum response length")
    
    # Site information (optional)
    site_url = st.text_input("Your Site URL (optional)", help="For OpenRouter rankings")
    site_name = st.text_input("Your Site Name (optional)", help="For OpenRouter rankings")
    
    # Statistics
    st.markdown("### 📊 Session Stats")
    st.markdown(f"""
    <div class="stats-card">
        <h4>Messages: {len(st.session_state.messages)}</h4>
    </div>
    <div class="stats-card">
        <h4>Model: {selected_model.split('/')[-1].split(':')[0]}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", type="secondary"):
        st.session_state.messages = []
        st.session_state.total_tokens = 0
        st.session_state.conversation_count = 0
        st.rerun()

# Main chat interface
st.markdown("### 💬 Chat Interface")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>🧑 You:</strong><br>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 NeuroSphere AI:</strong><br>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)

# Function to call OpenRouter API
def call_openrouter_api(messages, model, api_key, temperature=0.7, max_tokens=1000, site_url="", site_name=""):
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        # Add optional headers if provided
        if site_url:
            headers["HTTP-Referer"] = site_url
        if site_name:
            headers["X-Title"] = site_name
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    if not api_key:
        st.error("⚠️ Please enter your OpenRouter API key in the sidebar!")
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show typing indicator
        with st.spinner("🤖 NeuroSphere AI is thinking..."):
            # Call the API
            response = call_openrouter_api(
                st.session_state.messages,
                selected_model,
                api_key,
                temperature,
                max_tokens,
                site_url,
                site_name
            )
        
        if "error" in response:
            st.error(f"❌ {response['error']}")
            st.markdown(f"""
            <div class="chat-message error-message">
                <strong>⚠️ Error:</strong><br>
                {response['error']}
            </div>
            """, unsafe_allow_html=True)
        else:
            # Extract the assistant's response
            assistant_response = response['choices'][0]['message']['content']
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Update session stats
            if 'usage' in response:
                st.session_state.total_tokens += response['usage'].get('total_tokens', 0)
            
            st.session_state.conversation_count += 1
        
        # Rerun to show the new messages
        st.rerun()

# Footer
# st.markdown("---")
# col1, col2, col3 = st.columns(3)

# with col1:
#     st.markdown("**🔗 Powered by:**")
#     st.markdown("[OpenRouter](https://openrouter.ai/)")

# with col2:
#     st.markdown("**📚 Model Info:**")
#     st.markdown(f"Current: `{selected_model}`")

# with col3:
#     st.markdown("**⚡ Features:**")
#     st.markdown("Multi-model • Real-time • Customizable")

# # Instructions
# with st.expander("📖 How to Use NeuroSphere AI"):
#     st.markdown("""
#     ### Getting Started:
#     1. **Get API Key**: Sign up at [OpenRouter](https://openrouter.ai/) and get your free API key
#     2. **Enter Key**: Paste your API key in the sidebar
#     3. **Select Model**: Choose from various free language models
#     4. **Configure**: Adjust temperature and max tokens as needed
#     5. **Chat**: Start conversing with the AI!
    
#     ### Features:
#     - 🎯 **Multiple Models**: Test different LLMs side by side
#     - ⚙️ **Customizable**: Adjust temperature, max tokens, and more
#     - 📊 **Session Stats**: Track your usage and conversation history
#     - 🎨 **Modern UI**: Beautiful, responsive interface
#     - 🆓 **Free Models**: Access to various free language models
    
#     ### Tips:
#     - Lower temperature (0.1-0.3) for more focused responses
#     - Higher temperature (0.8-1.5) for more creative outputs
#     - Adjust max tokens based on desired response length
#     """)
# <code>pip install streamlit requests</code>
# Error handling for missing dependencies
st.markdown("""
---
<small>
<b>Dependencies:</b>AI generated content may be harmful.:<br>

</small>
""", unsafe_allow_html=True)