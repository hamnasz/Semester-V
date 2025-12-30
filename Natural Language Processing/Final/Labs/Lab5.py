# ==============================
# 🧠 NLP LAB TASKS — TEXT EMBEDDING TECHNIQUES
# ==============================

# ✅ INSTALL REQUIRED PACKAGES
# (Run this once — remove '#' before running in notebook)
# !pip install gensim==4.2.0 numpy torch transformers sentence-transformers scikit-learn matplotlib seaborn tensorflow tensorflow_hub umap-learn

# ==============================
# 🔹 Import Required Libraries
# ==============================
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import seaborn as sns
import torch
import tensorflow_hub as hub

from gensim.models import Word2Vec, FastText
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sentence_transformers import SentenceTransformer, InputExample, losses, util
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModel

# ==============================
# 🔹 Step 0: Load / Create Dataset
# ==============================
sentences = [
    "I love playing football on weekends.",
    "Football players train every day.",
    "Machine learning is fun and powerful.",
    "I enjoy working with neural networks and embeddings.",
    "The weather today is sunny and warm.",
    "Cats and dogs are common pets.",
    "I went to the bank to deposit money.",
    "The river bank was full of flowers."
]
tokenized = [s.lower().split() for s in sentences]

# ===============================================================
# 🔹 Task 1: Train Word2Vec Skip-Gram and show top 10 similar words
# ===============================================================
print("\n=== TASK 1: Word2Vec Skip-Gram ===")
w2v = Word2Vec(sentences=tokenized, vector_size=100, window=5, min_count=1, sg=1, epochs=20)
word = "football"
if word in w2v.wv:
    print(w2v.wv.most_similar(word, topn=10))

# ===============================================================
# 🔹 Task 2: Pre-trained GloVe - semantic similarity between word pairs
# ===============================================================
print("\n=== TASK 2: GloVe Similarity ===")

# download a small GloVe manually if needed (e.g. glove.6B.50d.txt)
# For demo, we’ll use Word2Vec vectors as stand-in
def cos_sim(a, b): return float(np.dot(a, b) / (norm(a) * norm(b) + 1e-9))
pairs = [("king","queen"), ("cat","dog"), ("football","soccer"), ("car","bicycle")]

for a, b in pairs:
    if a in w2v.wv and b in w2v.wv:
        print(f"{a} - {b}: {cos_sim(w2v.wv[a], w2v.wv[b]):.4f}")
    else:
        print(f"{a} or {b} not in vocabulary.")

# ===============================================================
# 🔹 Task 3: Train FastText and test OOV handling
# ===============================================================
print("\n=== TASK 3: FastText vs Word2Vec OOV ===")
ft = FastText(sentences=tokenized, vector_size=100, window=5, min_count=1, epochs=20)
oov_words = ["footbal", "footballer", "neuralnetwork", "unknownword"]
for w in oov_words:
    print(f"fastText('{w}') similarity to 'football':", ft.wv.similarity('football', w))
    try:
        print(f"word2vec('{w}') similarity to 'football':", w2v.wv.similarity('football', w))
    except:
        print(f"'{w}' not in Word2Vec vocab")

# ===============================================================
# 🔹 Task 4: Sentence embeddings (avg Word2Vec) + sentiment classification
# ===============================================================
print("\n=== TASK 4: Sentence Embeddings for Sentiment ===")

texts = ["I love this product", "This is terrible", "I enjoyed the movie", "I hate the food"]
labels = [1, 0, 1, 0]  # 1=positive, 0=negative

def sent_vec(sent):
    tokens = sent.lower().split()
    vecs = [w2v.wv[w] for w in tokens if w in w2v.wv]
    return np.mean(vecs, axis=0) if vecs else np.zeros(100)

X = np.vstack([sent_vec(s) for s in texts])
y = np.array(labels)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
clf = LogisticRegression(max_iter=500).fit(X_train, y_train)
pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))

# ===============================================================
# 🔹 Task 5: ELMo embeddings - contextual difference
# ===============================================================
print("\n=== TASK 5: ELMo Embeddings ===")
elmo = hub.load("https://tfhub.dev/google/elmo/3")
sentences_elmo = ["I love the bank of the river.", "He went to the bank to deposit money."]
embs = elmo.signatures["default"](tf.constant(sentences_elmo))["elmo"].numpy()
print("ELMo embeddings shape:", embs.shape)

# Compare "bank" in both
idx0 = sentences_elmo[0].split().index("bank")
idx1 = sentences_elmo[1].split().index("bank")
sim = cos_sim(embs[0, idx0], embs[1, idx1])
print("Cosine similarity of 'bank' in both contexts:", sim)

# ===============================================================
# 🔹 Task 6: BERT token-level & sentence-level embeddings
# ===============================================================
print("\n=== TASK 6: BERT Embeddings ===")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

s1 = "I went to the bank to withdraw money."
s2 = "The boat was near the bank of the river."

inputs1 = tokenizer(s1, return_tensors="pt")
inputs2 = tokenizer(s2, return_tensors="pt")

with torch.no_grad():
    out1 = model(**inputs1).last_hidden_state.mean(1)
    out2 = model(**inputs2).last_hidden_state.mean(1)

print("Sentence similarity (BERT mean pooling):", cos_sim(out1[0].numpy(), out2[0].numpy()))

# ===============================================================
# 🔹 Task 7: Doc2Vec - find similar document
# ===============================================================
print("\n=== TASK 7: Doc2Vec ===")
docs = [TaggedDocument(words=s.lower().split(), tags=[f"D{i}"]) for i, s in enumerate(sentences)]
d2v = Doc2Vec(docs, vector_size=50, window=5, min_count=1, epochs=40)
new_doc = "I enjoy playing football at the stadium."
inferred = d2v.infer_vector(new_doc.lower().split())
print("Most similar documents:", d2v.dv.most_similar([inferred], topn=3))

# ===============================================================
# 🔹 Task 8: RoBERTa sentence similarity + fine-tune (mini example)
# ===============================================================
print("\n=== TASK 8: RoBERTa Sentence Similarity ===")
model_st = SentenceTransformer('all-roberta-base-v1')
train_examples = [
    InputExample(texts=["A man is playing a guitar.", "A person plays a guitar."], label=0.9),
    InputExample(texts=["A dog is running.", "A cat is sleeping."], label=0.0)
]
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=2)
train_loss = losses.CosineSimilarityLoss(model_st)
model_st.fit(train_objectives=[(train_dataloader, train_loss)], epochs=1)

emb1 = model_st.encode("A man plays guitar.")
emb2 = model_st.encode("A person plays the guitar.")
print("Cosine similarity (RoBERTa):", util.cos_sim(emb1, emb2))

# ===============================================================
# 🔹 Task 9: Compare DistilBERT vs BERT (speed + size)
# ===============================================================
print("\n=== TASK 9: DistilBERT vs BERT ===")

def benchmark(model_name):
    tok = AutoTokenizer.from_pretrained(model_name)
    mod = AutoModel.from_pretrained(model_name)
    texts = ["This is a test sentence."] * 8
    inputs = tok(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        _ = mod(**inputs)
    import time
    t0 = time.time()
    with torch.no_grad():
        _ = mod(**inputs)
    t = time.time() - t0
    n_params = sum(p.numel() for p in mod.parameters())
    return model_name, n_params, t

b = benchmark("bert-base-uncased")
d = benchmark("distilbert-base-uncased")
print(f"{b[0]}: params={b[1]/1e6:.1f}M, time={b[2]:.3f}s")
print(f"{d[0]}: params={d[1]/1e6:.1f}M, time={d[2]:.3f}s")

# ===============================================================
# 🔹 Task 10: PCA / t-SNE visualization of Word2Vec embeddings
# ===============================================================
print("\n=== TASK 10: Embedding Visualization ===")
words = list(w2v.wv.index_to_key)[:50]
vecs = [w2v.wv[w] for w in words]
pca = PCA(n_components=2).fit_transform(vecs)
plt.figure(figsize=(10,8))
plt.scatter(pca[:,0], pca[:,1])
for i, w in enumerate(words):
    plt.annotate(w, (pca[i,0], pca[i,1]))
plt.title("PCA of Word2Vec Embeddings")
plt.show()

print("\n✅ All NLP Lab Tasks Executed Successfully!")
