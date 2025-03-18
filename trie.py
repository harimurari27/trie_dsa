import nltk
from nltk.corpus import wordnet as wn
from Levenshtein import distance

# ✅ Load WordNet data and insert into Trie
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.meaning = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, meaning):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.meaning = meaning

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # Collect all matching words
        results = []
        self._collect_words(node, prefix, results)
        return results

    def _collect_words(self, node, prefix, results):
        """Recursively collect all words with their meanings from the current node."""
        if node.is_end:
            results.append((prefix, node.meaning))
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, results)

    def auto_correct(self, word, max_distance=2, limit=10):
        """Finds the closest words based on Levenshtein distance."""
        def dfs(node, prefix):
            if node.is_end:
                dist = distance(word, prefix)
                if dist <= max_distance:
                    corrections.append((prefix, node.meaning, dist))

            for char, child in node.children.items():
                dfs(child, prefix + char)

        corrections = []
        dfs(self.root, "")
        corrections.sort(key=lambda x: x[2])  # Sort by distance
        return [(w, m) for w, m, _ in corrections[:limit]]

    def wildcard_search(self, pattern, limit=10):
        """Finds words matching wildcard patterns (* and ?)"""
        import fnmatch

        def dfs(node, prefix):
            if node.is_end and fnmatch.fnmatch(prefix, pattern):
                matches.append((prefix, node.meaning))
            for char, child in node.children.items():
                dfs(child, prefix + char)

        matches = []
        dfs(self.root, "")
        return matches[:limit]

def load_wordnet_into_trie(trie):
    """Load all words from WordNet into the Trie."""
    print("🚀 Inserting words into the Trie...")
    for synset in wn.all_synsets():
        for lemma in synset.lemmas():
            word = lemma.name().replace('_', ' ')
            meaning = synset.definition()
            trie.insert(word, meaning)

    print("✅ All words inserted into the Trie!")

# ✅ Initialize and load the Trie
trie = Trie()
nltk.download('wordnet')
load_wordnet_into_trie(trie)
