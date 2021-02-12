from nltk.tokenize import WhitespaceTokenizer
from nltk.util import ngrams
from collections import Counter
from random import randint, choices

tk = WhitespaceTokenizer()

with open(input(), 'r', encoding="UTF-8") as file:
    corpus = tk.tokenize(file.read())

trigrams = list(ngrams(corpus, 3))
index_dict = {}

for x, y, z in trigrams:
    index_dict.setdefault((x, y), []).append(z)

for k, v in index_dict.items():
    index_dict[k] = Counter(v)


def create_first_word():
    while True:
        candidate = list(index_dict.keys())[randint(0, len(index_dict.items()))]
        if not str(candidate[0]).istitle() or str(candidate[0][-1]) in [".", "!", "?"] \
                or str(candidate[0][0]) in ['"', '[']:
            continue
        else:
            return candidate


def create_middle_word():
    while True:
        candidate = str(list(index_dict.keys())[randint(0, len(index_dict.items()))])
        if candidate[0].isupper() or candidate[-1] in [".", "!", "?", '"', "..."]:
            continue
        else:
            return candidate


def predict_next_word(first_, second_):
    try:
        next_word = str(choices(list(index_dict[(first_, second_)].keys()),
                                list(index_dict[(first_, second_)].values()))[0])
        return next_word
    except (ValueError, IndexError):
        return create_middle_word()


for i in range(10):
    sentence = []
    first, second = create_first_word()
    sentence.append(first)
    sentence.append(second)
    while True:
        predict = predict_next_word(first, second)
        sentence.append(predict)
        first = second
        second = predict
        if len(sentence) >= 5 and predict[-1] in [".", "!", "?"]:
            break
    print(" ".join(sentence))
