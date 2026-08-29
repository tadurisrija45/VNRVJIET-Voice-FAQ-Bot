"""
Helper functions and utilities for VNR VJIET Voice FAQ Bot.
Handles text cleaning, input validation, speech text sanitization,
and standardized API response formatting.
"""

import re
import html
from typing import Tuple, Dict, Any, Optional


def clean_text(text: str) -> str:
    """
    Normalize and clean user input text.
    """
    if not text or not isinstance(text, str):
        return ""
    text = html.unescape(text.strip())
    text = re.sub(r'\s+', ' ', text)
    return text


def validate_question(question: Any) -> Tuple[bool, str]:
    """
    Validate the user question.
    Returns (is_valid, error_message).
    """
    if question is None:
        return False, "Please enter or speak a question."
    
    if not isinstance(question, str):
        return False, "Invalid question format."
    
    cleaned = question.strip()
    if len(cleaned) == 0:
        return False, "Please enter or speak a question."
    
    if len(cleaned) < 2:
        return False, "Question is too short. Please provide more detail."
        
    if len(cleaned) > 1000:
        return False, "Question is too long (maximum 1000 characters)."
        
    return True, ""


def sanitize_for_speech(text: str) -> str:
    """
    Sanitize text for natural speech synthesis.
    """
    if not text:
        return ""
    
    # Remove URLs
    cleaned = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove markdown link formatting [text](url) -> text
    cleaned = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', cleaned)
    
    # Remove special markdown characters
    cleaned = re.sub(r'[*_~`#<>\[\]]', '', cleaned)
    
    # Normalize spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def format_success_response(
    question: str,
    answer: str,
    source: str = "VNR VJIET Knowledge Base",
    category: str = "General",
    confidence: float = 1.0,
    speech_text: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a standardized success JSON response structure.
    """
    if speech_text is None:
        speech_text = sanitize_for_speech(answer)
    return {
        "success": True,
        "question": question,
        "answer": answer,
        "speech_text": speech_text,
        "source": source,
        "category": category,
        "confidence": round(float(confidence), 3)
    }


def format_error_response(
    error_message: str = "Unable to process the question.",
    status_code: int = 400
) -> Tuple[Dict[str, Any], int]:
    """
    Create a standardized error JSON response structure.
    """
    return {
        "success": False,
        "error": error_message
    }, status_code
