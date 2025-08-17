
---

# 📱 Social Media Manager

**Developer:** Daniel Kasonde

An AI-powered **Social Media Manager** built with **Streamlit** and **OpenAI** (via OpenRouter).
This app helps you **create, optimize, and manage content** across multiple platforms like **Twitter/X, LinkedIn, Instagram, Facebook, and WhatsApp** with platform-specific best practices.

---

## 🚀 Features

* 📝 **Create optimized posts** for different platforms
* 🔧 **Optimize existing content** with platform-specific tone and hashtags
* 🏷️ **Hashtag research** (trending + niche hashtags)
* 📅 **7-day content calendar generation**
* 🔍 **Competitor analysis** with insights and strategies
* 📊 **Platform comparison** (character limits, best times, hashtag strategy)
* ⏰ **Best practices and tips** for engagement, timing, and content creation
* ✅ **Real-time character & hashtag counting**

---

## 🛠️ Tech Stack

* **Python 3.9+**
* **Streamlit** – UI and app framework
* **OpenAI (via OpenRouter API)** – AI-powered content generation
* **Regex** – hashtag extraction and character counting

---

## 📂 Project Structure

```
app.py         # Main Streamlit application
```

---

## ⚙️ Installation & Setup

1. **Clone this repository**

```bash
git clone https://github.com/your-username/social-media-manager.git
cd social-media-manager
```

2. **Create a virtual environment & install dependencies**

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

(*Create a `requirements.txt` with: `streamlit openai`*)

3. **Set up environment variables**

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key_here
```

4. **Run the app**

```bash
streamlit run app.py
```

---

## 🎯 How to Use

1. **Select your platform** (Twitter, LinkedIn, Instagram, Facebook, WhatsApp)
2. **Choose a content type** (Create Post, Optimize Post, Hashtag Research, Content Calendar, Competitor Analysis)
3. **Enter your topic, niche, or content**
4. **Generate content** with AI assistance
5. **Review statistics** (character limits, hashtags, word count)
6. **Copy & publish** your optimized post

---

## 📊 Supported Platforms

* 🐦 **Twitter/X** (280 chars, 1–2 hashtags, witty tone)
* 💼 **LinkedIn** (3000 chars, 3–5 hashtags, professional tone)
* 📸 **Instagram** (2200 chars, 20–30 hashtags, engaging tone)
* 👥 **Facebook** (63,206 chars, 1–2 hashtags, community tone)
* 💬 **WhatsApp Status** (700 chars, casual tone)

---

## 🧑‍💻 Developer

**Daniel Kasonde**
*Social Media Manager v1.0*


