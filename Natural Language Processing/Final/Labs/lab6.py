import nltk
from nltk import CFG, ChartParser, RecursiveDescentParser
from nltk.parse import ShiftReduceParser
from nltk.parse.chart import BU_STRATEGY
from nltk.parse.viterbi import ViterbiParser

# Download necessary NLTK data
nltk.download('punkt_tab')
nltk.download('punkt')

# ============================================
# Task 1: Define Context-Free Grammar in Python
# ============================================

# Define a CFG for a subset of English
original_grammar = CFG.fromstring("""
    S -> NP VP | VP
    
    NP -> Det N | Det Adj N | N | PropN | NP PP
    VP -> V | V NP | V NP PP | VP PP | 'do' 'not' VP
    PP -> P NP
    
    Det -> 'the' | 'a' | 'an' | 'this' | 'that' | 'some'
    N -> 'dog' | 'cat' | 'ball' | 'park' | 'man' | 'woman' | 'book' | 'students'
    PropN -> 'John' | 'Mary'
    V -> 'chased' | 'saw' | 'ate' | 'walked' | 'read' | 'study'
    Adj -> 'big' | 'small' | 'black' | 'white' | 'happy'
    P -> 'in' | 'on' | 'at' | 'with' | 'by'
""")

print("=" * 60)
print("TASK 1: DEFINED GRAMMAR")
print("=" * 60)
print("Original Grammar Productions:")
for production in original_grammar.productions():
    print(f"  {production}")
print(f"\nTotal productions: {len(original_grammar.productions())}")
print(f"Start symbol: {original_grammar.start()}")

# ============================================
# Task 2: Tokenize Sentences
# ============================================

def tokenize_sentence(sentence):
    """Tokenize a sentence using NLTK's word_tokenize"""
    return nltk.word_tokenize(sentence)

# Define test sentences
grammatical_sentences = [
    "John chased the dog",
    "the cat saw a ball",
    "Mary read the book",
    "the students study",
    "the man walked in the park"
]

ungrammatical_sentences = [
    "chased dog the",  # Wrong word order
    "the dog chased",  # Missing object for transitive verb
    "John the dog chased",  # Wrong determiner position
    "the big",  # Missing noun
    "walked John park the in"  # Completely wrong order
]

print("\n" + "=" * 60)
print("TASK 2: TOKENIZED SENTENCES")
print("=" * 60)
print("\nGrammatical Sentences:")
for i, sent in enumerate(grammatical_sentences, 1):
    tokens = tokenize_sentence(sent)
    print(f"{i}. Original: '{sent}'")
    print(f"   Tokens: {tokens}")

print("\nUngrammatical Sentences:")
for i, sent in enumerate(ungrammatical_sentences, 1):
    tokens = tokenize_sentence(sent)
    print(f"{i}. Original: '{sent}'")
    print(f"   Tokens: {tokens}")

# ============================================
# Task 3: Recursive Descent Parsing
# ============================================

def recursive_descent_parse(sentence, grammar):
    """Parse a sentence using recursive descent parser"""
    tokens = tokenize_sentence(sentence)
    parser = RecursiveDescentParser(grammar)
    
    print(f"\nParsing: '{sentence}'")
    print(f"Tokens: {tokens}")
    
    try:
        trees = list(parser.parse(tokens))
        if trees:
            print("SUCCESS: Parse tree(s) found:")
            for i, tree in enumerate(trees[:2]):  # Show at most 2 trees
                print(f"  Tree {i+1}:")
                tree.pretty_print(unicodeline=True)
        else:
            print("FAILURE: No parse trees found")
        return len(trees) > 0
    except Exception as e:
        print(f"ERROR: {e}")
        return False

print("\n" + "=" * 60)
print("TASK 3: RECURSIVE DESCENT PARSING")
print("=" * 60)

print("\n--- Testing Grammatical Sentences ---")
for sent in grammatical_sentences[:3]:  # Test first 3
    recursive_descent_parse(sent, original_grammar)

print("\n--- Testing Ungrammatical Sentences ---")
for sent in ungrammatical_sentences[:3]:  # Test first 3
    recursive_descent_parse(sent, original_grammar)
    print("Expected failure explanation: Sentence structure violates grammar rules")

# ============================================
# Task 4: Shift-Reduce Parsing
# ============================================

def shift_reduce_parse(sentence, grammar):
    """Parse a sentence using shift-reduce parser"""
    tokens = tokenize_sentence(sentence)
    parser = ShiftReduceParser(grammar)
    
    print(f"\nParsing: '{sentence}'")
    print(f"Tokens: {tokens}")
    
    try:
        trees = list(parser.parse(tokens))
        if trees:
            print("SUCCESS: Parse tree(s) found:")
            for i, tree in enumerate(trees[:2]):  # Show at most 2 trees
                print(f"  Tree {i+1}:")
                tree.pretty_print(unicodeline=True)
            print(f"  Total trees found: {len(trees)}")
            if len(trees) > 1:
                print("  AMBIGUITY: Multiple parse trees indicate structural ambiguity")
        else:
            print("FAILURE: No parse trees found")
        return len(trees)
    except Exception as e:
        print(f"ERROR: {e}")
        return 0

# Test ambiguous sentence
ambiguous_sentences = [
    "John saw the man with the telescope",  # PP attachment ambiguity
    "the big dog chased the black cat"  # Multiple adjective attachment
]

print("\n" + "=" * 60)
print("TASK 4: SHIFT-REDUCE PARSING")
print("=" * 60)

print("\n--- Testing for Ambiguity ---")
for sent in ambiguous_sentences:
    num_trees = shift_reduce_parse(sent, original_grammar)

# ============================================
# Task 5: Convert Grammar to Chomsky Normal Form (CNF)
# ============================================

def grammar_to_cnf(grammar):
    """Convert grammar to Chomsky Normal Form"""
    # Remove productions with more than 2 symbols on RHS
    cnf_productions = []
    
    for prod in grammar.productions():
        rhs = prod.rhs()
        
        if len(rhs) == 1 and isinstance(rhs[0], str):
            # Terminal production
            cnf_productions.append(prod)
        elif len(rhs) == 2 and all(isinstance(sym, nltk.grammar.Nonterminal) for sym in rhs):
            # Already binary non-terminal production
            cnf_productions.append(prod)
        elif len(rhs) == 2 and isinstance(rhs[0], str) and isinstance(rhs[1], nltk.grammar.Nonterminal):
            # Mixed terminal and non-terminal - needs conversion
            # Create new non-terminal for terminal
            term_symbol = rhs[0].upper() + "_TERM"
            cnf_productions.append(nltk.grammar.Production(prod.lhs(), [nltk.grammar.Nonterminal(term_symbol), rhs[1]]))
            cnf_productions.append(nltk.grammar.Production(nltk.grammar.Nonterminal(term_symbol), [rhs[0]]))
        elif len(rhs) > 2:
            # Need to binarize
            current_lhs = prod.lhs()
            for i in range(len(rhs) - 2):
                new_symbol = nltk.grammar.Nonterminal(f"{current_lhs.symbol()}_{i}")
                cnf_productions.append(nltk.grammar.Production(current_lhs, [rhs[i], new_symbol]))
                current_lhs = new_symbol
            cnf_productions.append(nltk.grammar.Production(current_lhs, [rhs[-2], rhs[-1]]))
        else:
            cnf_productions.append(prod)
    
    # Create CNF grammar
    cnf_grammar = CFG(grammar.start(), cnf_productions)
    return cnf_grammar

# Create CNF version
cnf_grammar = grammar_to_cnf(original_grammar)

print("\n" + "=" * 60)
print("TASK 5: CONVERT GRAMMAR TO CHOMSKY NORMAL FORM")
print("=" * 60)

print("\nOriginal Grammar (first 10 productions):")
for i, prod in enumerate(list(original_grammar.productions())[:10]):
    print(f"  {prod}")

print("\nCNF Grammar (first 15 productions):")
for i, prod in enumerate(list(cnf_grammar.productions())[:15]):
    print(f"  {prod}")

print(f"\nOriginal grammar has {len(original_grammar.productions())} productions")
print(f"CNF grammar has {len(cnf_grammar.productions())} productions")