"""
FAQ Search Engine for VNR VJIET Voice FAQ Bot.
Uses advanced TF-IDF, Cosine Similarity, Keyword matching, and Fuzzy Request Matching.
"""

import os
import re
import logging
import difflib
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

COMMON_SYNONYMS = {
    'where': ['location', 'address', 'place', 'area', 'reach'],
    'location': ['where', 'address', 'place', 'bachupally', 'nizampet'],
    'fees': ['fee', 'tuition', 'cost', 'expenses', 'payment'],
    'fee': ['fees', 'tuition', 'cost', 'expenses'],
    'placements': ['placement', 'jobs', 'hiring', 'salary', 'package', 'ctc'],
    'package': ['salary', 'placements', 'ctc', 'highest', 'average'],
    'branches': ['courses', 'programs', 'btech', 'departments'],
    'courses': ['branches', 'programs', 'btech', 'degrees'],
    'eamcet': ['eapcet', 'tgeapcet', 'counseling', 'code', 'cutoff'],
    'hostel': ['hostels', 'accommodation', 'rooms', 'stay', 'mess'],
    'bus': ['transport', 'transportation', 'routes', 'buses'],
    'fest': ['fests', 'events', 'sintillashunz', 'convergence'],
    'attendance': ['percentage', '75', 'condonation', 'rules'],
}


class FAQSearchEngine:
    """
    High-performance FAQ Search Engine for VNR VJIET Knowledge Base.
    """
    
    def __init__(self, csv_path: str = 'data/VNRVJIET_COMPLETE_DATABASE.csv'):
        self.csv_path = csv_path
        self.df = None
        self.question_col = 'Question'
        self.answer_col = 'Answer'
        self.category_col = 'Category'
        self.keywords_col = 'Keywords'
        self.vectorizer = None
        self.tfidf_matrix = None
        self.corpus = []
        self.load_database()

    def load_database(self) -> bool:
        """
        Load and index the CSV database.
        """
        if not os.path.exists(self.csv_path):
            logger.error(f'FAQ database file not found: {self.csv_path}')
            return False
        
        try:
            self.df = pd.read_csv(self.csv_path, encoding='utf-8')
        except UnicodeDecodeError:
            self.df = pd.read_csv(self.csv_path, encoding='latin1')
        except Exception as e:
            logger.error(f'Error reading FAQ CSV: {e}')
            return False

        cols = self.df.columns.tolist()
        
        # Auto-detect question column
        for c in cols:
            c_lower = str(c).strip().lower()
            if 'question' in c_lower or c_lower in ['q', 'query', 'queries']:
                self.question_col = c
                break
        
        # Auto-detect answer column
        for c in cols:
            c_lower = str(c).strip().lower()
            if 'answer' in c_lower or c_lower in ['a', 'response', 'reply']:
                self.answer_col = c
                break
        
        # Auto-detect category and keywords columns
        for c in cols:
            c_lower = str(c).strip().lower()
            if 'category' in c_lower or 'topic' in c_lower:
                self.category_col = c
            if 'keyword' in c_lower or 'tag' in c_lower:
                self.keywords_col = c
        
        self.corpus = []
        for _, row in self.df.iterrows():
            q = str(row.get(self.question_col, ''))
            a = str(row.get(self.answer_col, ''))
            cat = str(row.get(self.category_col, '')) if self.category_col in row else ''
            kw = str(row.get(self.keywords_col, '')) if self.keywords_col in row else ''
            
            # Form rich text representation
            combined = f"{q} {q} {cat} {kw} {a[:150]}"
            self.corpus.append(combined.lower())
        
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            stop_words='english',
            sublinear_tf=True,
            min_df=1
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)
        return True

    def _expand_query_synonyms(self, query: str) -> str:
        """
        Add synonyms of query words to improve retrieval recall.
        """
        words = re.findall(r'\w+', query.lower())
        expanded = list(words)
        for w in words:
            if w in COMMON_SYNONYMS:
                expanded.extend(COMMON_SYNONYMS[w])
        return ' '.join(expanded)

    def search(
        self,
        query: str,
        top_k: int = 3,
        threshold: float = 0.25
    ) -> List[Dict[str, Any]]:
        """
        Search the FAQ database for relevant entries.
        """
        if self.df is None or self.vectorizer is None or len(self.df) == 0:
            if not self.load_database():
                return []

        query_clean = query.strip().lower()
        if not query_clean:
            return []
        
        expanded_query = self._expand_query_synonyms(query_clean)
        query_vec = self.vectorizer.transform([expanded_query])
        cosine_sims = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        
        results = []
        # Filter out common stop words from token overlap
        stop_words = {'what', 'is', 'are', 'the', 'of', 'in', 'at', 'for', 'to', 'a', 'an', 'how', 'tell', 'me', 'about', 'can', 'i', 'get'}
        query_words = set(re.findall(r'\w+', query_clean)) - stop_words
        
        for i, row in self.df.iterrows():
            q_text = str(row.get(self.question_col, ''))
            a_text = str(row.get(self.answer_col, ''))
            cat_text = str(row.get(self.category_col, 'General'))
            kw_text = str(row.get(self.keywords_col, ''))
            
            cosine_score = float(cosine_sims[i])
            q_clean = q_text.lower()
            fuzzy_ratio = difflib.SequenceMatcher(None, query_clean, q_clean).ratio()
            
            target_words = set(re.findall(r'\w+', f"{q_clean} {kw_text.lower()}"))
            intersect = query_words.intersection(target_words)
            kw_overlap_ratio = len(intersect) / max(1, len(query_words)) if query_words else 0.0
            
            # If completely irrelevant, avoid accidental fuzzy score matching
            if cosine_score < 0.04 and len(intersect) == 0 and fuzzy_ratio < 0.65:
                combined_score = 0.0
            else:
                combined_score = (0.50 * cosine_score) + (0.30 * kw_overlap_ratio) + (0.20 * fuzzy_ratio)
                if query_clean in q_clean or q_clean in query_clean:
                    combined_score = min(1.0, combined_score + 0.25)
            
            results.append({
                'index': i,
                'category': cat_text,
                'question': q_text,
                'answer': a_text,
                'score': round(combined_score, 4),
                'cosine_score': round(cosine_score, 4)
            })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        filtered = [x for x in results if x['score'] >= threshold]
        return filtered[:top_k]

    def get_best_match(self, query: str, threshold: float = 0.25) -> Optional[Dict[str, Any]]:
        """
        Find the single best FAQ matching record.
        """
        matches = self.search(query, top_k=1, threshold=threshold)
        if matches:
            return matches[0]
        return None


# Singleton instance for application-wide sharing
faq_engine = FAQSearchEngine()

def search_faq(query: str, top_k: int = 3, threshold: float = 0.25) -> List[Dict[str, Any]]:
    return faq_engine.search(query, top_k=top_k, threshold=threshold)

def get_best_faq_match(query: str, threshold: float = 0.25) -> Optional[Dict[str, Any]]:
    return faq_engine.get_best_match(query, threshold=threshold)
