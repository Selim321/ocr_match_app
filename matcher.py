import re
import string
from typing import List, Tuple, Set

def normalize(text: str) -> str:
    """Normalize the text by removing punctuation and converting to lowercase."""
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.lower()
    return text

def generate_ngrams(word: str, n: int) -> Set[str]:
    """Generate n-grams for a given word."""
    ngrams = set()
    for i in range(len(word) - n + 1):
        ngrams.add(word[i:i + n])
    return ngrams

def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Calculate Jaccard similarity between two sets of n-grams."""
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    if not union:
        return 0.0
    return len(intersection) / len(union)

def match_word(target: str, candidates: List[str], n: int) -> List[Tuple[str, float]]:
    """Match a target word with candidate words based on n-gram similarity."""
    target_ngrams = generate_ngrams(target, n)
    similarities = []
    for candidate in candidates:
        candidate_ngrams = generate_ngrams(candidate, n)
        similarity = jaccard_similarity(target_ngrams, candidate_ngrams)
        similarities.append((candidate, similarity))
    # Sort candidates by similarity in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities

def split_and_match(word: str, words_list: List[str], threshold: float = 0.3, n: int = 2) -> List[str]:
    """Split the word and match against a list of words using n-gram similarity."""
    normalized_word = normalize(word)
    word_parts = re.split(r'\s+|-', normalized_word)  # Split by spaces or hyphens
    matches = []
    for w in words_list:
        normalized_w = normalize(w)
        parts = re.split(r'\s+|-', normalized_w)  # Split by spaces or hyphens
        for part in parts:
            for keyword in word_parts:
                if match_word(part, [keyword], n)[0][1] >= threshold:
                    if w not in matches:
                        matches.append(w)
                        break
    return matches

def match_word_with_matches(word, matches, n=2):
    filtered_matches = []
    jaccard_threshold = 0.5
    n_grams_word = generate_ngrams(normalize(word), n)

    for match in matches:
      n_grams_match = generate_ngrams(normalize(match), n)
      score = jaccard_similarity(n_grams_word, n_grams_match)
      if score >= jaccard_threshold:
        filtered_matches.append(match)

    # Sort the matches by score in ascending order
    filtered_matches.sort(key=lambda x: x[1])

    # Return the list of matches
    return filtered_matches



def check_match(scanned_name: str, product_name: str, alternate_names: List[str], threshold: float = 0.3, n: int = 2) -> Tuple[bool, List[str]]:
    """Check if the scanned name matches the product name or any of the alternate names."""
    words_list = [product_name] + alternate_names
    matches = split_and_match(scanned_name, words_list, threshold, n)

    # Filter only if more than one match
    if len(matches)>1:
        matched_products = match_word_with_matches(scanned_name, matches)
    else:
        matched_products = matches

    return bool(matched_products), matched_products