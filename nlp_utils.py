import re

def tokenize(text):
    """Extracts lowercase tokens of length > 2 from text."""
    if not text:
        return []
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text)
    return [t for t in tokens if len(t) > 2]

def levenshtein_distance(s1, s2):
    """Calculates the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def calculate_relevance(article, query):
    """
    Advanced Python-based relevance scoring algorithm.
    Calculates relevance of an article to the given query.
    """
    score = 0
    query = query.lower().strip()
    if not query:
        return 1  # Base score

    title = (article.get('title') or '').lower()
    body = (article.get('body') or '').lower()
    doc_type = (article.get('type') or '').lower()
    
    # Exact substring match
    if query in title:
        score += 50
    if query in body:
        score += 20
    if query in doc_type:
        score += 30

    # Token based fuzzy matching
    query_tokens = tokenize(query)
    title_tokens = tokenize(title)
    body_tokens = tokenize(body)
    type_tokens = tokenize(doc_type)

    for q_tok in query_tokens:
        # Title token match
        for t_tok in title_tokens:
            if q_tok == t_tok:
                score += 15
            elif q_tok in t_tok or t_tok in q_tok:
                score += 5
            elif levenshtein_distance(q_tok, t_tok) <= 1:
                score += 8
                
        # Body token match
        for b_tok in body_tokens:
            if q_tok == b_tok:
                score += 3
            elif levenshtein_distance(q_tok, b_tok) <= 1:
                score += 1
                
        # Type token match
        for ty_tok in type_tokens:
            if q_tok == ty_tok:
                score += 20

    return score
