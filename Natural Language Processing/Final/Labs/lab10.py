import nltk
from nltk.corpus import conll2002
from collections import defaultdict, Counter
import numpy as np

# Download the CONLL-2002 dataset
nltk.download('conll2002')

print("="*60)
print("SPANISH NER WITH CONLL-2002 DATASET")
print("="*60)

# ============================================
# Task 1 – Explore dataset
# ============================================

print("\n" + "="*60)
print("TASK 1: EXPLORE DATASET")
print("="*60)

# Load Spanish data from CONLL-2002
print("\nLoading Spanish NER dataset...")
sentences = conll2002.iob_sents('esp.train')

print(f"Total sentences: {len(sentences)}")
print(f"First 5 sentences with NER tags:")

# Display first 5 sentences
for i in range(min(5, len(sentences))):
    print(f"\nSentence {i+1}:")
    print("-" * 40)
    
    # Get words and tags
    words = [word for word, pos, tag in sentences[i]]
    tags = [tag for word, pos, tag in sentences[i]]
    
    # Display aligned words and tags
    for j in range(len(words)):
        print(f"  Word: {words[j]:<15} | Tag: {tags[j]}")
    
    print(f"  Sentence length: {len(words)} tokens")

# Count statistics
total_tokens = sum(len(sentence) for sentence in sentences)
print(f"\nDataset Statistics:")
print(f"  Total sentences: {len(sentences)}")
print(f"  Total tokens: {total_tokens}")

# Get all unique tags
all_tags = []
for sentence in sentences:
    all_tags.extend([tag for _, _, tag in sentence])

unique_tags = set(all_tags)
print(f"  Unique NER tags: {sorted(unique_tags)}")
print(f"  Number of unique tags: {len(unique_tags)}")

# ============================================
# Task 2 – Extract sequences
# ============================================

print("\n" + "="*60)
print("TASK 2: EXTRACT SEQUENCES")
print("="*60)

# Extract word sequences and tag sequences
word_sequences = []
tag_sequences = []

for sentence in sentences[:10]:  # First 10 sentences for demonstration
    words = [word for word, pos, tag in sentence]
    tags = [tag for word, pos, tag in sentence]
    word_sequences.append(words)
    tag_sequences.append(tags)

print("\nExtracted sequences from first 3 sentences:")
print("\nSentence 1:")
print(f"  Words: {' '.join(word_sequences[0][:10])}...")
print(f"  Tags:  {' '.join(tag_sequences[0][:10])}...")

print("\nSentence 2:")
print(f"  Words: {' '.join(word_sequences[1][:10])}...")
print(f"  Tags:  {' '.join(tag_sequences[1][:10])}...")

print("\nSentence 3:")
print(f"  Words: {' '.join(word_sequences[2][:10])}...")
print(f"  Tags:  {' '.join(tag_sequences[2][:10])}...")

# Count tag frequencies
tag_counter = Counter(all_tags)
print("\nTag frequency distribution:")
for tag, count in tag_counter.most_common():
    percentage = (count / total_tokens) * 100
    print(f"  {tag:<10}: {count:>6} ({percentage:>5.1f}%)")

# ============================================
# Task 3 – Compute emission probabilities
# ============================================

print("\n" + "="*60)
print("TASK 3: COMPUTE EMISSION PROBABILITIES")
print("="*60)

# Count word-tag co-occurrences
word_tag_counts = defaultdict(Counter)
tag_counts = Counter(all_tags)

for sentence in sentences:
    for word, _, tag in sentence:
        word_lower = word.lower()  # Lowercase for better generalization
        word_tag_counts[word_lower][tag] += 1

print("\nEmission probabilities P(word|tag) for example words:")

# Example words to analyze
example_words = ['madrid', 'españa', 'presidente', 'empresa', 'la']

for word in example_words:
    word_lower = word.lower()
    if word_lower in word_tag_counts:
        print(f"\nWord: '{word}'")
        print("-" * 30)
        
        total_occurrences = sum(word_tag_counts[word_lower].values())
        
        for tag in sorted(word_tag_counts[word_lower].keys()):
            count = word_tag_counts[word_lower][tag]
            # P(word|tag) = count(word,tag) / count(tag)
            emission_prob = count / tag_counts[tag]
            
            # Also compute maximum likelihood estimate
            mle = count / total_occurrences
            
            print(f"  Tag: {tag:<10}")
            print(f"    Count(word,tag): {count}")
            print(f"    P('{word}'|{tag}) = {count}/{tag_counts[tag]} = {emission_prob:.6f}")
            print(f"    MLE P(tag|'{word}') = {count}/{total_occurrences} = {mle:.6f}")
    else:
        print(f"\nWord '{word}' not found in corpus")

# Check some common words with O tag
print("\n\nMost common words with O (Other) tag:")
o_words = [(word, count['O']) for word, count in word_tag_counts.items() if 'O' in count]
o_words_sorted = sorted(o_words, key=lambda x: x[1], reverse=True)[:5]

for word, count in o_words_sorted:
    emission_prob = count / tag_counts['O']
    print(f"  '{word}': P('{word}'|O) = {count}/{tag_counts['O']} = {emission_prob:.6f}")

# ============================================
# Task 4 – Compute transition probabilities
# ============================================

print("\n" + "="*60)
print("TASK 4: COMPUTE TRANSITION PROBABILITIES")
print("="*60)

# Count tag transitions
transition_counts = defaultdict(Counter)
start_counts = Counter()  # Count of tags at sentence start

for sentence in sentences:
    tags = [tag for _, _, tag in sentence]
    
    # Count start tag
    start_counts[tags[0]] += 1
    
    # Count transitions
    for i in range(len(tags) - 1):
        current_tag = tags[i]
        next_tag = tags[i + 1]
        transition_counts[current_tag][next_tag] += 1

# Total sentences for start probabilities
total_sentences = len(sentences)

print("\nStart probabilities (probability of tag starting a sentence):")
print("-" * 50)
for tag in sorted(start_counts.keys()):
    prob = start_counts[tag] / total_sentences
    print(f"  P({tag:<10} | START) = {start_counts[tag]}/{total_sentences} = {prob:.6f}")

print("\nTransition probabilities (selected important ones):")
print("-" * 50)

# Specific transitions to examine
important_transitions = [
    ('O', 'B-PER'),
    ('O', 'B-LOC'),
    ('O', 'B-ORG'),
    ('B-PER', 'I-PER'),
    ('I-PER', 'I-PER'),
    ('B-LOC', 'I-LOC'),
    ('B-ORG', 'I-ORG'),
    ('I-PER', 'O'),
    ('I-LOC', 'O'),
    ('I-ORG', 'O'),
    ('O', 'O')
]

for from_tag, to_tag in important_transitions:
    if from_tag in transition_counts and to_tag in transition_counts[from_tag]:
        count = transition_counts[from_tag][to_tag]
        total_from = sum(transition_counts[from_tag].values())
        prob = count / total_from
        
        print(f"  P({to_tag:<10} | {from_tag:<10}) = {count}/{total_from} = {prob:.6f}")
    else:
        print(f"  P({to_tag:<10} | {from_tag:<10}) = 0 (never observed)")

# Show all transitions from O tag
print("\nAll transitions from O tag:")
print("-" * 30)
o_transitions = transition_counts.get('O', {})
total_o = sum(o_transitions.values())

for to_tag, count in sorted(o_transitions.items()):
    prob = count / total_o
    print(f"  O → {to_tag:<10}: {count}/{total_o} = {prob:.6f}")

# Show all transitions to O tag
print("\nAll transitions to O tag:")
print("-" * 30)
to_o_transitions = []
for from_tag, transitions in transition_counts.items():
    if 'O' in transitions:
        total_from = sum(transitions.values())
        prob = transitions['O'] / total_from
        to_o_transitions.append((from_tag, transitions['O'], total_from, prob))

for from_tag, count, total_from, prob in sorted(to_o_transitions):
    print(f"  {from_tag:<10} → O: {count}/{total_from} = {prob:.6f}")