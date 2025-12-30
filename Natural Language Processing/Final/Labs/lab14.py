import nltk
from nltk import CFG
from nltk.parse import RecursiveDescentParser, ChartParser

print("="*60)
print("CONTEXT-FREE GRAMMAR PARSING")
print("="*60)

# ============================================
# Task 1 – Define a CFG in NLTK
# ============================================

print("\n" + "="*60)
print("TASK 1: DEFINE A CFG IN NLTK")
print("="*60)

# Define a basic CFG
grammar1 = CFG.fromstring("""
    S -> NP VP
    NP -> Det N | Det Adj N
    VP -> V NP | V
    Det -> 'the' | 'a' | 'an'
    N -> 'boy' | 'dog' | 'park' | 'cat'
    V -> 'saw' | 'walked' | 'ran'
    Adj -> 'big' | 'small' | 'black'
""")

print("Grammar 1 Productions:")
for production in grammar1.productions():
    print(f"  {production}")

# ============================================
# Task 2 – Parse a sentence
# ============================================

print("\n" + "="*60)
print("TASK 2: PARSE A SENTENCE")
print("="*60)

sentence1 = "the boy saw a dog"
tokens1 = sentence1.lower().split()

print(f"Sentence: '{sentence1}'")
print(f"Tokens: {tokens1}")

print("\n1. Recursive Descent Parser:")
rd_parser1 = RecursiveDescentParser(grammar1)
try:
    trees = list(rd_parser1.parse(tokens1))
    if trees:
        print("SUCCESS: Parse tree found:")
        tree = trees[0]
        tree.pretty_print(unicodeline=True)
    else:
        print("FAILURE: No parse trees found")
except Exception as e:
    print(f"ERROR: {e}")

print("\n2. Chart Parser:")
chart_parser1 = ChartParser(grammar1)
try:
    trees = list(chart_parser1.parse(tokens1))
    if trees:
        print("SUCCESS: Parse tree found:")
        tree = trees[0]
        tree.pretty_print(unicodeline=True)
    else:
        print("FAILURE: No parse trees found")
except Exception as e:
    print(f"ERROR: {e}")

# ============================================
# Task 3 – Ambiguity
# ============================================

print("\n" + "="*60)
print("TASK 3: AMBIGUITY AND PP-ATTACHMENT")
print("="*60)

# Extend grammar to include prepositional phrases
grammar2 = CFG.fromstring("""
    S -> NP VP
    NP -> Det N | Det Adj N | NP PP
    VP -> V NP | V NP PP | V PP
    PP -> P NP
    Det -> 'the' | 'a' | 'an'
    N -> 'boy' | 'dog' | 'park' | 'cat' | 'telescope'
    V -> 'saw' | 'walked' | 'ran' | 'chased'
    Adj -> 'big' | 'small' | 'black' | 'white'
    P -> 'in' | 'on' | 'with' | 'at'
""")

sentence2 = "the boy saw a dog in the park"
tokens2 = sentence2.lower().split()

print(f"Sentence: '{sentence2}'")
print(f"Tokens: {tokens2}")

print("\nParsing with Chart Parser (showing all parse trees):")
chart_parser2 = ChartParser(grammar2)
try:
    trees = list(chart_parser2.parse(tokens2))
    if trees:
        print(f"Found {len(trees)} parse tree(s):")
        for i, tree in enumerate(trees, 1):
            print(f"\nParse Tree {i}:")
            tree.pretty_print(unicodeline=True)
            
            # Explain the ambiguity
            if len(trees) > 1:
                if i == 1:
                    print("  Interpretation 1: The dog is in the park")
                    print("  Structure: [the boy] [saw [a dog] [in the park]]")
                    print("  PP attaches to VP")
                elif i == 2:
                    print("  Interpretation 2: The boy saw a dog that is in the park")
                    print("  Structure: [the boy] [saw [[a dog] [in the park]]]")
                    print("  PP attaches to NP")
    else:
        print("FAILURE: No parse trees found")
except Exception as e:
    print(f"ERROR: {e}")

# ============================================
# Task 4 – Extend the grammar
# ============================================

print("\n" + "="*60)
print("TASK 4: EXTEND THE GRAMMAR")
print("="*60)

# Extend grammar with adverbs and recursive NP rules
grammar3 = CFG.fromstring("""
    S -> NP VP
    NP -> Det N | Det Adj N | NP PP
    VP -> V NP | V NP PP | V PP | VP Adv
    PP -> P NP
    Det -> 'the' | 'a' | 'an'
    N -> 'boy' | 'dog' | 'park' | 'cat'
    V -> 'saw' | 'walked' | 'ran' | 'chased'
    Adj -> 'big' | 'small' | 'black' | 'white'
    P -> 'in' | 'on' | 'with' | 'at'
    Adv -> 'quickly' | 'slowly' | 'happily'
""")

sentence3 = "the dog walked in the park slowly"
tokens3 = sentence3.lower().split()

print(f"Sentence: '{sentence3}'")
print(f"Tokens: {tokens3}")

print("\nGrammar 3 Productions (new additions highlighted):")
for production in grammar3.productions():
    # Highlight new productions
    if str(production).startswith("Adv") or "VP Adv" in str(production) or "NP PP" in str(production):
        print(f"  * {production} (NEW)")
    else:
        print(f"    {production}")

print("\nParsing the sentence:")
chart_parser3 = ChartParser(grammar3)
try:
    trees = list(chart_parser3.parse(tokens3))
    if trees:
        print(f"Found {len(trees)} parse tree(s):")
        for i, tree in enumerate(trees, 1):
            print(f"\nParse Tree {i}:")
            tree.pretty_print(unicodeline=True)
            
            # Analyze the structure
            if i == 1:
                print("  Structure: [the dog] [[[walked [in the park]] slowly]]")
                print("  Interpretation: The dog walked in the park, and did so slowly")
                print("  The adverb 'slowly' modifies the verb phrase 'walked in the park'")
    else:
        print("FAILURE: No parse trees found")
except Exception as e:
    print(f"ERROR: {e}")

# Test another sentence to show multiple possibilities
print("\n" + "-"*60)
print("Testing another sentence with the extended grammar:")
sentence4 = "the boy saw the big dog in the park with a telescope"
tokens4 = sentence4.lower().split()
print(f"Sentence: '{sentence4}'")

try:
    trees = list(chart_parser3.parse(tokens4))
    if trees:
        print(f"Found {len(trees)} parse tree(s) due to multiple PP attachments")
        print(f"Ambiguity from: 'in the park' and 'with a telescope' can attach to different nodes")
    else:
        print("FAILURE: No parse trees found")
except Exception as e:
    print(f"ERROR: {e}")