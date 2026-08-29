"""
OpenAI LLM Integration Service for VNR VJIET Voice FAQ Bot.
Handles query augmentation with retrieved FAQ context and generates
grounded, natural answers for voice and text display.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

UNKNOWN_RESPONSE = "I'm sorry, I couldn't find that information in the VNR VJIET FAQ database."

SYSTEM_PROMPT = """You are the official AI Voice FAQ Assistant for Vallurupalli Nageswara Rao Vignana Jyothi Institute of Engineering and Technology (VNR VJIET), Hyderabad.

Your role is to help students, parents, and visitors by answering their questions accurately and politely using ONLY the provided VNR VJIET Knowledge Base context.

STRICT GUIDELINES:
1. Ground your answer EXCLUSIVELY in the provided FAQ Context.
2. If the question cannot be answered using the provided context, you MUST respond EXACTLY with:
"I'm sorry, I couldn't find that information in the VNR VJIET FAQ database."
3. Never fabricate or extrapolate information about fees, cutoffs, placements, faculty, hostel, or admissions if not explicitly given.
4. Keep the answer clear, helpful, concise (2-4 sentences where possible), and natural for text-to-speech audio reading.
5. Avoid complex markdown tables or excessive formatting that sounds awkward when read aloud.
"""


class LLMService:
    """
    Service wrapper for OpenAI Chat Completion API.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.client = None
        self._init_client()

    def _init_client(self):
        """Initialize OpenAI client if API key is present."""
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if self.api_key and self.api_key != "your_openai_api_key_here":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                logger.info("OpenAI client successfully initialized.")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
                self.client = None
        else:
            self.client = None

    def generate_answer(
        self,
        question: str,
        retrieved_faqs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate answer based on retrieved FAQ context.
        Uses OpenAI if configured; otherwise gracefully uses top FAQ match.
        """
        # Re-check key in case environment was updated
        if not self.client and os.getenv("OPENAI_API_KEY", "").strip():
            self._init_client()

        # If no relevant FAQs retrieved or top match is empty
        if not retrieved_faqs:
            return {
                "answer": UNKNOWN_RESPONSE,
                "source": "FAQ Database (No Match)",
                "used_llm": False
            }

        top_match = retrieved_faqs[0]

        # If OpenAI client is available, generate grounded AI answer
        if self.client:
            try:
                # Format context from retrieved FAQs
                context_blocks = []
                for idx, faq in enumerate(retrieved_faqs, 1):
                    context_blocks.append(
                        f"FAQ {idx} [{faq.get('category', 'General')}]:\n"
                        f"Question: {faq.get('question', '')}\n"
                        f"Answer: {faq.get('answer', '')}"
                    )
                context_str = "\n\n".join(context_blocks)

                user_prompt = (
                    f"VNR VJIET Knowledge Base Context:\n{context_str}\n\n"
                    f"User Question: {question}\n\n"
                    f"Provide the best, accurate answer based ONLY on the context above:"
                )

                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2,
                    max_tokens=250
                )

                ai_answer = response.choices[0].message.content.strip()
                return {
                    "answer": ai_answer,
                    "source": "OpenAI (gpt-4o-mini) + VNR VJIET Database",
                    "used_llm": True
                }

            except Exception as e:
                logger.warning(f"OpenAI API call failed ({e}). Falling back to database match.")
                # Fallback directly to top verified database answer
                return {
                    "answer": top_match.get("answer", UNKNOWN_RESPONSE),
                    "source": "VNR VJIET Knowledge Base (Direct)",
                    "used_llm": False
                }

        # Fallback when no OpenAI API key is set
        return {
            "answer": top_match.get("answer", UNKNOWN_RESPONSE),
            "source": "VNR VJIET Knowledge Base (Direct)",
            "used_llm": False
        }


# Singleton instance
llm_service = LLMService()

def generate_answer(question: str, retrieved_faqs: List[Dict[str, Any]]) -> Dict[str, Any]:
    return llm_service.generate_answer(question, retrieved_faqs)
