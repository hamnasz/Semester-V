import nltk
from nltk.corpus import treebank
from collections import Counter, defaultdict
from nltk.grammar import PCFG, induce_pcfg, Nonterminal

# Download the Treebank dataset
nltk.download('treebank')

print("="*60)
print("PROBABILISTIC CONTEXT-FREE GRAMMAR FROM TREEBANK")
print("="*60)

# ============================================
# Task 1 – Load and inspect Treebank trees
# ============================================

print("\n" + "="*60)
print("TASK 1: LOAD AND INSPECT TREEBANK TREES")
print("="*60)

# Load parsed sentences from Treebank
parsed_sents = treebank.parsed_sents()

print(f"Total parsed sentences in Treebank: {len(parsed_sents)}")

# Display first 3 parsed trees
print("\nFirst 3 parsed sentences from Treebank:")
for i in range(min(3, len(parsed_sents))):
    print(f"\nSentence {i+1}:")
    print("-" * 40)
    tree = parsed_sents[i]
    
    # Display the tree structure
    if len(str(tree)) < 500:  # Show full tree if not too large
        print(tree)
    else:
        # Show truncated version for large trees
        print(str(tree)[:500] + "...")
    
    # Show sentence length
    leaves = tree.leaves()
    print(f"Tokens: {len(leaves)}")
    print(f"Words (first 10): {' '.join(leaves[:10])}...")

# Show tree statistics
print(f"\nTreebank Statistics:")
print(f"  Total sentences: {len(parsed_sents)}")

# Count nodes in first 100 trees
all_nodes = []
for tree in parsed_sents[:100]:
    all_nodes.extend(list(tree.subtrees()))

print(f"  Average nodes per tree (first 100): {len(all_nodes)/100:.1f}")

# ============================================
# Task 2 – Extract productions
# ============================================

print("\n" + "="*60)
print("TASK 2: EXTRACT PRODUCTIONS")
print("="*60)

# Extract productions from all trees
all_productions = []
production_counter = Counter()

print("Extracting productions from parsed trees...")
for i, tree in enumerate(parsed_sents):
    productions = tree.productions()
    all_productions.extend(productions)
    for prod in productions:
        production_counter[prod] += 1

print(f"Total productions extracted: {len(all_productions)}")
print(f"Unique productions: {len(production_counter)}")

# Show some example productions
print("\nSample productions (first 20):")
print("-" * 40)
for i, prod in enumerate(all_productions[:20]):
    lhs = prod.lhs()
    rhs = " ".join(str(sym) for sym in prod.rhs())
    print(f"{i+1:2}. {lhs} -> {rhs}")

# Show different types of productions
print("\nTypes of productions in the corpus:")
print("-" * 40)

# Categorize by LHS
lhs_counter = Counter()
rhs_length_counter = Counter()
terminal_prods = 0
nonterminal_prods = 0

for prod in all_productions:
    lhs_counter[prod.lhs()] += 1
    rhs_length = len(prod.rhs())
    rhs_length_counter[rhs_length] += 1
    
    # Check if production leads to terminals
    if all(isinstance(sym, str) for sym in prod.rhs()):
        terminal_prods += 1
    else:
        nonterminal_prods += 1

print(f"Terminal productions: {terminal_prods:,} ({terminal_prods/len(all_productions)*100:.1f}%)")
print(f"Non-terminal productions: {nonterminal_prods:,} ({nonterminal_prods/len(all_productions)*100:.1f}%)")

print("\nRHS length distribution:")
for length, count in sorted(rhs_length_counter.items()):
    percentage = count / len(all_productions) * 100
    print(f"  Length {length}: {count:>6} ({percentage:>5.1f}%)")

# ============================================
# Task 3 – Build a PCFG
# ============================================

print("\n" + "="*60)
print("TASK 3: BUILD A PCFG")
print("="*60)

print("Inducing PCFG from productions...")
# Induce PCFG from productions
pcfg_grammar = induce_pcfg(Nonterminal('S'), all_productions)

print(f"PCFG created successfully!")
print(f"Total rules in PCFG: {len(pcfg_grammar.productions())}")
print(f"Start symbol: {pcfg_grammar.start()}")

# Show some PCFG rules
print("\nSample PCFG rules (first 20):")
print("-" * 40)
for i, prod in enumerate(pcfg_grammar.productions()[:20]):
    lhs = prod.lhs()
    rhs = " ".join(str(sym) for sym in prod.rhs())
    prob = prod.prob()
    print(f"{i+1:2}. {lhs} -> {rhs} [{prob:.6f}]")

# Show rules for common non-terminals
print("\nRules for common non-terminals (with probabilities):")
print("-" * 50)

common_lhs = ['NP', 'VP', 'PP', 'S']
for lhs_symbol in common_lhs:
    lhs = Nonterminal(lhs_symbol)
    rules = [prod for prod in pcfg_grammar.productions(lhs=lhs)]
    if rules:
        print(f"\n{lhs_symbol}:")
        for prod in rules[:5]:  # Show first 5 rules
            rhs = " ".join(str(sym) for sym in prod.rhs())
            print(f"  -> {rhs} [{prod.prob():.6f}]")
        if len(rules) > 5:
            print(f"  ... and {len(rules)-5} more rules")

# ============================================
# Task 4 – Analyze rule frequencies
# ============================================

print("\n" + "="*60)
print("TASK 4: ANALYZE RULE FREQUENCIES")
print("="*60)

# Count frequencies for each CFG rule (ignoring probabilities)
cfg_counter = Counter()

for prod in all_productions:
    # Create a string representation without probability
    lhs = prod.lhs()
    rhs = tuple(str(sym) for sym in prod.rhs())
    rule_key = (str(lhs), rhs)
    cfg_counter[rule_key] += 1

print(f"Unique CFG rules: {len(cfg_counter)}")

# Most common rules
print("\nTop 20 most common CFG rules:")
print("-" * 50)
for (lhs, rhs), count in cfg_counter.most_common(20):
    rhs_str = " ".join(rhs)
    percentage = count / len(all_productions) * 100
    print(f"{lhs} -> {rhs_str}")
    print(f"  Count: {count:>6} ({percentage:>5.2f}%)")

# Rare rules (appearing only once)
rare_rules = [(rule, count) for rule, count in cfg_counter.items() if count == 1]
print(f"\nRare rules (appearing only once): {len(rare_rules)}")

# Show some rare rules
print("\nSample rare CFG rules (first 10):")
print("-" * 50)
for (lhs, rhs), count in rare_rules[:10]:
    rhs_str = " ".join(rhs)
    print(f"{lhs} -> {rhs_str}")

# Analyze by rule type
print("\nAnalysis by rule type:")
print("-" * 40)

# Rules expanding to terminals only
terminal_rules = [(rule, count) for rule, count in cfg_counter.items() 
                  if all(not sym.startswith("'") for sym in rule[1])]
nonterminal_rules = [(rule, count) for rule, count in cfg_counter.items() 
                     if any(sym.startswith("'") for sym in rule[1])]

print(f"Rules expanding to non-terminals only: {len(terminal_rules)}")
print(f"Rules expanding to terminals: {len(nonterminal_rules)}")

# Most common terminal expansions
print("\nTop 10 most common terminal expansions:")
print("-" * 40)
terminal_expansions = Counter()
for (lhs, rhs), count in cfg_counter.items():
    if any(sym.startswith("'") for sym in rhs):
        terminal_expansions[(str(lhs), tuple(rhs))] = count

for (lhs, rhs), count in terminal_expansions.most_common(10):
    rhs_str = " ".join(rhs)
    print(f"{lhs} -> {rhs_str}")
    print(f"  Count: {count}")

# Rules with different RHS lengths
print("\nRules by RHS length (most common for each length):")
print("-" * 50)

rules_by_length = defaultdict(list)
for (lhs, rhs), count in cfg_counter.items():
    rules_by_length[len(rhs)].append(((lhs, rhs), count))

for length in sorted(rules_by_length.keys()):
    rules = rules_by_length[length]
    if rules:
        (lhs, rhs), count = max(rules, key=lambda x: x[1])
        rhs_str = " ".join(rhs)
        print(f"Length {length}: {lhs} -> {rhs_str}")
        print(f"  Count: {count} (total rules of length {length}: {len(rules)})")

# Empty productions (epsilon rules)
epsilon_rules = [(rule, count) for rule, count in cfg_counter.items() if len(rule[1]) == 0]
if epsilon_rules:
    print(f"\nEpsilon (empty) rules found: {len(epsilon_rules)}")
    for (lhs, rhs), count in epsilon_rules:
        print(f"  {lhs} -> ε (count: {count})")
else:
    print("\nNo epsilon (empty) rules found in the corpus.")

# Unary rules (single symbol on RHS)
unary_rules = [(rule, count) for rule, count in cfg_counter.items() if len(rule[1]) == 1]
print(f"\nUnary rules: {len(unary_rules)}")
if unary_rules:
    # Show most common unary rules
    print("Most common unary rules:")
    for (lhs, rhs), count in sorted(unary_rules, key=lambda x: x[1], reverse=True)[:10]:
        rhs_str = " ".join(rhs)
        print(f"  {lhs} -> {rhs_str} (count: {count})")