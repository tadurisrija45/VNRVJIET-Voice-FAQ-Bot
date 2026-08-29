# VNR VJIET Voice FAQ Assistant

A voice-in, voice-out FAQ assistant for answering common questions about **VNR Vignana Jyothi Institute of Engineering and Technology (VNR VJIET), Hyderabad**.

This project is developed as part of the **LLMs Meet Speech – Take-Home Assessment, Project 2: Voice FAQ Bot**.

---

## 1. Project Overview

The **VNR VJIET Voice FAQ Assistant** allows students, parents, and visitors to ask questions about VNR VJIET using either **voice or text**.

The system:

- Records a spoken question from the user
- Converts speech into text
- Searches a structured VNR VJIET FAQ knowledge base
- Uses an LLM to generate a grounded answer
- Displays the answer to the user
- Converts the answer back into speech
- Maintains the current conversation history

The project focuses on building a working **end-to-end speech + LLM pipeline** rather than only a UI demonstration.

---

## 2. Assessment Track

**Selected Track:** Project 2 – Voice FAQ Bot

### Assessment Requirement

Build a voice-in, voice-out assistant that answers common questions from a small knowledge base.

### Project Implementation

This project uses VNR VJIET institutional FAQs as the knowledge base.

The user can:

**Speak → Transcribe → Retrieve FAQ → Generate Answer → Speak Answer**

Text input is also supported as an alternative to voice input.

---

## 3. Core Features

### 🎤 Voice Input

The user can ask a question using the browser microphone.

The browser's Web Speech API captures the user's speech and converts it into text.

### ⌨️ Text Input

Users can type their question manually when they do not want to use the microphone.

### 🔍 FAQ Retrieval

The application searches the VNR VJIET FAQ knowledge base to find the most relevant information.

The retrieval system combines:

- TF-IDF
- Cosine Similarity
- Keyword Overlap
- Fuzzy Matching
- Synonym Expansion
- Weighted Relevance Scoring

### 🧠 LLM Answer Generation

After retrieving relevant FAQ information, the application can use an OpenAI LLM to generate a natural-language answer grounded in the retrieved information.

The LLM is not intended to answer from unrelated knowledge when the required information is not available in the FAQ database.

### 🔊 Voice Output

The generated answer can be spoken back to the user using browser text-to-speech.

### 💬 Conversation History

The interface keeps the current questions and answers visible during the session.

### 🗑️ Clear Chat

Users can clear the current conversation and start a new interaction.

### 🛡️ Unknown Question Handling

If the system cannot find sufficiently relevant information, it returns a safe response instead of generating an unsupported answer.

Example:

> I'm sorry, I couldn't find that information in the VNR VJIET FAQ database.

### 📱 Responsive Interface

The application is designed to work on desktop, tablet, and mobile screen sizes.

---

## 4. End-to-End System Workflow

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
5. Speech Handling

The application supports a complete voice interaction flow.

Voice Input Flow
User speaks
     ↓
Browser microphone
     ↓
Speech recognition
     ↓
Transcribed text
     ↓
FAQ retrieval
     ↓
LLM response
     ↓
Text answer
     ↓
Speech synthesis
     ↓
User hears answer

The application also provides text input so that the FAQ and LLM pipeline can be tested independently of microphone availability.

6. Knowledge Base

The project uses a structured FAQ database:

data/VNRVJIET_COMPLETE_DATABASE.csv

The knowledge base currently contains:

Total FAQ Records: 147
Empty Questions:   0
Empty Answers:     0
Duplicate Questions: 0
Categories:        11
FAQ Categories
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

The knowledge base is used as the source of information for answering VNR VJIET-related questions.

7. Retrieval Approach

The FAQ retrieval engine uses a hybrid approach instead of depending on a single similarity method.

Combined Relevance Score
Combined Score =
    50% × Cosine Similarity
  + 30% × Keyword Overlap
  + 20% × Fuzzy Matching

The system also uses predefined synonym expansion.

For example:

User Query:
Where is the college?

Expanded Query:
where location address place area reach college

This helps the system recognize different ways of asking similar questions.

8. LLM Usage

The LLM is used after FAQ retrieval.

The general pipeline is:

User Question
      ↓
FAQ Retrieval
      ↓
Relevant FAQ Information
      ↓
LLM Prompt
      ↓
Grounded Answer

The retrieved FAQ information provides context for the LLM.

This approach reduces the possibility of the LLM providing unrelated information about the institution.

Unknown Information

If no FAQ has sufficient relevance, the system can avoid unnecessary LLM generation and return an unknown-information response.

9. Thoughtful LLM Use

The LLM is not used simply as an independent chatbot.

It is integrated into the retrieval pipeline.

The application first identifies relevant institutional information and then provides that information to the LLM for answer generation.

This provides:

Better grounding
More relevant answers
Reduced hallucination risk
Consistent answers based on the FAQ database

The application also handles cases where the LLM API is unavailable by allowing verified FAQ retrieval to continue.

10. Speech-Handling Quality

The project supports:

Microphone input
Speech-to-text conversion
Text-based fallback
Answer generation
Text-to-speech output
Start/stop speech controls
Unknown-question handling

Browser speech recognition is used for the prototype.

Google Chrome or Microsoft Edge is recommended for speech recognition support.

11. Code Quality and Structure

The project separates different responsibilities into individual modules.

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
Module Responsibilities

app.py

Handles the Flask application, routes, requests, and responses.

services/speech_to_text.py

Handles speech-to-text related functionality.

services/faq_search.py

Handles FAQ preprocessing, retrieval, similarity calculation, and relevance scoring.

services/llm.py

Handles communication with the LLM and grounded response generation.

services/text_to_speech.py

Handles text-to-speech functionality.

utils/helpers.py

Contains reusable helper functions.

data/VNRVJIET_COMPLETE_DATABASE.csv

Contains the structured VNR VJIET FAQ knowledge base.

12. Technology Stack
Technology	Purpose
HTML5	Web page structure
CSS3	Responsive interface
JavaScript ES6+	Frontend interaction
Python 3	Backend logic
Flask	Web framework and API
Pandas	FAQ data processing
Scikit-learn	TF-IDF and cosine similarity
Python difflib	Fuzzy matching
OpenAI API	LLM response generation
Web Speech API	Speech recognition
Web Speech API	Text-to-speech
CSV	FAQ knowledge base
13. Installation
Step 1: Clone the Repository
git clone https://github.com/tadurisrija45/VNRVJIET-Voice-FAQ-Bot.git
cd VNRVJIET-Voice-FAQ-Bot
Step 2: Create Virtual Environment
python -m venv venv
Step 3: Activate Virtual Environment

Windows:

venv\Scripts\activate
Step 4: Install Dependencies
pip install -r requirements.txt
14. Environment Configuration

Create a .env file using .env.example.

Example:

OPENAI_API_KEY=your_actual_openai_api_key_here
PORT=5000
DEBUG=True

Do not commit the actual .env file or API key to GitHub.

The repository should contain .env.example instead.

15. Running the Application

Start the Flask application:

python app.py

The application will normally be available at:

http://127.0.0.1:5000

Open the address in Google Chrome or Microsoft Edge.

Allow microphone permission when using voice input.

16. Testing

The complete pipeline can be tested using the following scenarios.

Test	Expected Result
Open application	Homepage loads
Type a known FAQ	Relevant answer is displayed
Ask using voice	Speech is converted to text
Submit recognized question	Backend returns an answer
Use different wording	Hybrid retrieval finds relevant FAQ
Ask unrelated question	Safe unknown response
Click Listen	Answer is spoken
Click Stop	Speech stops
Clear conversation	Chat history is cleared
Resize browser	Responsive interface remains usable
17. Example Questions
What is the full name of VNR VJIET?

When was VNR VJIET established?

Is VNR VJIET autonomous?

Which university is VNR VJIET affiliated to?

What is the campus address?

What courses are offered?

What B.Tech programs are available?

What PG programs are available?

What hostel facilities are available?

What library facilities are available?

What are the placement facilities?

Where is the college located?

How can I contact the college?

What student services are available?
18. Error and Edge-Case Handling

The application considers common failure cases.

Unknown Question

If the question does not match the knowledge base sufficiently:

I'm sorry, I couldn't find that information in the VNR VJIET FAQ database.
Microphone Permission

If microphone access is denied, the user can use text input instead.

Unclear Speech

If the speech recognition result is empty or unclear, the user can retry or type the question manually.

LLM API Unavailable

If the LLM service is unavailable, the application can continue using verified FAQ retrieval where configured.

Port Conflict

If port 5000 is already being used, change the port:

PORT=5001
19. Security

Sensitive configuration is stored using environment variables.

The actual API key is not included in the source code.

The following file is excluded from Git:

.env

The repository contains:

.env.example

as a safe configuration template.

Never commit:

API keys
Passwords
Private credentials
Other secrets
20. Design Decisions and Trade-offs
Why a Hybrid FAQ Search?

A single similarity technique may fail when users phrase questions differently.

Combining:

Semantic similarity
Keyword matching
Fuzzy matching
Synonym expansion

provides more robust retrieval for a small FAQ dataset.

Why Use a Structured FAQ Database?

The application is designed for institutional information where accuracy is important.

Using a structured FAQ database makes the information easier to verify and update.

Why Browser Speech APIs?

Browser speech APIs allow the prototype to provide voice interaction without requiring a separate speech server.

This keeps the prototype simple and easy to run.

Why Keep Text Input?

Text input provides a fallback when:

Microphone permission is unavailable
Speech recognition is inaccurate
The user is in a noisy environment
The browser does not support the required speech feature
21. Known Limitations

The current prototype has some limitations:

Browser speech recognition depends on browser support.
Recognition quality may decrease with noisy audio.
The FAQ database requires manual updates when institutional information changes.
The current prototype primarily targets English questions.
LLM availability depends on API configuration and network access.
The system is designed around a relatively small institutional FAQ dataset.
22. Stretch Goals

The assessment suggests extending a basic FAQ bot with retrieval over a real FAQ document.

This project already implements a structured retrieval layer over the VNR VJIET FAQ dataset.

Possible future improvements include:

Retrieval-Augmented Generation (RAG)
Vector database integration
Multilingual voice support
Telugu language support
Admin FAQ management
Automatic knowledge-base updates
User feedback and answer ratings
Analytics dashboard
Cloud deployment
Mobile application
23. Creativity / Additional Features

Beyond the basic voice FAQ requirement, the project includes:

Hybrid FAQ retrieval
Synonym expansion
Fuzzy matching
Relevance threshold filtering
Grounded LLM responses
Text-input fallback
Conversation history
Clear-chat functionality
Voice answer playback
Responsive web interface
Safe handling of unknown questions

These additions improve the usability and reliability of the basic Voice FAQ Bot concept.

24. Ground Rules / Development Approach

This project was developed as an individual prototype.

The implementation uses publicly available libraries, APIs, and technical documentation.

AI coding assistance was used during development for implementation support, debugging, and documentation.

The final project structure, integration, testing, and configuration were reviewed for this application.

Development was approached incrementally:

1. Create FAQ knowledge base
2. Build FAQ retrieval
3. Add Flask backend
4. Add text interaction
5. Add voice input
6. Add LLM response generation
7. Add voice output
8. Add error handling
9. Test the complete pipeline
10. Document the project
25. End-to-End Demonstration

The final prototype demonstrates the complete pipeline:

🎤 User Voice
      ↓
📝 Speech-to-Text
      ↓
🔍 FAQ Retrieval
      ↓
📚 Relevant Knowledge
      ↓
🧠 LLM
      ↓
💬 Grounded Answer
      ↓
🔊 Text-to-Speech
      ↓
👤 User

The main objective is to demonstrate that speech input can be connected to knowledge retrieval, an LLM, and speech output in one working application.

26. Project Objectives

The project aims to:

Build a working voice-in, voice-out assistant.
Answer common VNR VJIET questions.
Connect speech processing with an LLM.
Use a real institutional FAQ knowledge base.
Improve retrieval using hybrid search techniques.
Provide grounded responses.
Handle unknown questions safely.
Provide a simple and accessible interface.
Demonstrate an end-to-end AI application.
Maintain clear and modular project documentation.
27. Conclusion

The VNR VJIET Voice FAQ Assistant demonstrates an end-to-end implementation of a voice-enabled FAQ system.

Instead of treating the LLM as a standalone chatbot, the application combines:

Speech Recognition
        +
FAQ Retrieval
        +
Knowledge Base
        +
LLM
        +
Speech Synthesis

This creates a practical voice assistant for answering common VNR VJIET questions while keeping responses grounded in the project's knowledge base.

👩‍💻 Developer

Thaduru Srija

VNR Vignana Jyothi Institute of Engineering and Technology

B.Tech – Computer Science and Engineering (Data Science)