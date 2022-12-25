
class Trie:
    """ Efficient structure for holding large sets of strings when doing many look-ups.
    see: https://en.wikipedia.org/wiki/Trie"""
    def __init__(self):
        self.root = {}
        self.END_TOKEN = '*'

    def insert(self, word: str) -> None:
        current = self.root
        for letter in word:
            if letter not in current:
                current[letter] = {}
            current = current[letter]
        current[self.END_TOKEN] = True

    def holds(self, word: str) -> bool:
        current = self.root
        for letter in word:
            if letter not in current:
                return False
            current = current[letter]
        return self.END_TOKEN in current

    def add_strings(self, strings):
        for string in strings:
            self.insert(word=string)
