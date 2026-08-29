# VNR VJIET Voice FAQ Assistant

An intelligent **voice-enabled FAQ web application** developed for **VNR Vignana Jyothi Institute of Engineering and Technology (VNR VJIET), Hyderabad**.

The application allows students, parents, and visitors to ask questions about VNR VJIET using **voice or text**. Questions are processed through a hybrid FAQ retrieval engine using **TF-IDF, Cosine Similarity, keyword overlap, fuzzy matching, and synonym expansion**. Relevant verified information is retrieved from a structured college FAQ database, and the application can generate grounded responses using an OpenAI LLM.

---

## 📌 Project Overview

The main goal of this project is to provide a simple and accessible way for users to obtain information about VNR VJIET without manually searching through multiple college resources.

The assistant supports:

* 🎤 Voice-based questions
* ⌨️ Text-based questions
* 🔍 Intelligent FAQ retrieval
* 🧠 Grounded AI responses
* 🔊 Voice-based answers
* 💬 Conversation history
* 📱 Responsive web interface

The knowledge base currently contains **147 verified FAQ records** covering major areas of the institution.

---

## ✨ Features

### 🎤 Voice Input

Users can speak their questions through the browser microphone. The browser's Web Speech API converts speech into text.

### ⌨️ Text Input

Users can also type their questions directly into the application.

### 📚 VNR VJIET Knowledge Base

The application uses:

```text
data/VNRVJIET_COMPLETE_DATABASE.csv
```

The database contains **147 FAQ records** covering categories such as:

* College information
* Academics
* Admissions
* B.Tech Programs
* PG Programs
* Campus
* Hostel
* Library
* Placements
* Student Services & Contacts
* General Navigation

### 🔍 Hybrid FAQ Search

The search engine combines multiple techniques:

1. TF-IDF Vectorization
2. Cosine Similarity
3. Keyword Overlap
4. Fuzzy String Matching
5. Query Synonym Expansion
6. Weighted relevance scoring
7. Similarity threshold filtering

This combination improves retrieval when users phrase the same question in different ways.

### 🧠 Grounded AI Responses

The application can use an OpenAI LLM to generate responses based on the retrieved FAQ information.

The system is designed to keep responses grounded in the retrieved knowledge base.

### 🛡️ Unknown Question Handling

When a question does not meet the required relevance threshold, the system can safely return:

> I'm sorry, I couldn't find that information in the VNR VJIET FAQ database.

### 🔊 Voice Output

The application uses browser speech synthesis to read the assistant's response aloud.

### 💬 Conversation History

Users can view their current questions and assistant responses in the conversation interface.

### 🗑️ Clear Chat

Users can clear the current conversation and start a new interaction.

### 📱 Responsive Interface

The frontend is designed to work across desktop, tablet, and mobile screen sizes.

---

## 🏗️ Project Structure

The project follows the required fixed structure:

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

> **Security note:** `.env` is used only for local configuration and is excluded from Git using `.gitignore`. The repository contains `.env.example` instead.

---

## 🛠️ Technology Stack

| Layer                 | Technology       | Purpose                                |
| --------------------- | ---------------- | -------------------------------------- |
| Frontend              | HTML5            | Web page structure                     |
| Styling               | CSS3             | Responsive user interface              |
| Client-side Logic     | JavaScript ES6+  | User interaction and API communication |
| Backend               | Python 3         | Application logic                      |
| Web Framework         | Flask            | Backend server and REST API            |
| Database              | CSV              | VNR VJIET FAQ knowledge base           |
| Data Processing       | Pandas           | Reading and processing FAQ data        |
| Information Retrieval | Scikit-learn     | TF-IDF and Cosine Similarity           |
| Fuzzy Matching        | Python `difflib` | Approximate question matching          |
| AI                    | OpenAI API       | Grounded response generation           |
| Speech Recognition    | Web Speech API   | Voice-to-text                          |
| Speech Synthesis      | Web Speech API   | Text-to-voice                          |

---

## 🔄 System Workflow

```text
                    USER
                     │
              ┌──────┴──────┐
              │             │
           🎤 Voice       ⌨️ Text
              │             │
              ▼             │
       Speech Recognition   │
              │             │
              └──────┬──────┘
                     ▼
              Question Text
                     │
                     ▼
              Flask Backend
                     │
                     ▼
             FAQ Search Engine
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      TF-IDF      Keywords      Fuzzy
        │            │            │
        └────────────┼────────────┘
                     ▼
              Relevance Score
                     │
                     ▼
             Relevant FAQ Data
                     │
                     ▼
             Grounded LLM Layer
                     │
                     ▼
              Final Answer
                     │
              ┌──────┴──────┐
              ▼             ▼
        Display Answer    🔊 Speech
```

---

## 🔎 FAQ Search Method

The FAQ search engine calculates a combined relevance score using:

```text
Combined Score =
    50% × Cosine Similarity
  + 30% × Keyword Overlap
  + 20% × Fuzzy Matching
```

The system also expands selected query words using predefined synonyms before performing TF-IDF retrieval.

For example:

```text
User Query:
"Where is the college?"

Expanded Query:
"where location address place area reach college"
```

This helps the system recognize different ways of asking similar questions.

---

## 📊 Knowledge Base

The current database contains:

```text
Total FAQ Records: 147
Empty Questions:   0
Empty Answers:     0
Duplicate Questions: 0
Categories:        11
```

### Categories

```text
Academics
Admissions
B.Tech Programs
Campus
College
General Navigation
Hostel
Library
PG Programs
Placements
Student Services & Contacts
```

---

## 🚀 Installation and Setup

### 1. Clone the Repository

```powershell
git clone https://github.com/tadurisrija45/VNRVJIET-Voice-FAQ-Bot.git
cd VNRVJIET-Voice-FAQ-Bot
```

### 2. Create a Virtual Environment

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create the local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Then configure the required values in `.env`.

Example:

```env
OPENAI_API_KEY=your_actual_openai_api_key_here
PORT=5000
DEBUG=True
```

> Never upload your actual `.env` file or API key to GitHub.

---

## ▶️ Run the Application

Start the Flask application:

```powershell
python app.py
```

The application will run at:

```text
http://127.0.0.1:5000
```

Open the address in Google Chrome or another supported browser.

---

## 🧪 Testing

The following scenarios can be used to test the application.

| Test                                  | Expected Result                      |
| ------------------------------------- | ------------------------------------ |
| Open application                      | Homepage loads successfully          |
| Type a known FAQ                      | Relevant answer is displayed         |
| Ask using voice                       | Speech is converted into text        |
| Submit recognized question            | Backend returns an answer            |
| Ask a question with different wording | Hybrid search finds the relevant FAQ |
| Ask an unrelated question             | Safe unknown-question response       |
| Click Listen                          | Answer is spoken aloud               |
| Click Stop                            | Speech stops                         |
| Clear conversation                    | Chat history is cleared              |
| Resize browser                        | Responsive interface remains usable  |

### Example Questions

```text
What is the full name of VNRVJIET?

When was VNRVJIET established?

Is VNRVJIET autonomous?

Which university is VNRVJIET affiliated to?

What is the campus address?

What courses are offered?

What hostel facilities are available?

What library facilities are available?

What are the placement facilities?
```

---

## 🔐 Security

The project uses environment variables for sensitive configuration.

The following file is intentionally excluded from Git:

```text
.env
```

The repository contains:

```text
.env.example
```

as a safe template.

Never commit API keys, passwords, or other secrets to the repository.

---

## 🛠️ Troubleshooting

### Microphone Does Not Work

Allow microphone permission for:

```text
http://127.0.0.1:5000
```

Google Chrome or Microsoft Edge is recommended for browser speech recognition.

### Port 5000 Already in Use

Change the port value in `.env`:

```env
PORT=5001
```

Then restart the application.

### OpenAI API Key Not Available

If the application is configured to use direct verified FAQ retrieval when the LLM is unavailable, it can continue using the knowledge base.

---

## 🎯 Project Objectives

The project aims to:

1. Provide quick access to VNR VJIET information.
2. Support both voice and text interaction.
3. Improve FAQ retrieval using hybrid information-retrieval techniques.
4. Reduce the need for manual searching.
5. Provide grounded AI-assisted responses.
6. Demonstrate practical integration of AI, NLP, speech technologies, and web development.

---

## 🔮 Future Enhancements

Possible future improvements include:

* Multilingual voice support
* Telugu language support
* More frequently updated institutional data
* Admin interface for FAQ management
* Analytics dashboard
* User feedback and answer-rating system
* Retrieval-Augmented Generation (RAG)
* Cloud deployment
* Mobile application

---

## 📜 License and Acknowledgment

Developed as an academic/internship project for **VNR Vignana Jyothi Institute of Engineering and Technology (VNR VJIET)**.

The project demonstrates the practical integration of:

```text
Python + Flask
HTML + CSS + JavaScript
NLP / Information Retrieval
OpenAI LLM
Speech Recognition
Speech Synthesis
Structured Knowledge Base
```

---

## 👩‍💻 Developer

**Thaduru Srija**

VNR Vignana Jyothi Institute of Engineering and Technology

B.Tech – Computer Science and Engineering (Data Science)
