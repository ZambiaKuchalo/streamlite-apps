# 🧠 NeuroSphere AI

**Advanced Language Model Testing Interface**

NeuroSphere AI is a **Streamlit-based web app** for testing and comparing multiple Large Language Models (LLMs) through the [OpenRouter API](https://openrouter.ai/).  
Developed by **Daniel Kasonde**, it provides a sleek chat interface, real-time responses, and easy configuration of model parameters.

---

## ✨ Features
- 🚀 **Multi-model support** – Choose from several LLMs (DeepSeek, LLaMA, Phi-3, Gemma, Qwen, and more).
- ⚡ **Real-time chat** – Seamless back-and-forth conversation.
- 🎨 **Modern UI** – Custom CSS styling with a responsive interface.
- 🔧 **Configurable parameters** – Adjust temperature, max tokens, and site metadata.
- 📊 **Session stats** – Track message counts, model usage, and conversation history.
- 🗑️ **Clear chat** – Reset the conversation instantly.

---

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/neurosphere-ai.git
   cd neurosphere-ai
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open the app in your browser (default: `http://localhost:8501`).

3. Enter your **OpenRouter API key** in the sidebar.  
   - Get a free API key from [OpenRouter](https://openrouter.ai/).

4. Select a model, configure parameters, and start chatting! 🎉

---

## ⚠️ Notes
- Replace the **default API key** in the code with your own for security.  
- Some models may have usage limits depending on OpenRouter’s terms.

---

## 👨‍💻 Author
**Daniel Kasonde**  
🚀 Passionate about AI, LLMs, and creating modern interactive tools.

---

## 📜 License
MIT License – Free to use, modify, and distribute.
