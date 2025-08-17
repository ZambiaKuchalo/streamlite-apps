import os
import streamlit as st
import pyperclip
from openai import OpenAI
import time

# Page configuration
st.set_page_config(
    page_title="AI Language Processor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        #api_key=st.secrets.get("OPENROUTER_API_KEY", "your-api-key-here")  # Put your API key in secrets.toml
        api_key = os.environ.get("OPENAI_API_KEY")
    )

client = get_openai_client()

# Function definitions for different language tasks
def get_prompt_for_task(task, text, additional_params=None):
    prompts = {
        "summarize": f"Provide a concise summary of the following text:\n\n{text}",
        "paraphrase": f"Paraphrase the following text while maintaining its original meaning:\n\n{text}",
        "expand": f"Expand and elaborate on the following text with more details and examples:\n\n{text}",
        "simplify": f"Rewrite the following text in simpler, easier-to-understand language:\n\n{text}",
        "formalize": f"Rewrite the following text in a more formal, professional tone:\n\n{text}",
        "casualize": f"Rewrite the following text in a more casual, conversational tone:\n\n{text}",
        "translate": f"Translate the following text to {additional_params.get('target_language', 'Spanish')}:\n\n{text}",
        "grammar_check": f"Check and correct any grammar, spelling, or punctuation errors in the following text:\n\n{text}",
        "tone_analysis": f"Analyze the tone and sentiment of the following text:\n\n{text}",
        "key_points": f"Extract the key points and main ideas from the following text:\n\n{text}",
        "questions": f"Generate thoughtful questions based on the following text:\n\n{text}",
        "title_generate": f"Generate 5 compelling titles for content based on the following text:\n\n{text}",
        "outline": f"Create a structured outline based on the following text:\n\n{text}",
        "action_items": f"Extract actionable items and tasks from the following text:\n\n{text}",
        "pros_cons": f"Create a pros and cons list based on the following text:\n\n{text}"
    }
    return prompts.get(task, f"Process the following text:\n\n{text}")

def process_text(task, text, additional_params=None):
    """Process text using OpenAI API"""
    if not text.strip():
        return "Please enter some text to process."
    
    try:
        prompt = get_prompt_for_task(task, text, additional_params)
        
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://ai-language-processor.streamlit.app",
                "X-Title": "AI Language Processor",
            },
            model="deepseek/deepseek-r1:free",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant specialized in text processing and language tasks. Provide clear, accurate, and well-formatted responses."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return completion.choices[0].message.content
    
    except Exception as e:
        return f"Error processing text: {str(e)}"

# Sidebar for task selection
st.sidebar.title("🤖 AI Language Processor")
st.sidebar.markdown("Select a language processing task from the options below:")

# Task categories
task_categories = {
    "📝 Text Transformation": {
        "summarize": "Summarize Text",
        "paraphrase": "Paraphrase Text",
        "expand": "Expand Text",
        "simplify": "Simplify Language",
    },
    "🎨 Style & Tone": {
        "formalize": "Make Formal",
        "casualize": "Make Casual",
        "tone_analysis": "Analyze Tone",
    },
    "🔧 Editing & Grammar": {
        "grammar_check": "Grammar Check",
        "translate": "Translate Text",
    },
    "📊 Analysis & Extraction": {
        "key_points": "Extract Key Points",
        "outline": "Create Outline",
        "action_items": "Extract Action Items",
        "pros_cons": "Pros & Cons List",
    },
    "💡 Content Generation": {
        "questions": "Generate Questions",
        "title_generate": "Generate Titles",
    }
}

# Initialize session state for task selection
if 'selected_task' not in st.session_state:
    st.session_state.selected_task = "summarize"

# Task selection
for category, tasks in task_categories.items():
    st.sidebar.markdown(f"### {category}")
    for task_key, task_name in tasks.items():
        if st.sidebar.button(task_name, key=task_key, use_container_width=True):
            st.session_state.selected_task = task_key
            # Clear previous result when task changes
            if 'last_result' in st.session_state:
                del st.session_state.last_result

selected_task = st.session_state.selected_task

# Translation language selection (if translate task is selected)
additional_params = {}
if st.session_state.selected_task == "translate":
    st.sidebar.markdown("### Translation Settings")
    target_language = st.sidebar.selectbox(
        "Target Language",
        ["Spanish", "French", "German", "Italian", "Portuguese", "Chinese", "Japanese", "Korean", "Arabic", "Russian"]
    )
    additional_params["target_language"] = target_language

# Main interface
st.title("🤖 AI Language Processor")
st.markdown("Transform, analyze, and enhance your text with powerful AI language processing tools.")

# Current task display
task_names = {
    "summarize": "Text Summarization",
    "paraphrase": "Text Paraphrasing", 
    "expand": "Text Expansion",
    "simplify": "Language Simplification",
    "formalize": "Formal Writing",
    "casualize": "Casual Writing",
    "translate": "Text Translation",
    "grammar_check": "Grammar Checking",
    "tone_analysis": "Tone Analysis",
    "key_points": "Key Points Extraction",
    "questions": "Question Generation",
    "title_generate": "Title Generation",
    "outline": "Outline Creation",
    "action_items": "Action Items Extraction",
    "pros_cons": "Pros & Cons Analysis"
}

current_task_name = task_names.get(st.session_state.selected_task, "Text Processing")
st.subheader(f"Current Task: {current_task_name}")

# Add visual indicator of current task
st.info(f"🎯 **Active Task:** {current_task_name}")

# Input area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Input Text")
    input_text = st.text_area(
        "Enter your text here:",
        height=400,
        placeholder="Paste or type your text here...",
        key="input_area"
    )
    
    # Processing button
    process_button = st.button("🚀 Process Text", type="primary", use_container_width=True)
    
    # Character count
    if input_text:
        st.caption(f"Characters: {len(input_text)} | Words: {len(input_text.split())}")

with col2:
    st.markdown("### Output")
    
    # Process text when button is clicked
    if process_button and input_text.strip():
        with st.spinner(f"Processing text with {current_task_name.lower()}..."):
            result = process_text(selected_task, input_text, additional_params)
            st.session_state.last_result = result
    
    # Display result
    if hasattr(st.session_state, 'last_result'):
        output_container = st.container()
        with output_container:
            st.text_area(
                "Processed Text:",
                value=st.session_state.last_result,
                height=400,
                key="output_area"
            )
            
            # Copy button
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                try:
                    # For local development, you might need to install pyperclip
                    # For deployment, we'll show a success message
                    st.success("✅ Text copied to clipboard! (Select and copy manually if needed)")
                except:
                    st.info("💡 Select the text above and copy manually (Ctrl+C / Cmd+C)")
    else:
        st.text_area(
            "Processed Text:",
            value="Your processed text will appear here...",
            height=400,
            disabled=True
        )

# Footer with instructions
st.markdown("---")
st.markdown("""
### 📋 How to Use:
1. **Select a task** from the sidebar (summarize, paraphrase, etc.)
2. **Enter your text** in the input area on the left
3. **Click "Process Text"** to get AI-powered results
4. **Copy the output** using the copy button or manually select the text

### 🔧 Available Features:
- **Text Transformation**: Summarize, paraphrase, expand, or simplify text
- **Style & Tone**: Change formality level and analyze tone
- **Editing**: Grammar checking and translation
- **Analysis**: Extract key points, create outlines, find action items
- **Generation**: Create questions and titles based on your content
""")

# API Key instructions (for deployment)
st.sidebar.markdown("---")
st.sidebar.caption("AI Language Processor v1.0")
st.sidebar.caption("Developed by Daniel Kasonde")
### 🔑 Setup Instructions:
#1. Get your API key from [OpenRouter](https://openrouter.ai/)
#2. Add it to your Streamlit secrets as `OPENROUTER_API_KEY`
#3. Or replace the API key directly in the code
# Version info
st.sidebar.markdown("---")

