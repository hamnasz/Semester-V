import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("GENDER BIAS ANALYSIS IN WORD EMBEDDINGS")
print("="*60)

# ============================================
# Simulated Word Embeddings
# ============================================

# Create a simple simulated embedding space (300 dimensions)
np.random.seed(42)
embedding_dim = 300

# Define word vectors
word_vectors = {
    # Gender words
    'he': np.random.randn(embedding_dim) * 0.5,
    'she': np.random.randn(embedding_dim) * 0.5,
    'man': np.random.randn(embedding_dim) * 0.5,
    'woman': np.random.randn(embedding_dim) * 0.5,
    'male': np.random.randn(embedding_dim) * 0.5,
    'female': np.random.randn(embedding_dim) * 0.5,
    
    # Occupations with bias
    'engineer': np.random.randn(embedding_dim) * 0.5,
    'nurse': np.random.randn(embedding_dim) * 0.5,
    'doctor': np.random.randn(embedding_dim) * 0.5,
    'teacher': np.random.randn(embedding_dim) * 0.5,
    'programmer': np.random.randn(embedding_dim) * 0.5,
    'receptionist': np.random.randn(embedding_dim) * 0.5,
    
    # Career/Family terms for WEAT
    'career': np.random.randn(embedding_dim) * 0.5,
    'business': np.random.randn(embedding_dim) * 0.5,
    'office': np.random.randn(embedding_dim) * 0.5,
    'salary': np.random.randn(embedding_dim) * 0.5,
    
    'family': np.random.randn(embedding_dim) * 0.5,
    'home': np.random.randn(embedding_dim) * 0.5,
    'children': np.random.randn(embedding_dim) * 0.5,
    'parents': np.random.randn(embedding_dim) * 0.5
}

# Artificially introduce gender bias in occupations
# Make some occupations closer to 'he' and some closer to 'she'
for word in ['engineer', 'doctor', 'programmer']:
    word_vectors[word] = word_vectors[word] + 0.3 * word_vectors['he'] - 0.1 * word_vectors['she']
    
for word in ['nurse', 'teacher', 'receptionist']:
    word_vectors[word] = word_vectors[word] - 0.1 * word_vectors['he'] + 0.3 * word_vectors['she']

# Make career terms closer to male words
for word in ['career', 'business', 'office', 'salary']:
    word_vectors[word] = word_vectors[word] + 0.2 * word_vectors['he'] - 0.1 * word_vectors['she']
    
# Make family terms closer to female words
for word in ['family', 'home', 'children', 'parents']:
    word_vectors[word] = word_vectors[word] - 0.1 * word_vectors['he'] + 0.2 * word_vectors['she']

# ============================================
# Task 1 – Compute gender direction
# ============================================

print("\n" + "="*60)
print("TASK 1: COMPUTE GENDER DIRECTION")
print("="*60)

# Compute gender direction vector
gender_direction = word_vectors['he'] - word_vectors['she']

print(f"Gender direction vector shape: {gender_direction.shape}")
print(f"Gender direction magnitude: {np.linalg.norm(gender_direction):.4f}")

# Also compute from other gender word pairs
gender_direction2 = word_vectors['man'] - word_vectors['woman']
gender_direction3 = word_vectors['male'] - word_vectors['female']

print(f"\nCosine similarity between different gender direction vectors:")
print(f"he-she vs man-woman: {cosine_similarity([gender_direction], [gender_direction2])[0][0]:.4f}")
print(f"he-she vs male-female: {cosine_similarity([gender_direction], [gender_direction3])[0][0]:.4f}")

# Normalize the gender direction
gender_direction_normalized = gender_direction / np.linalg.norm(gender_direction)
print(f"\nNormalized gender direction (first 5 dims): {gender_direction_normalized[:5]}")

# ============================================
# Task 2 – Cosine similarity bias test
# ============================================

print("\n" + "="*60)
print("TASK 2: COSINE SIMILARITY BIAS TEST")
print("="*60)

# Occupations to test
occupations = ['engineer', 'nurse', 'doctor', 'teacher', 'programmer', 'receptionist']

print(f"\n{'Occupation':<12} {'Similarity with "he"':<20} {'Similarity with "she"':<20} {'Difference':<15}")
print("-" * 70)

for occupation in occupations:
    sim_he = cosine_similarity([word_vectors[occupation]], [word_vectors['he']])[0][0]
    sim_she = cosine_similarity([word_vectors[occupation]], [word_vectors['she']])[0][0]
    diff = sim_he - sim_she
    
    print(f"{occupation:<12} {sim_he:<20.4f} {sim_she:<20.4f} {diff:>10.4f}")

# ============================================
# Task 3 – Projection on gender axis
# ============================================

print("\n" + "="*60)
print("TASK 3: PROJECTION ON GENDER AXIS")
print("="*60)

def project_on_gender_axis(word):
    """Project a word vector onto the normalized gender direction"""
    word_vec = word_vectors[word]
    projection = np.dot(word_vec, gender_direction_normalized)
    return projection

print(f"\nProjection of words on gender direction (he-she axis):")
print(f"(Positive = more 'he'-like, Negative = more 'she'-like)")
print("\n" + "-" * 60)

# Gender words themselves
print("Gender words:")
for word in ['he', 'she', 'man', 'woman', 'male', 'female']:
    proj = project_on_gender_axis(word)
    print(f"  {word:<10}: {proj:>10.4f}")

print("\nOccupations:")
for occupation in occupations:
    proj = project_on_gender_axis(occupation)
    print(f"  {occupation:<12}: {proj:>10.4f}")

print("\nCareer/Family terms:")
career_family_words = ['career', 'business', 'family', 'home']
for word in career_family_words:
    proj = project_on_gender_axis(word)
    print(f"  {word:<10}: {proj:>10.4f}")

# ============================================
# Task 4 – WEAT-style comparison
# ============================================

print("\n" + "="*60)
print("TASK 4: WEAT-STYLE COMPARISON")
print("="*60)

# Define word sets for WEAT test
male_words = ['he', 'man', 'male']
female_words = ['she', 'woman', 'female']
career_words = ['career', 'business', 'office', 'salary']
family_words = ['family', 'home', 'children', 'parents']

def compute_association(target_word, attribute_words):
    """Compute average cosine similarity between target and attribute words"""
    similarities = []
    target_vec = word_vectors[target_word]
    
    for attr_word in attribute_words:
        attr_vec = word_vectors[attr_word]
        sim = cosine_similarity([target_vec], [attr_vec])[0][0]
        similarities.append(sim)
    
    return np.mean(similarities)

print("\nAssociations between gender words and career/family terms:")
print("(Higher values indicate stronger association)")
print("\n" + "-" * 60)

print("\nMale words association:")
for word in male_words:
    career_assoc = compute_association(word, career_words)
    family_assoc = compute_association(word, family_words)
    diff = career_assoc - family_assoc
    print(f"  {word:<6}: Career={career_assoc:.4f}, Family={family_assoc:.4f}, Diff={diff:>8.4f}")

print("\nFemale words association:")
for word in female_words:
    career_assoc = compute_association(word, career_words)
    family_assoc = compute_association(word, family_words)
    diff = career_assoc - family_assoc
    print(f"  {word:<6}: Career={career_assoc:.4f}, Family={family_assoc:.4f}, Diff={diff:>8.4f}")

# Compute WEAT effect size
print("\nWEAT Effect Size Calculation:")

# Compute differential association for each word pair
def compute_differential_association(X, Y, A, B):
    """Compute s(X, Y, A, B) for WEAT"""
    total = 0
    for x in X:
        for y in Y:
            mean_a = compute_association(x, A) - compute_association(y, A)
            mean_b = compute_association(x, B) - compute_association(y, B)
            total += (mean_a - mean_b)
    return total / (len(X) * len(Y))

# Calculate WEAT effect
effect_size = compute_differential_association(male_words, female_words, career_words, family_words)
print(f"\nWEAT effect size: {effect_size:.4f}")
print(f"(Positive value indicates bias: male~career, female~family)")