
---

# ⚖️ Legal Brief Generator Pro

**Legal Brief Generator Pro** is a Streamlit-based web application that enables lawyers, students, and legal professionals to **create professional legal documents** and **perform case analysis** with AI assistance. The tool generates structured legal briefs, motions, memos, and contract analyses with the option to include **AI-powered legal research, argument suggestions, and precedent finding**.

---

## 🚀 Features

* **Generate Legal Documents**

  * Motion to Dismiss
  * Summary Judgment Brief
  * Appeals Brief
  * Contract Analysis
  * Case Summary
  * Legal Memorandum

* **AI-Powered Tools**

  * Legal Argument Enhancer
  * Precedent Finder (AI)
  * Legal Research Assistant (experimental)
  * Argument Suggestions

* **Citation Generator**

  * Supports **Bluebook, ALWD, APA** formats

* **Professional UI**

  * Modern Streamlit design with custom CSS
  * Download documents as `.md` files

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/legal-brief-generator.git
cd legal-brief-generator
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

---

## 🔑 API Configuration (Optional for AI Features)

The app integrates with **OpenRouter AI** for AI-powered legal analysis.

1. Get an API key from [OpenRouter](https://openrouter.ai/).
2. Set the key in your environment:

```bash
export OPENROUTER_API_KEY="your_api_key_here"   # Mac/Linux
set OPENROUTER_API_KEY="your_api_key_here"      # Windows (PowerShell)
```

Or configure it inside the Streamlit sidebar.

---

## 📂 Project Structure

```
legal-brief-generator/
│── app.py                 # Main Streamlit app
│── requirements.txt       # Python dependencies
│── README.md              # Project documentation
```

---

## ⚠️ Disclaimer

This tool is for **educational and informational purposes only**.
It does not provide legal advice and should not replace consultation with a qualified attorney.
All generated documents should be **reviewed by licensed legal counsel** before use.

---

## 👨‍💻 Authors

* **Daniel Kasonde**
* **Kateule Kasonde**

---

