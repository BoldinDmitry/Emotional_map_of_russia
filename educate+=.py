import json

corpus = json.loads(open('files/corpus.json', 'r').read())
middle = json.loads(open('files/middle.json', 'r').read())
re_edu = json.loads(open('files/for_reeducate.json', 'r').read())
words_poset = re_edu[0]
words_neg = re_edu[1]


def educate_existing_model(words_poset: list, words_neg: list, corpus: dict) -> None:
    """

    :param words_poset: list of positive words
    :param words_neg: list of negative words
    :param corpus: dict of shape word:coef
    :return: corpus updated
    """
    words = []
    for g in words_poset:
        words.append(g)
    for g2 in words_neg:
        words.append(g2)
    for i2 in words:
        while words.count(i2) > 1:
            words.remove(i2)
    for i in words:
        if corpus.get(i) is not None:
            corpus[i] = round((corpus.get(i) * middle.get(i) + words_poset.count(i) * 1 + words_neg.count(i) * -1) /
                              (middle.get(i) + 1), 6)
        else:
            corpus[i] = round(
                (words_poset.count(i) * 1 + words_neg.count(i) * -1) / \
                (words_poset.count(i) * 1 + words_neg.count(i) * 1), 6)
    with open('files/corpus2.json', 'w') as outfile:
        json.dump(corpus, outfile)
    y = [[], []]
    with open('files/for_reeducate.json', 'w') as outfile:
        json.dump(y, outfile)


educate_existing_model(words_poset, words_neg, corpus)