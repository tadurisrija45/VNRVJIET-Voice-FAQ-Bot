# VNR VJIET Voice FAQ Assistant

An intelligent, voice-in and voice-out FAQ web application built for **Vallurupalli Nageswara Rao Vignana Jyothi Institute of Engineering and Technology (VNR VJIET)**, Hyderabad.

The system allows students, parents, and visitors to ask questions about the college using either **voice** or **text**, performs intelligent hybrid retrieval over the comprehensive college knowledge base, generates grounded answers using OpenAI LLM (or direct verified database retrieval), and speaks the answer aloud using speech synthesis.

---

## 📌 Features

- 🎤 **Voice Input (Speech-to-Text)**: Speak naturally into your browser microphone; questions are transcribed in real-time.
- ⌨️ **Text Input**: Type questions with automatic validation and suggestion chips for popular topics.
- 📚 **VNR VJIET Knowledge Base**: Rich CSV database covering admissions, branches, cutoffs, fee structure, placements, fests, hostels, transport, and campus facilities.
- 🔍 **Hybrid Search Engine**: Combines TF-IDF vectorization, Cosine Similarity, Keyword Overlap, and Fuzzy Typo Matching for high-precision retrieval.
- 🧠 **AI-Powered Grounded Answers**: OpenAI LLM (`gpt-4o-mini`) integration with strict anti-hallucination prompting.
- 🛡️ **Zero Hallucination Guarantee**: If information is not in the database, the bot safely responds: *"I'm sorry, I couldn't find that information in the VNR VJIET FAQ database."*
- 🔊 **Voice Output (Text-to-Speech)**: Integrated browser speech synthesis with customized phonetic pronunciation for college terms (e.g. *VNR VJIET*, *JNTUH*, *LPA*, *INR*, *NAAC A++*).
- 💬 **Conversation History & Clear Chat**: View the ongoing discussion and clear chat history at any time.
- 📱 **Modern Responsive UI**: Clean, academic-themed design optimized for mobile, tablet, and desktop screens.

---

## 🏗️ Mandatory Project Structure

This project strictly adheres to the following fixed architecture:

```text
VNRVJIET-Voice-FAQ-Bot/
│
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── data/
│   └── VNRVJIET_COMPLETE_DATABASE.csv
│
├── services/
│   ├── __init__.py
│   ├── speech_to_text.py
│   ├── faq_search.py
│   ├── llm.py
│   └── text_to_speech.py
│
├── utils/
│   ├── __init__.py
│   └── helpers.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   └── images/
│       └── vnrvjiet-logo.png
│
└── templates/
    └── index.html
```

---

## 🛠️ Tech Stack & Technologies

| Layer | Technologies | Purpose |
|---|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) | Modern academic responsive UI, speech recognition & synthesis |
| **Backend** | Python 3, Flask | RESTful API (`/api/ask`), route handling, server logic |
| **Knowledge Base** | CSV (`pandas`, `scikit-learn`) | TF-IDF + Cosine Similarity hybrid semantic search |
| **AI / LLM** | OpenAI API (`gpt-4o-mini`) | Context-grounded conversational response generation |
| **Voice / Speech** | Web Speech API (`SpeechRecognition`, `SpeechSynthesis`) | Browser-native low-latency voice-in and voice-out |

---

## 🔄 Complete Voice Flow Architecture

```text
User speaks question
         ↓
Browser Microphone
         ↓
Web Speech API (SpeechRecognition)
         ↓
Question Transcript
         ↓
JavaScript Fetch (POST /api/ask)
         ↓
Flask Application (app.py)
         ↓
FAQ Search Engine (services/faq_search.py)
         ↓
Searches data/VNRVJIET_COMPLETE_DATABASE.csv
         ↓
Retrieved FAQ Context
         ↓
LLM Grounding (services/llm.py)
         ↓
Validated JSON Response
         ↓
Frontend Renders Conversation Bubble
         ↓
Speech Synthesis (services/text_to_speech.py / window.speechSynthesis)
         ↓
🔊 User Hears Spoken Answer
```

---

## 🚀 Installation & Setup (Windows PowerShell)

### 1. Clone or Navigate to Project Directory

```powershell
cd c:\Users\tadur\OneDrive\Desktop\VNRVJIET-Voice-FAQ-Bot
```

### 2. Create and Activate Virtual Environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and configure your OpenAI API key (optional — if no key is provided, the bot uses direct verified knowledge base retrieval):

```env
OPENAI_API_KEY=your_actual_openai_api_key_here
PORT=5000
DEBUG=True
```

---

## ▶️ Running the Application

Start the Flask server:

```powershell
python app.py
```

Open your web browser and navigate to:

```text
http://127.0.0.1:5000
```

---

## 🧪 Testing Scenarios

| Test Case | Expected Behavior |
|---|---|
| **1. Open Website** | Web UI loads with header, microphone, input bar, and pipeline explanation. |
| **2. FAQ Database** | 30+ comprehensive VNR VJIET FAQ records loaded and indexed on startup. |
| **3. Typed Question** | Submitting `"Where is VNR VJIET located?"` returns Bachupally, Hyderabad details. |
| **4. Known FAQ Variations** | `"What is the highest package?"` correctly returns ₹48-54 LPA placement details. |
| **5. Voice Input** | Clicking 🎤 turns red (`🔴 Listening...`), captures speech, and populates input. |
| **6. Answer Display** | Question and Assistant answers appear in conversation stream with copy and audio controls. |
| **7. Listen / Stop Button** | Clicking 🔊 reads answer aloud; clicking ⏹ immediately halts speech synthesis. |
| **8. Unknown Query Handling** | Asking `"How to bake a pizza?"` safely returns: *"I'm sorry, I couldn't find that information in the VNR VJIET FAQ database."* |
| **9. Clear Chat** | Clicking "Clear Chat" resets history and displays empty state. |
| **10. Mobile Responsiveness** | UI flexes cleanly on mobile, tablet, and desktop viewports. |

---

## ❓ Troubleshooting

- **Microphone Access Denied**:
  Ensure your browser has granted microphone permissions for `http://127.0.0.1:5000` or `localhost`.
- **Browser Compatibility**:
  Use Google Chrome, Microsoft Edge, or Safari for the best Web Speech API experience.
- **Port In Use**:
  If port `5000` is already in use, change `PORT=5001` in your `.env` file.
- **No OpenAI Key**:
  The application automatically falls back to direct verified database answers without throwing errors.

---

## 📜 License & Acknowledgments

Developed for **VNR Vignana Jyothi Institute of Engineering and Technology (VNR VJIET)**.
