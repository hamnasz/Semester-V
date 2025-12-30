import nltk
from nltk.corpus import wordnet as wn

# Download WordNet data
nltk.download('wordnet')
nltk.download('omw-eng')

print("="*60)
print("WORDNET SEMANTIC ANALYSIS LAB")
print("="*60)

# ============================================
# Task 1 — Explore Synsets
# ============================================

print("\n" + "="*60)
print("TASK 1: EXPLORE SYNSETS - WORD: 'bank'")
print("="*60)

word = "bank"
synsets = wn.synsets(word)

print(f"\nAll synsets for the word '{word}':")
print("-" * 40)

for i, synset in enumerate(synsets, 1):
    print(f"\n{i}. {synset.name()}:")
    print(f"   Definition: {synset.definition()}")
    print(f"   Examples: {synset.examples()}")
    print(f"   Lemma names: {synset.lemma_names()}")

print(f"\nTotal senses of '{word}': {len(synsets)}")

# ============================================
# Task 2 — Explore Lexical Relations
# ============================================

print("\n" + "="*60)
print("TASK 2: EXPLORE LEXICAL RELATIONS")
print("="*60)

# Test words for different relations
test_words = ["car", "happy", "dog"]

for word in test_words:
    print(f"\nWord: '{word}'")
    print("-" * 40)
    
    # Get the most common synset
    synset = wn.synsets(word)[0]
    
    # Hypernyms (more general terms)
    hypernyms = synset.hypernyms()
    if hypernyms:
        print(f"Hypernyms (more general): {[h.name() for h in hypernyms]}")
    
    # Hyponyms (more specific terms)
    hyponyms = synset.hyponyms()
    if hyponyms:
        print(f"Hyponyms (more specific, first 5): {[h.name() for h in hyponyms[:5]]}")
        print(f"  Total hyponyms: {len(hyponyms)}")
    
    # Meronyms (part-of relations)
    meronyms = synset.part_meronyms() + synset.substance_meronyms() + synset.member_meronyms()
    if meronyms:
        print(f"Meronyms (parts/members): {[m.name() for m in meronyms[:3]]}")
    
    # Holonyms (whole-of relations)
    holonyms = synset.part_holonyms() + synset.substance_holonyms() + synset.member_holonyms()
    if holonyms:
        print(f"Holonyms (wholes): {[h.name() for h in holonyms[:3]]}")
    
    # Antonyms
    antonyms = []
    for lemma in synset.lemmas():
        if lemma.antonyms():
            antonyms.extend([ant.name() for ant in lemma.antonyms()])
    if antonyms:
        print(f"Antonyms: {list(set(antonyms))}")

# ============================================
# Task 3 — Path Similarity
# ============================================

print("\n" + "="*60)
print("TASK 3: PATH SIMILARITY")
print("="*60)

# Word pairs to compare
word_pairs = [
    ("car", "vehicle"),
    ("car", "bicycle"),
    ("car", "cat"),
    ("dog", "cat"),
    ("dog", "wolf"),
    ("happy", "sad"),
    ("happy", "joyful")
]

print("\nPath Similarity Scores:")
print("-" * 40)

for word1, word2 in word_pairs:
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)
    
    if synsets1 and synsets2:
        # Get first synset for each word
        syn1 = synsets1[0]
        syn2 = synsets2[0]
        
        similarity = syn1.path_similarity(syn2)
        
        if similarity is not None:
            print(f"'{word1}' - '{word2}': {similarity:.3f}")
        else:
            print(f"'{word1}' - '{word2}': No path found")
    else:
        print(f"'{word1}' or '{word2}' not found in WordNet")

# ============================================
# Task 4 — Wu-Palmer Similarity
# ============================================

print("\n" + "="*60)
print("TASK 4: WU-PALMER SIMILARITY")
print("="*60)

# Use same word pairs for comparison
print("\nWu-Palmer Similarity Scores:")
print("-" * 40)

for word1, word2 in word_pairs:
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)
    
    if synsets1 and synsets2:
        # Get first synset for each word
        syn1 = synsets1[0]
        syn2 = synsets2[0]
        
        similarity = syn1.wup_similarity(syn2)
        
        if similarity is not None:
            print(f"'{word1}' - '{word2}': {similarity:.3f}")
        else:
            print(f"'{word1}' - '{word2}': No similarity computed")
    else:
        print(f"'{word1}' or '{word2}' not found in WordNet")