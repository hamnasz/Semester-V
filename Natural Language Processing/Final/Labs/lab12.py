import nltk
from nltk.corpus import treebank
from collections import defaultdict, Counter
import numpy as np

# Download the Penn Treebank dataset
nltk.download('treebank')
nltk.download('punkt')

print("="*60)
print("POS TAGGING WITH PENN TREEBANK")
print("="*60)

# ============================================
# Task 1 – Explore dataset
# ============================================

print("\n" + "="*60)
print("TASK 1: EXPLORE DATASET")
print("="*60)

# Load tagged sentences from Penn Treebank
tagged_sentences = treebank.tagged_sents()

print(f"Total sentences in Penn Treebank: {len(tagged_sentences)}")
print("\nFirst 5 sentences with POS tags:")

# Display first 5 sentences
for i in range(min(5, len(tagged_sentences))):
    print(f"\nSentence {i+1}:")
    print("-" * 40)
    
    # Get words and tags
    sentence = tagged_sentences[i]
    words = [word for word, tag in sentence]
    tags = [tag for word, tag in sentence]
    
    # Display aligned words and tags
    for j in range(len(words)):
        print(f"  Word: {words[j]:<15} | POS: {tags[j]}")
    
    print(f"  Sentence length: {len(words)} tokens")

# Count statistics
total_tokens = sum(len(sentence) for sentence in tagged_sentences)
print(f"\nDataset Statistics:")
print(f"  Total sentences: {len(tagged_sentences)}")
print(f"  Total tokens: {total_tokens}")

# Get all unique POS tags
all_tags = []
for sentence in tagged_sentences:
    all_tags.extend([tag for _, tag in sentence])

unique_tags = set(all_tags)
print(f"  Unique POS tags: {len(unique_tags)}")

# Show most common POS tags
tag_counter = Counter(all_tags)
print(f"\nTop 10 most frequent POS tags:")
for tag, count in tag_counter.most_common(10):
    percentage = (count / total_tokens) * 100
    print(f"  {tag:<10}: {count:>6} ({percentage:>5.1f}%)")

# ============================================
# Task 2 – Extract sequences
# ============================================

print("\n" + "="*60)
print("TASK 2: EXTRACT SEQUENCES")
print("="*60)

# Extract word sequences and tag sequences
word_sequences = []
tag_sequences = []

for sentence in tagged_sentences[:10]:  # First 10 sentences for demonstration
    words = [word for word, tag in sentence]
    tags = [tag for word, tag in sentence]
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

# Get vocabulary statistics
all_words = [word.lower() for sentence in tagged_sentences for word, _ in sentence]
vocab = set(all_words)
print(f"\nVocabulary Statistics:")
print(f"  Total word tokens: {len(all_words)}")
print(f"  Unique word types: {len(vocab)}")

# ============================================
# Task 3 – Compute emission probabilities
# ============================================

print("\n" + "="*60)
print("TASK 3: COMPUTE EMISSION PROBABILITIES")
print("="*60)

# Count word-tag co-occurrences
word_tag_counts = defaultdict(Counter)
tag_counts = Counter(all_tags)

for sentence in tagged_sentences:
    for word, tag in sentence:
        word_lower = word.lower()  # Lowercase for better generalization
        word_tag_counts[word_lower][tag] += 1

print("\nEmission probabilities P(word|tag) for example words:")

# Example words to analyze
example_words = ['the', 'cat', 'runs', 'quickly', 'market']

for word in example_words:
    word_lower = word.lower()
    if word_lower in word_tag_counts:
        print(f"\nWord: '{word}'")
        print("-" * 30)
        
        total_occurrences = sum(word_tag_counts[word_lower].values())
        
        # Show top tags for this word
        for tag, count in word_tag_counts[word_lower].most_common():
            # P(word|tag) = count(word,tag) / count(tag)
            emission_prob = count / tag_counts[tag]
            
            # Also compute maximum likelihood estimate
            mle = count / total_occurrences
            
            print(f"  Tag: {tag:<10}")
            print(f"    Count('{word}', {tag}): {count}")
            print(f"    P('{word}'|{tag}) = {count}/{tag_counts[tag]} = {emission_prob:.6f}")
            print(f"    MLE P({tag}|'{word}') = {count}/{total_occurrences} = {mle:.6f}")
            
        # Only show top 3 tags for brevity
        if len(word_tag_counts[word_lower]) > 3:
            print(f"    ... and {len(word_tag_counts[word_lower]) - 3} more tags")
    else:
        print(f"\nWord '{word}' not found in corpus")

# Show words that are highly specific to certain tags
print("\n\nWords with highest P(word|tag) for each tag (most specific words):")
specific_examples = []

for tag in ['NN', 'VB', 'JJ', 'DT', 'IN']:  # Common POS tags
    # Find words that appear mostly with this tag
    candidates = []
    for word, tag_counts_dict in word_tag_counts.items():
        if tag in tag_counts_dict:
            total_occurrences = sum(tag_counts_dict.values())
            proportion = tag_counts_dict[tag] / total_occurrences
            if proportion > 0.9 and tag_counts_dict[tag] > 5:  # >90% with this tag
                candidates.append((word, tag_counts_dict[tag], proportion))
    
    if candidates:
        # Take the most frequent one
        word, count, proportion = max(candidates, key=lambda x: x[1])
        emission_prob = count / tag_counts[tag]
        specific_examples.append((word, tag, emission_prob))
        print(f"  '{word}' for {tag:<10}: P('{word}'|{tag}) = {count}/{tag_counts[tag]} = {emission_prob:.6f}")

# ============================================
# Task 4 – Compute transition probabilities
# ============================================

print("\n" + "="*60)
print("TASK 4: COMPUTE TRANSITION PROBABILITIES")
print("="*60)

# Count tag transitions
transition_counts = defaultdict(Counter)
start_counts = Counter()  # Count of tags at sentence start

for sentence in tagged_sentences:
    tags = [tag for _, tag in sentence]
    
    # Count start tag
    start_counts[tags[0]] += 1
    
    # Count transitions
    for i in range(len(tags) - 1):
        current_tag = tags[i]
        next_tag = tags[i + 1]
        transition_counts[current_tag][next_tag] += 1

# Total sentences for start probabilities
total_sentences = len(tagged_sentences)

print("\nStart probabilities (probability of POS tag starting a sentence):")
print("-" * 50)
for tag, count in start_counts.most_common(10):
    prob = count / total_sentences
    print(f"  P({tag:<5} | START) = {count}/{total_sentences} = {prob:.6f}")

print(f"\nTop 5 most common sentence-starting tags cover {sum(start_counts.most_common(5).values())/total_sentences*100:.1f}% of sentences")

print("\nTransition probabilities for common POS sequences:")
print("-" * 50)

# Specific transitions to examine
important_transitions = [
    ('DT', 'NN'),    # Determiner → Noun
    ('DT', 'JJ'),    # Determiner → Adjective
    ('JJ', 'NN'),    # Adjective → Noun
    ('NN', 'VB'),    # Noun → Verb
    ('VB', 'DT'),    # Verb → Determiner
    ('VB', 'RB'),    # Verb → Adverb
    ('IN', 'DT'),    # Preposition → Determiner
    ('NN', 'IN'),    # Noun → Preposition
    ('PRP', 'VB'),   # Pronoun → Verb
    ('VBZ', 'JJ'),   # Verb 3rd singular → Adjective
    ('TO', 'VB'),    # To → Verb
    ('NN', 'NN'),    # Noun → Noun (compound)
    ('RB', 'JJ'),    # Adverb → Adjective
]

for from_tag, to_tag in important_transitions:
    if from_tag in transition_counts and to_tag in transition_counts[from_tag]:
        count = transition_counts[from_tag][to_tag]
        total_from = sum(transition_counts[from_tag].values())
        prob = count / total_from
        
        print(f"  P({to_tag:<5} | {from_tag:<5}) = {count:>4}/{total_from:>4} = {prob:.6f}")
    else:
        print(f"  P({to_tag:<5} | {from_tag:<5}) = 0 (never observed)")

# Show all transitions from the most common tags
print("\nAll transitions from common tags (top 3 next tags):")
print("-" * 60)

common_tags = ['NN', 'IN', 'DT', 'JJ', 'VB', 'RB']
for tag in common_tags:
    if tag in transition_counts:
        print(f"\nFrom {tag}:")
        transitions = transition_counts[tag]
        total_transitions = sum(transitions.values())
        
        for next_tag, count in transitions.most_common(3):
            prob = count / total_transitions
            print(f"  → {next_tag:<5}: {count:>4}/{total_transitions:>4} = {prob:.6f}")
        
        if len(transitions) > 3:
            print(f"  ... and {len(transitions) - 3} more possible tags")

# Show the most common bigrams
print("\nMost frequent tag bigrams in corpus:")
print("-" * 50)

bigram_counts = []
for from_tag, transitions in transition_counts.items():
    for to_tag, count in transitions.items():
        bigram_counts.append((f"{from_tag} → {to_tag}", count))

for bigram, count in sorted(bigram_counts, key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {bigram:<15}: {count:>6} occurrences")