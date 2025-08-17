
---

# 🏥 MedAssist AI - Clinical Decision Support Tool

**MedAssist AI** is a Streamlit-based application designed to provide **AI-powered clinical decision support** for healthcare professionals.
It assists with **symptom analysis, differential diagnosis, drug interaction checks, lab interpretation, and patient assessment history**.
The app integrates with **OpenRouter AI** to deliver evidence-based suggestions while emphasizing that clinical judgment remains essential.

---

## 🚀 Features

* **Symptom Analysis** → Provides likely conditions, red flag symptoms, diagnostic tests, and urgency assessment.
* **Differential Diagnosis Assistant** → Generates differential diagnoses with distinguishing features and recommended workups.
* **Drug Interaction Checker** → Evaluates drug-drug interactions, contraindications, and alternative recommendations.
* **Laboratory Results Interpreter** → Interprets lab values (manual entry or file upload) with clinical context.
* **Patient Assessment History** → Saves and retrieves recent analyses.
* **Clinical Reports & Analytics** → Displays case volumes, emergency trends, and activity logs.
* **Settings Panel** → Configure API keys, preferences, and institutional settings.

⚠️ **Important Disclaimer:**
This tool is for **educational and decision-support purposes only**. Always consult with qualified medical professionals and institutional protocols.

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/medassist-ai.git
cd medassist-ai
```

### 2. Create Virtual Environment

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

## 🔑 API Configuration (AI Features)

1. Get a free API key from [OpenRouter](https://openrouter.ai/).
2. Set it as an environment variable:

```bash
export OPENAI_API_KEY="your_api_key_here"   # Mac/Linux
set OPENAI_API_KEY="your_api_key_here"      # Windows (PowerShell)
```

Or enter it in the **Settings** tab inside the app.

---

## 📂 Project Structure

```
medassist-ai/
│── app.py               # Main Streamlit app
│── requirements.txt     # Dependencies
│── README.md            # Documentation
```

---

## 👨‍⚕️ Authors

* **Your Name / Team Name**

---

## ⚠️ Disclaimer

MedAssist AI is **NOT a substitute for professional medical judgment**.
It is an **educational and decision-support tool only**. All outputs must be verified by a licensed healthcare provider.

---

# ✅ requirements.txt

Here’s the dependency file based on the imports in your code:

```txt
streamlit>=1.32.0
openai>=1.0.0
pandas>=2.0.0
```

---
