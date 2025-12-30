import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter
import math
import random

# Text processing
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Scikit-learn
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('movie_reviews', quiet=True)

print("=" * 70)
print("NLP LAB: NAIVE BAYES CLASSIFICATION FOR SENTIMENT ANALYSIS")
print("=" * 70)

# ============================================
# Dataset Creation
# ============================================

# Create a sample dataset of movie reviews
def create_sample_dataset():
    """Create a balanced dataset of positive and negative movie reviews"""
    
    positive_reviews = [
        "This movie was absolutely fantastic! I loved every minute of it.",
        "Brilliant performance by the actors, highly recommended.",
        "An excellent film with great storytelling and visuals.",
        "One of the best movies I've seen this year, truly remarkable.",
        "The plot was engaging and the cinematography was stunning.",
        "Heartwarming story that kept me hooked till the end.",
        "Outstanding direction and superb acting from the entire cast.",
        "A masterpiece that deserves all the awards.",
        "I thoroughly enjoyed this movie, it was entertaining.",
        "Perfect combination of drama, action, and emotion.",
        "The characters were well-developed and relatable.",
        "Beautiful soundtrack that complemented the movie perfectly.",
        "A must-watch for all movie enthusiasts.",
        "This film exceeded all my expectations.",
        "Captivating from start to finish.",
        "The visual effects were mind-blowing.",
        "Emotionally powerful and thought-provoking.",
        "A cinematic triumph that will be remembered.",
        "The best adaptation I've seen in years.",
        "Hilarious and heartwarming at the same time."
    ]
    
    negative_reviews = [
        "This was the worst movie I've ever seen, complete waste of time.",
        "Terrible acting and a boring plot, not recommended.",
        "I was extremely disappointed with this film.",
        "The story made no sense and the characters were poorly written.",
        "Awful cinematography and bad direction.",
        "A complete disaster from beginning to end.",
        "I couldn't wait for this movie to end, it was so dull.",
        "The worst adaptation of the book imaginable.",
        "Poorly executed with no redeeming qualities.",
        "The acting was stiff and the dialogue was cringe-worthy.",
        "A boring and predictable plot with no surprises.",
        "The special effects looked cheap and unrealistic.",
        "I regret spending money on this terrible movie.",
        "The director should be ashamed of this film.",
        "Complete waste of talented actors.",
        "The screenplay was confusing and messy.",
        "Uninspired and cliché throughout.",
        "The pacing was terrible, too slow and boring.",
        "A failed attempt at being profound.",
        "I've seen better movies made by amateurs."
    ]
    
    # Combine and create labels
    reviews = positive_reviews + negative_reviews
    labels = ['positive'] * len(positive_reviews) + ['negative'] * len(negative_reviews)
    
    # Create DataFrame
    df = pd.DataFrame({
        'review': reviews,
        'sentiment': labels
    })
    
    return df

# Create dataset
df = create_sample_dataset()

# ============================================
# Task 1: Load dataset and print label distribution
# ============================================

print("\n" + "=" * 70)
print("TASK 1: DATASET LOADING AND LABEL DISTRIBUTION")
print("=" * 70)

print("\nDataset Preview (First 5 rows):")
print(df.head())

print("\nDataset Information:")
print(f"Total reviews: {len(df)}")
print(f"Positive reviews: {len(df[df['sentiment'] == 'positive'])}")
print(f"Negative reviews: {len(df[df['sentiment'] == 'negative'])}")

# Visualize label distribution
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Count plot
sentiment_counts = df['sentiment'].value_counts()
axes[0].bar(sentiment_counts.index, sentiment_counts.values, 
           color=['green', 'red'], alpha=0.7)
axes[0].set_title('Sentiment Distribution')
axes[0].set_xlabel('Sentiment')
axes[0].set_ylabel('Count')
for i, v in enumerate(sentiment_counts.values):
    axes[0].text(i, v + 0.5, str(v), ha='center', fontweight='bold')

# Pie chart
axes[1].pie(sentiment_counts.values, labels=sentiment_counts.index, 
           autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'], 
           startangle=90, explode=(0.05, 0))
axes[1].set_title('Sentiment Proportion')

plt.tight_layout()
plt.show()

# ============================================
# Task 2: Text Preprocessing
# ============================================

print("\n" + "=" * 70)
print("TASK 2: TEXT PREPROCESSING")
print("=" * 70)

class TextPreprocessor:
    """Custom text preprocessor for NLP tasks"""
    
    def __init__(self, remove_stopwords=True, stemming=True):
        self.remove_stopwords = remove_stopwords
        self.stemming = stemming
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer() if stemming else None
        
    def preprocess_text(self, text):
        """Apply preprocessing steps to text"""
        
        # 1. Lowercasing
        text = text.lower()
        
        # 2. Tokenization
        tokens = word_tokenize(text)
        
        # 3. Remove punctuation and non-alphabetic tokens
        tokens = [token for token in tokens if token.isalpha()]
        
        # 4. Remove stopwords (optional)
        if self.remove_stopwords:
            tokens = [token for token in tokens if token not in self.stop_words]
        
        # 5. Stemming (optional)
        if self.stemming and self.stemmer:
            tokens = [self.stemmer.stem(token) for token in tokens]
        
        return ' '.join(tokens)
    
    def preprocess_dataframe(self, df, text_column='review'):
        """Preprocess all texts in a DataFrame"""
        df['processed_review'] = df[text_column].apply(self.preprocess_text)
        return df

# Initialize preprocessor
preprocessor = TextPreprocessor(remove_stopwords=True, stemming=True)

# Apply preprocessing
df = preprocessor.preprocess_dataframe(df)

print("\nOriginal vs Processed Text Examples:")
print("-" * 50)
for i in range(3):
    print(f"\nExample {i+1}:")
    print(f"Original: {df['review'].iloc[i][:80]}...")
    print(f"Processed: {df['processed_review'].iloc[i]}")

# ============================================
# Task 3: Vectorization using CountVectorizer
# ============================================

print("\n" + "=" * 70)
print("TASK 3: TEXT VECTORIZATION")
print("=" * 70)

# Initialize CountVectorizer
vectorizer = CountVectorizer(
    max_features=1000,  # Limit vocabulary size
    ngram_range=(1, 2),  # Include unigrams and bigrams
    min_df=2,  # Ignore terms that appear in less than 2 documents
    max_df=0.95  # Ignore terms that appear in more than 95% of documents
)

# Fit and transform the processed reviews
X = vectorizer.fit_transform(df['processed_review'])
y = df['sentiment']

print("\nVectorization Information:")
print(f"Vocabulary size: {len(vectorizer.vocabulary_)}")
print(f"Feature matrix shape: {X.shape}")
print(f"Number of documents: {X.shape[0]}")
print(f"Number of features: {X.shape[1]}")

# Get feature names
feature_names = vectorizer.get_feature_names_out()

print("\nTop 20 features (words):")
print(feature_names[:20])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print(f"\nTraining set size: {X_train.shape[0]} samples")
print(f"Testing set size: {X_test.shape[0]} samples")

# ============================================
# Task 4: Train Multinomial Naive Bayes Classifier
# ============================================

print("\n" + "=" * 70)
print("TASK 4: TRAIN MULTINOMIAL NAIVE BAYES CLASSIFIER")
print("=" * 70)

# Train the classifier
mnb_classifier = MultinomialNB(alpha=1.0)  # Laplace smoothing
mnb_classifier.fit(X_train, y_train)

# Make predictions
y_pred = mnb_classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Evaluation:")
print(f"Accuracy: {accuracy:.4f}")
print(f"Accuracy (%): {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Negative', 'Positive'],
            yticklabels=['Negative', 'Positive'])
ax.set_xlabel('Predicted Label')
ax.set_ylabel('True Label')
ax.set_title('Confusion Matrix')
plt.show()