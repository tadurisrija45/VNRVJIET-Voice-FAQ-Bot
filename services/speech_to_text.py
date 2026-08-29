
"""
Speech-to-Text (STT) service helpers for VNR VJIET Voice FAQ Bot.
"""

import re
from typing import Dict, Any, Tuple

PHONETIC_CORRECTIONS = {
    r'\b(v n r|vnr|vn\vr|b)\b': 'VNR',
    r'\b(v n r vjiet|vnrvjiet|vnrvjit|vnr vjit|vnr viet|vnr vjieth)\b': 'VNR VJIET',
    r'\b(vjieyt|vjiet|vjit|viet)\b': 'VJIET',
    r'\b(bachupally|bachupali|bacuhpaliylbatchupally)\b': 'Bachupally',
    r'\b(jntu h|jnmtu|jnntuh)\b': 'JNTUH',
    r'\b(eam cet|eamset|eapcet|eap cet)\b': 'EAMCET',
    r'\b(b tech|b-tech|btesh|btech)\b': 'B.Tech',
    r'\b(m tech|m-tech|mtech)\b': 'M.Tech',
    r'\b(cse aiml|cse ai ml|ai and ml)\b': 'CSE AI&MM',
    r'\b(sintillashunz|sintillazhunz|sintilashunz)\b': 'Sintillashunz',
    r'\b(convergence)\b': 'Convergence',
}



def process_speech_transcript(transcript: str) -> str:
    """
    Normalize and correct common speech-recognition phonetic anomalies
    specific to VNR VJIET queries.
    """
    if not transcript or not isinstance(transcript, str):
        return ""
    
    cleaned = transcript.strip()
    for pattern, replacement in PHONETIC_CORRECTIONS.items():
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
    
    return cleaned



def validate_transcript(transcript: str) -> Tuple[bool, str]:
    """
    Validate speech-recognized question text.
    """
    if not transcript or len(transcript.strip()) == 0:
        return False, "Please enter or speak a question."
    return True, ""



def get_stt_info() -> Dict[str, Any]:
    """
    Return speech-to-text configuration metadata.
    """
    return {
        "provider": "Web Speech API (Browser) + Backend Phonetic Normalizer",
        "language": "in-EN / en-US",
        "status": "active"
    }
