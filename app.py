"""
VNR VJIET Voice FAQ Assistant - Main Flask Application
Serves web interface and handles the /api/ask voice/text question pipeline.
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment configuration
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Import services and utilities
from utils.helpers import (
    clean_text,
    validate_question,
    format_success_response,
    format_error_response
)
from services.speech_to_text import process_speech_transcript
from services.faq_search import search_faq, get_best_faq_match
from services.llm import generate_answer
from services.text_to_speech import prepare_text_for_speech

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'vnrvjiet-secret-key-2026')
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def home():
    """
    Render the main VNR VJIET Voice FAQ Assistant user interface.
    """
    return render_template('index.html')


@app.route('/api/ask', methods=['POST'])
def api_ask():
    """
    Process voice or typed student questions.
    Pipeline: Input Validation -> STT Text Normalization -> FAQ Hybrid Search -> LLM Grounding -> TTS Prep
    """
    try:
        if not request.is_json:
            response_data, status_code = format_error_response(
                "Invalid request. Content-Type must be application/json.",
                400
            )
            return jsonify(response_data), status_code

        data = request.get_json() or {}
        raw_question = data.get('question', '')

        # 1. Validate user input
        is_valid, error_msg = validate_question(raw_question)
        if not is_valid:
            response_data, status_code = format_error_response(error_msg, 400)
            return jsonify(response_data), status_code

        # 2. Clean and normalize question text
        normalized_question = clean_text(raw_question)
        phonetic_corrected_question = process_speech_transcript(normalized_question)

        # 3. Retrieve relevant knowledge from CSV database
        retrieved_faqs = search_faq(phonetic_corrected_question, top_k=3, threshold=0.20)
        
        # 4. Generate answer through LLM or grounded database fallback
        llm_result = generate_answer(phonetic_corrected_question, retrieved_faqs)
        answer_text = llm_result.get('answer', "I'm sorry, I couldn't find that information in the VNR VJIET FAQ database.")
        source_info = llm_result.get('source', "VNR VJIET Knowledge Base")

        # Determine primary category and confidence
        primary_category = retrieved_faqs[0].get('category', 'General') if retrieved_faqs else 'General'
        top_score = retrieved_faqs[0].get('score', 0.0) if retrieved_faqs else 0.0

        # 5. Prepare phonetic text-to-speech output
        speech_text = prepare_text_for_speech(answer_text)

        # 6. Return standardized JSON response
        success_response = format_success_response(
            question=normalized_question,
            answer=answer_text,
            source=source_info,
            category=primary_category,
            confidence=top_score,
            speech_text=speech_text
        )
        return jsonify(success_response), 200

    except Exception as e:
        logger.error(f"Unexpected error in /api/ask: {e}", exc_info=False)
        response_data, status_code = format_error_response(
            "The AI service is temporarily unavailable. Please try again.",
            500
        )
        return jsonify(response_data), status_code


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check and system info endpoint.
    """
    return jsonify({
        "status": "healthy",
        "service": "VNR VJIET Voice FAQ Assistant",
        "version": "1.0.0"
    }), 200


# Safe HTTP Error Handlers
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"success": False, "error": "Bad request format."}), 400


@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "Resource not found."}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"success": False, "error": "HTTP method not allowed."}), 405


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"success": False, "error": "Internal server error. Please try again."}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() in ['true', '1', 't']
    logger.info(f"Starting VNR VJIET Voice FAQ Assistant on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
