from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def detect_recurring_complaint(new_text: str, existing_texts: List[Tuple[str, str]], threshold: float = 0.45) -> Tuple[bool, str]:
    """
    Analyzes similarity between a newly filed complaint and existing open complaints
    in the same taluka or department using TF-IDF and Cosine Similarity.
    
    existing_texts: list of (ticket_id, complaint_text)
    returns (is_recurring, cluster_or_matched_ticket_id)
    """
    if not existing_texts or not new_text.strip():
        return False, ""

    try:
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

        return False, ""
    except Exception as e:
        print(f"Error in complaint clustering: {e}")
        return False, ""

