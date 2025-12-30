import nltk
from nltk.tokenize import word_tokenize
from collections import defaultdict, Counter
import numpy as np

# Download necessary NLTK data
nltk.download('punkt')

print("="*60)
print("N-GRAM LANGUAGE MODELING")
print("="*60)

# Sample corpus
corpus = [
    "The cat sat on the mat.",
    "The dog chased the cat.",
    "The cat chased the mouse.",
    "The mouse ran from the cat.",
    "The dog sat on the mat.",
    "A cat and a dog are friends."
]

print("Original Corpus:")
for i, sentence in enumerate(corpus, 1):
    print(f"{i}. {sentence}")

# ============================================
# Task 1 — Tokenization
# ============================================

print("\n" + "="*60)
print("TASK 1: TOKENIZATION")
print("="*60)

def preprocess_sentence(sentence):
    """Convert sentence to lowercase tokens"""
    # Convert to lowercase
    sentence_lower = sentence.lower()
    # Tokenize
    tokens = word_tokenize(sentence_lower)
    # Add start and end tokens
    tokens = ['<s>'] + tokens + ['</s>']
    return tokens

# Tokenize all sentences
tokenized_corpus = [preprocess_sentence(sentence) for sentence in corpus]

print("\nTokenized sentences with <s> and </s> markers:")
for i, tokens in enumerate(tokenized_corpus, 1):
    print(f"{i}. {tokens}")

# ============================================
# Task 2 — Build Unigram and Bigram Counts
# ============================================

print("\n" + "="*60)
print("TASK 2: UNIGRAM AND BIGRAM COUNTS")
print("="*60)

# Initialize counters
unigram_counter = Counter()
bigram_counter = Counter()

# Count unigrams and bigrams
for tokens in tokenized_corpus:
    # Count unigrams
    for token in tokens:
        unigram_counter[token] += 1
    
    # Count bigrams
    for i in range(len(tokens) - 1):
        bigram = (tokens[i], tokens[i + 1])
        bigram_counter[bigram] += 1

# Display unigram counts
print("\nUnigram counts (sorted by frequency):")
total_unigrams = sum(unigram_counter.values())
print(f"Total tokens (including <s> and </s>): {total_unigrams}")

print("\nTop 10 most frequent unigrams:")
for word, count in unigram_counter.most_common(10):
    print(f"  '{word}': {count}")

print("\nAll unigram counts:")
for word, count in sorted(unigram_counter.items()):
    print(f"  '{word}': {count}")

# Display bigram counts
print("\nBigram counts (top 20):")
print("Format: (word1, word2): count")

# Sort bigrams by count
sorted_bigrams = sorted(bigram_counter.items(), key=lambda x: x[1], reverse=True)

for bigram, count in sorted_bigrams[:20]:
    print(f"  ('{bigram[0]}', '{bigram[1]}'): {count}")

print(f"\nTotal unique bigrams: {len(bigram_counter)}")

# ============================================
# Task 3 — Compute Probabilities
# ============================================

print("\n" + "="*60)
print("TASK 3: COMPUTE PROBABILITIES")
print("="*60)

# Compute unigram probabilities
print("\nUnigram probabilities:")
print("-" * 40)

for word, count in sorted(unigram_counter.items()):
    probability = count / total_unigrams
    print(f"  P('{word}') = {count}/{total_unigrams} = {probability:.6f}")

# Compute bigram conditional probabilities
print("\nBigram conditional probabilities P(w2|w1):")
print("-" * 40)

# Get some example bigrams to show
example_bigrams = [
    ('<s>', 'the'),
    ('the', 'cat'),
    ('cat', 'sat'),
    ('sat', 'on'),
    ('on', 'the'),
    ('the', 'mat'),
    ('mat', '</s>'),
    ('the', 'dog'),
    ('dog', 'chased')
]

for w1, w2 in example_bigrams:
    bigram_count = bigram_counter.get((w1, w2), 0)
    w1_count = unigram_counter.get(w1, 0)
    
    if w1_count > 0:
        probability = bigram_count / w1_count
        print(f"  P('{w2}'|'{w1}') = {bigram_count}/{w1_count} = {probability:.6f}")
    else:
        print(f"  P('{w2}'|'{w1}') = 0/{w1_count} = 0.0")

# Show all bigrams starting with 'the'
print("\nAll bigram probabilities for w1='the':")
print("-" * 40)

w1 = 'the'
w1_count = unigram_counter.get(w1, 0)

if w1_count > 0:
    # Find all bigrams starting with 'the'
    the_bigrams = [(w1, w2) for (w1_bigram, w2), count in bigram_counter.items() 
                  if w1_bigram == w1]
    
    for w1, w2 in sorted(the_bigrams):
        bigram_count = bigram_counter.get((w1, w2), 0)
        probability = bigram_count / w1_count
        print(f"  P('{w2}'|'{w1}') = {bigram_count}/{w1_count} = {probability:.6f}")
else:
    print(f"  Word '{w1}' not found in corpus")

# ============================================
# Task 4 — Unigram Sentence Probability
# ============================================

print("\n" + "="*60)
print("TASK 4: UNIGRAM SENTENCE PROBABILITY")
print("="*60)

# Test sentences
test_sentences = [
    "the cat sat",
    "the dog chased",
    "a mouse ran",
    "cat dog mouse"
]

print("\nUnigram model: P(sentence) = Π P(word)")
print("(Using log probabilities to avoid underflow)")
print("-" * 60)

for test_sentence in test_sentences:
    print(f"\nSentence: '{test_sentence}'")
    
    # Tokenize test sentence (no <s> or </s> for unigram)
    tokens = word_tokenize(test_sentence.lower())
    
    # Calculate probability
    log_prob = 0
    probabilities = []
    
    for token in tokens:
        unigram_prob = unigram_counter.get(token, 0) / total_unigrams
        probabilities.append(unigram_prob)
        if unigram_prob > 0:
            log_prob += np.log(unigram_prob)
        else:
            log_prob = -np.inf  # Zero probability
            break
    
    # Convert back to linear probability
    if log_prob == -np.inf:
        linear_prob = 0
    else:
        linear_prob = np.exp(log_prob)
    
    # Display calculation
    print(f"  Tokens: {tokens}")
    print(f"  Individual probabilities: {[f'{p:.6f}' for p in probabilities]}")
    print(f"  Log probability: {log_prob:.6f}")
    print(f"  Linear probability: {linear_prob:.6e}")
    
    if any(p == 0 for p in probabilities):
        print("  Note: Contains unseen words -> probability = 0")
