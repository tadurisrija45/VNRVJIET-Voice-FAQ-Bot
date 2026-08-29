"""
Text-to-Speech (TTS) service helpers for VNR VJIET Voice FAQ Bot.
"""

import re
from typing import Dict, Any


def prepare_text_for_speech(text: str) -> str:
    """
    Prepares raw answer text for high-quality, audible browser speech synthesis.
    Removes formatting, special characters, markdown, and converts
    abbreviations into natural-sounding phonetic text.
    """
    if not text or not isinstance(text, str):
        return ""
    
    spoken = text.strip()
    
    # Remove URLs
    spoken = re.sub(r'https?://\S+|www\.\S+', '', spoken)
    # Convert markdown links [text](url) -> text
    spoken = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', spoken)
    # Remove markdown symbols
    spoken = re.sub(r'[*_~`#<>\[\]]', '', spoken)
    
    # Phonetic replacements for natural speech
    replacements = [
        (r'₹', 'rupees '),
        (r'\bINR\b', 'rupees'),
        (r'\bRs\.?\b', 'rupees'),
        (r'\bLPA\b', 'Lakhs per annum'),
        (r'\bNAAC A\+\+\b', 'NAAC A plus plus'),
        (r'\bA\+\+\b', 'A plus plus'),
        (r'\bJNTUH\b', 'J N T U Hyderabad'),
        (r'\bVNR VJIET\b', 'V N R V J I E T'),
        (r'\bVNRVJIET\b', 'V N R V J I E T'),
        (r'\bCSE\b', 'C S E'),
        (r'\bECE\b', 'E C E'),
        (r'\bEEE\b', 'E E E'),
        (r'\bIT\b', 'I T'),
        (r'\bAI & ML\b', 'A I and M L'),
        (r'\bAI&ML\b', 'A I and M L'),
        (r'\bAI/ML\b', 'A I and M L'),
        (r'\bB\.Tech\b', 'B Tech'),
        (r'\bM\.Tech\b', 'M Tech'),
        (r'\bPh\.D\b', 'PhD'),
        (r'\bePASS\b', 'e-pass'),
        (r'\bJPMC\b', 'J P Morgan Chase'),
    ]
    
    for pat, repl in replacements:
        spoken = re.sub(pat, repl, spoken, flags=re.IGNORECASE)
    
    spoken = re.sub(r'\s+', ' ', spoken).strip()
    return spoken


def get_tts_config() -> Dict[str, Any]:
    """
    Return TTS optimization settings for the browser.
    """
    return {
        "provider": "Web Speech Synthesis API",
        "preferred_lang": "en-IN",
        "fallback_lang": "en-US",
        "rate": 1.0,
        "pitch": 1.0,
        "volume": 1.0
    }
