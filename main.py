from logging.config import stopListening
from typing import List, Set, Tuple, Dict


class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.is_end_of_word = False


class Trie:
    def __init__(self) -> None:
        self.root = self.get_node()

    def get_node(self):
        return TrieNode()

    def char_to_idx(self, ch: str) -> int:
        return ord(ch) - ord("a")

    def insert(self, word: str):
        tCrawl = self.root
        for i in range(len(word)):
            idx = self.char_to_idx(word[i])
            if not tCrawl.children[idx]:
                tCrawl.children[idx] = self.get_node()
            tCrawl = tCrawl.children[idx]
        tCrawl.is_end_of_word = True

    def search(self, word: str) -> bool:
        tCrawl = self.root
        for i in range(len(word)):
            idx = self.char_to_idx(word[i])
            if not tCrawl.children[idx]:
                return False
            tCrawl = tCrawl.children[idx]
        return tCrawl.is_end_of_word


# return list of valid words, sorted by length
def get_word_hunt_words(input_grid: List[List[str]], word_trie: Trie) -> Dict:
    h = len(input_grid)
    w = len(input_grid[0])

    word_list = {}

    def backtrack(
        r: int, c: int, node: TrieNode, word: List[str], visited: List[Tuple[int, int]]
    ):
        if node.is_end_of_word:
            word_list["".join(word)] = visited

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if not (dr == 0 and dc == 0):
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < h) and (0 <= nc < w):
                        if (nr, nc) not in visited:
                            new_char = input_grid[nr][nc]
                            new_node = node.children[word_trie.char_to_idx(new_char)]
                            if new_node:
                                backtrack(
                                    nr,
                                    nc,
                                    new_node,
                                    word + [new_char],
                                    visited + [(nr, nc)],
                                )
                                new_node = node

    for r in range(h):
        for c in range(w):
            backtrack(r, c, t.root, [], [])

    return word_list


def display_route(input_grid: List[List[str]], path: List[str]):
    h = len(input_grid)
    w = len(input_grid[0])
    start = path[0]
    end = path[-1]

    # print("<--ROUTE-->")
    for r in range(h):
        s = ""
        for c in range(w):
            if (r, c) == end:
                s += "E"
            elif (r, c) == start:
                s += "S"
            elif (r, c) in path:
                s += "*"
            else:
                s += "."
        print(s)


if __name__ == "__main__":
    with open("words.txt") as f:
        words = [line.rstrip("\n") for line in f if all([c != "-" for c in line])]
    t = Trie()
    for w in words:
        t.insert(w)

    with open("input.txt") as f:
        input = [[l[i] for i in range(len(l)) if l[i] != "\n"] for l in f]

    words = get_word_hunt_words(input, t)
    for k in sorted(words, key=len, reverse=False):
        print(f"Word: {k}")
        display_route(input, words[k])
