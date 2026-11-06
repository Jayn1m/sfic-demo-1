from typing import List, Tuple

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False

def _char_ngrams(text: str, n_min=3, n_max=5) -> set:
    text = " " + text.strip().lower() + " "
    ngrams = set()
    for n in range(n_min, n_max + 1):
        for i in range(len(text) - n + 1):
            ngrams.add(text[i:i+n])
    return ngrams

def _ngram_similarity(s1: str, s2: str) -> float:
    g1 = _char_ngrams(s1)
    g2 = _char_ngrams(s2)
    if not g1 or not g2:
        return 0.0
    return len(g1 & g2) / len(g1 | g2)

def detect_recurring_complaint(new_text: str, existing_texts: List[Tuple[str, str]], threshold: float = 0.45) -> Tuple[bool, str]:
    """
    Analyzes similarity between a newly filed complaint and existing open complaints
    in the same taluka or department using TF-IDF / Cosine Similarity or n-gram fallback.
    
    existing_texts: list of (ticket_id, complaint_text)
    returns (is_recurring, cluster_or_matched_ticket_id)
    """
    if not existing_texts or not new_text.strip():
        return False, ""

    try:
        if SKLEARN_AVAILABLE:
            corpus = [new_text] + [item[1] for item in existing_texts]
            # Char-wb n-grams work well for Indic scripts (Gujarati)
            vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))
            tfidf_matrix = vectorizer.fit_transform(corpus)
            
            # Calculate cosine similarity of new_text (row 0) with all existing complaints
            sim_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
            
            max_idx = sim_scores.argmax()
            max_score = sim_scores[max_idx]

            if max_score >= threshold:
                matched_ticket_id = existing_texts[max_idx][0]
                cluster_id = f"CLUSTER-{matched_ticket_id}"
                return True, cluster_id
        else:
            # Lightweight pure-Python fallback for serverless environments
            best_score = 0.0
            best_ticket = ""
            for ticket_id, text in existing_texts:
                score = _ngram_similarity(new_text, text)
                if score > best_score:
                    best_score = score
                    best_ticket = ticket_id

            if best_score >= threshold:
                return True, f"CLUSTER-{best_ticket}"

        return False, ""
    except Exception as e:
        print(f"Error in complaint clustering: {e}")
        return False, ""


