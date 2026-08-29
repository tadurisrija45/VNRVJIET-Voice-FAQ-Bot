/**
 * VNR VJIET Voice FAQ Assistant - Frontend Application Logic
 * Integrates Web Speech API (STT), Speech Synthesis (TTS),
 * asynchronous API requests to /api/ask, and conversation history.
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const recordButton = document.getElementById('recordButton');
    const micIcon = document.getElementById('micIcon');
    const recordStatus = document.getElementById('recordStatus');
    const statusInstruction = document.getElementById('statusInstruction');
    const liveTranscript = document.getElementById('liveTranscript');
    const questionForm = document.getElementById('questionForm');
    const questionInput = document.getElementById('questionInput');
    const askButton = document.getElementById('askButton');
    const chatStream = document.getElementById('chatStream');
    const emptyState = document.getElementById('emptyState');
    const clearChatButton = document.getElementById('clearChatButton');
    const toastContainer = document.getElementById('toastContainer');
    const faqChips = document.querySelectorAll('.faq-chip');

    // Pipeline Step Elements
    const stepSpeech = document.getElementById('stepSpeech');
    const stepSTT = document.getElementById('stepSTT');
    const stepLLM = document.getElementById('stepLLM');
    const stepTTS = document.getElementById('stepTTS');

    // State Variables
    let isListening = false;
    let recognition = null;
    let currentSpeechUtterance = null;
    let activeSpeakButton = null;
    let availableVoices = [];

    // Initialize Speech Recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const isSpeechRecognitionSupported = !!SpeechRecognition;

    if (isSpeechRecognitionSupported) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'en-IN'; // Indian English for accurate regional pronunciations

        recognition.onstart = () => {
            isListening = true;
            recordButton.classList.add('listening');
            micIcon.textContent = '🔴';
            recordStatus.textContent = 'Listening... Speak now';
            recordStatus.className = 'status-badge listening';
            statusInstruction.textContent = 'Speak your question clearly into your microphone';
            liveTranscript.hidden = false;
            liveTranscript.textContent = 'Listening...';
            setPipelineActive(stepSpeech, stepSTT);
        };

        recognition.onresult = (event) => {
            let interim = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interim += event.results[i][0].transcript;
                }
            }

            const currentText = finalTranscript || interim;
            if (currentText) {
                liveTranscript.textContent = `"${currentText}"`;
                questionInput.value = currentText;
            }

            if (finalTranscript.trim().length > 0) {
                stopSpeechRecognition();
                processUserQuestion(finalTranscript.trim(), true);
            }
        };

        recognition.onerror = (event) => {
            console.warn('Speech recognition error:', event.error);
            stopSpeechRecognition();

            if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
                showToast('Microphone access was denied. Please allow microphone access or type your question.', 'error');
                recordStatus.textContent = 'Microphone permission denied';
            } else if (event.error === 'no-speech') {
                showToast('No speech was detected. Please try speaking again.', 'error');
                recordStatus.textContent = 'No speech detected';
            } else {
                showToast(`Voice input error: ${event.error}. Please type your question.`, 'error');
                recordStatus.textContent = 'Ready to listen';
            }
        };

        recognition.onend = () => {
            if (isListening) {
                stopSpeechRecognition();
            }
        };
    } else {
        console.warn('Web Speech API is not supported in this browser.');
    }

    // Initialize Speech Synthesis Voices
    if ('speechSynthesis' in window) {
        const loadVoices = () => {
            availableVoices = window.speechSynthesis.getVoices();
        };
        loadVoices();
        if (speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = loadVoices;
        }
    }

    // Toggle Microphone Recording
    function toggleSpeechRecognition() {
        if (!isSpeechRecognitionSupported) {
            showToast('Voice input is not supported in this browser. Please type your question.', 'error');
            return;
        }

        // Stop any active speech synthesis before recording
        stopSpeechSynthesis();

        if (isListening) {
            stopSpeechRecognition();
        } else {
            try {
                recognition.start();
            } catch (err) {
                console.error('Failed to start recognition:', err);
                stopSpeechRecognition();
            }
        }
    }

    function stopSpeechRecognition() {
        isListening = false;
        if (recognition) {
            try {
                recognition.stop();
            } catch (e) {
                // Ignore if already stopped
            }
        }
        recordButton.classList.remove('listening');
        micIcon.textContent = '🎤';
        recordStatus.textContent = 'Ready to listen';
        recordStatus.className = 'status-badge';
        statusInstruction.textContent = 'Click the microphone and speak your question';
        resetPipeline();
    }

    // Main Question Processing Pipeline
    async function processUserQuestion(questionText, autoSpeak = false) {
        if (!questionText || questionText.trim().length === 0) {
            showToast('Please enter or speak a question.', 'error');
            return;
        }

        const cleanedQuestion = questionText.trim();

        // UI Updates for Processing State
        questionInput.value = '';
        askButton.disabled = true;
        recordStatus.textContent = 'Processing question...';
        recordStatus.className = 'status-badge processing';
        statusInstruction.textContent = 'Searching VNR VJIET Knowledge Base...';
        setPipelineActive(stepLLM);

        try {
            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: cleanedQuestion })
            });

            const data = await response.json();

            if (data.success) {
                appendChatMessage(data.question, data.answer, data.category, data.source, autoSpeak);
                recordStatus.textContent = 'Ready to listen';
                recordStatus.className = 'status-badge';
                statusInstruction.textContent = 'Click the microphone and speak your question';
                liveTranscript.hidden = true;
            } else {
                showToast(data.error || 'Unable to process the question.', 'error');
                recordStatus.textContent = 'Error processing question';
                recordStatus.className = 'status-badge';
            }
        } catch (error) {
            console.error('API Error:', error);
            showToast('The AI service is temporarily unavailable. Please try again.', 'error');
            recordStatus.textContent = 'Connection error';
            recordStatus.className = 'status-badge';
        } finally {
            askButton.disabled = false;
            resetPipeline();
        }
    }

    // Append Message to Conversation Stream
    function appendChatMessage(question, answer, category, source, autoSpeak) {
        if (emptyState) {
            emptyState.style.display = 'none';
        }

        const chatPair = document.createElement('div');
        chatPair.className = 'chat-pair';

        const categoryTag = category ? `<span class="assistant-category-badge">${escapeHtml(category)}</span>` : '';

        chatPair.innerHTML = `
            <!-- User Question Bubble -->
            <div class="user-message-card">
                <div class="user-meta">You</div>
                <div class="user-text">${escapeHtml(question)}</div>
            </div>

            <!-- Assistant Answer Bubble -->
            <div class="assistant-message-card">
                <div class="assistant-header">
                    <div class="assistant-identity">
                        <img src="/static/images/vnrvjiet-logo.png" alt="VNR VJIET Assistant" class="assistant-avatar">
                        <span class="assistant-name">VNR VJIET Assistant</span>
                    </div>
                    ${categoryTag}
                </div>
                <div class="assistant-body">
                    <p class="assistant-text">${escapeHtml(answer)}</p>
                </div>
                <div class="assistant-actions">
                    <button type="button" class="btn-action btn-listen" title="Listen to answer">
                        <span class="btn-icon">🔊</span>
                        <span class="btn-text">Listen</span>
                    </button>
                    <button type="button" class="btn-action btn-stop" title="Stop listening" style="display: none;">
                        <span class="btn-icon">⏹</span>
                        <span class="btn-text">Stop</span>
                    </button>
                    <button type="button" class="btn-action btn-copy" title="Copy answer">
                        <span class="btn-icon">📋</span>
                        <span class="btn-text">Copy</span>
                    </button>
                </div>
            </div>
        `;

        chatStream.appendChild(chatPair);

        // Attach Button Listeners
        const btnListen = chatPair.querySelector('.btn-listen');
        const btnStop = chatPair.querySelector('.btn-stop');
        const btnCopy = chatPair.querySelector('.btn-copy');

        btnListen.addEventListener('click', () => {
            speakText(answer, btnListen, btnStop);
        });

        btnStop.addEventListener('click', () => {
            stopSpeechSynthesis();
        });

        btnCopy.addEventListener('click', () => {
            copyToClipboard(answer, btnCopy);
        });

        // Scroll to the newest message
        chatPair.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        // If voice-initiated, automatically speak the answer
        if (autoSpeak) {
            speakText(answer, btnListen, btnStop);
        }
    }

    // Text-to-Speech (TTS) Functionality
    function speakText(text, listenBtn, stopBtn) {
        if (!('speechSynthesis' in window)) {
            showToast('Text-to-speech is not supported in this browser.', 'error');
            return;
        }

        stopSpeechSynthesis();

        // Clean text for speech
        const speechContent = sanitizeForSpeech(text);
        if (!speechContent) return;

        currentSpeechUtterance = new SpeechSynthesisUtterance(speechContent);
        currentSpeechUtterance.rate = 1.0;
        currentSpeechUtterance.pitch = 1.0;
        currentSpeechUtterance.lang = 'en-IN';

        // Select suitable voice (English Indian, or natural English)
        if (availableVoices.length > 0) {
            const voice = availableVoices.find(v => v.lang === 'en-IN' || v.lang === 'en_IN') ||
                          availableVoices.find(v => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('India'))) ||
                          availableVoices.find(v => v.lang.startsWith('en'));
            if (voice) {
                currentSpeechUtterance.voice = voice;
            }
        }

        activeSpeakButton = { listenBtn, stopBtn };

        currentSpeechUtterance.onstart = () => {
            if (listenBtn && stopBtn) {
                listenBtn.style.display = 'none';
                stopBtn.style.display = 'inline-flex';
            }
            setPipelineActive(stepTTS);
        };

        currentSpeechUtterance.onend = () => {
            resetSpeakButtons();
            resetPipeline();
        };

        currentSpeechUtterance.onerror = (e) => {
            console.warn('Speech synthesis error:', e);
            resetSpeakButtons();
            resetPipeline();
        };

        window.speechSynthesis.speak(currentSpeechUtterance);
    }

    function stopSpeechSynthesis() {
        if ('speechSynthesis' in window && window.speechSynthesis.speaking) {
            window.speechSynthesis.cancel();
        }
        resetSpeakButtons();
        resetPipeline();
    }

    function resetSpeakButtons() {
        if (activeSpeakButton) {
            const { listenBtn, stopBtn } = activeSpeakButton;
            if (listenBtn) listenBtn.style.display = 'inline-flex';
            if (stopBtn) stopBtn.style.display = 'none';
            activeSpeakButton = null;
        }
    }

    // Helper to sanitize text for natural speech synthesis
    function sanitizeForSpeech(text) {
        if (!text) return '';
        return text
            .replace(/https?:\/\/\S+/g, '')
            .replace(/[*_~`#<>\[\]]/g, '')
            .replace(/₹/g, 'rupees ')
            .replace(/\bVNR VJIET\b/gi, 'V N R V J I E T')
            .replace(/\bVNRVJIET\b/gi, 'V N R V J I E T')
            .replace(/\bJNTUH\b/gi, 'J N T U Hyderabad')
            .replace(/\bLPA\b/gi, 'Lakhs per annum')
            .replace(/\bINR\b/gi, 'rupees')
            .replace(/\bAI\s*&\s*ML\b/gi, 'A I and M L')
            .replace(/\bNAAC A\+\+\b/gi, 'NAAC A plus plus')
            .replace(/\bJPMC\b/gi, 'J P Morgan Chase')
            .trim();
    }

    // Copy to Clipboard Helper
    async function copyToClipboard(text, btn) {
        try {
            await navigator.clipboard.writeText(text);
            const originalHtml = btn.innerHTML;
            btn.innerHTML = '<span class="btn-icon">✓</span><span class="btn-text">Copied!</span>';
            setTimeout(() => {
                btn.innerHTML = originalHtml;
            }, 1800);
            showToast('Answer copied to clipboard!', 'success');
        } catch (err) {
            showToast('Failed to copy to clipboard', 'error');
        }
    }

    // Pipeline Step Highlighting
    function setPipelineActive(...activeSteps) {
        [stepSpeech, stepSTT, stepLLM, stepTTS].forEach(s => {
            if (s) s.classList.remove('active');
        });
        activeSteps.forEach(s => {
            if (s) s.classList.add('active');
        });
    }

    function resetPipeline() {
        [stepSpeech, stepSTT, stepLLM, stepTTS].forEach(s => {
            if (s) s.classList.remove('active');
        });
    }

    // Toast Notifications
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(10px)';
            setTimeout(() => {
                if (toast.parentNode) {
                    toastContainer.removeChild(toast);
                }
            }, 300);
        }, 3500);
    }

    // Escape HTML to prevent XSS
    function escapeHtml(str) {
        if (!str) return '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // Event Listeners
    recordButton.addEventListener('click', toggleSpeechRecognition);

    questionForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = questionInput.value.trim();
        if (text) {
            processUserQuestion(text, false);
        } else {
            showToast('Please enter or speak a question.', 'error');
        }
    });

    faqChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const query = chip.getAttribute('data-query');
            if (query) {
                questionInput.value = query;
                processUserQuestion(query, false);
            }
        });
    });

    clearChatButton.addEventListener('click', () => {
        stopSpeechSynthesis();
        stopSpeechRecognition();
        chatStream.innerHTML = '';
        if (emptyState) {
            emptyState.style.display = 'block';
            chatStream.appendChild(emptyState);
        }
        showToast('Chat history cleared.', 'info');
    });

    // Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            stopSpeechSynthesis();
            stopSpeechRecognition();
        }
    });
});
