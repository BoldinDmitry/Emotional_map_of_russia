import json

poset = (json.loads(open('poset/learn_poset.json', 'r').read()))[0:-25000]

neg = (json.loads(open('neg/learn_neg.json', 'r').read()))[0:-25000]
print(len(neg))


def count_coef(poset: list, neg: list) -> dict:
    """

    :param poset: list of positive words
    :param neg: list of negative words
    :return:None (actually saving corpus dict and middle list)
    """
    midle = {}
    coef_i = {}
    for i in range(len(poset)):
        word = poset[i]
        if coef_i.get(word) is None:
            coef_i[word] = round(((poset.count(word) + -1 * neg.count(word)) / \
                                  (poset.count(word) + neg.count(word))), 0)
            midle[word] = (poset.count(word) + neg.count(word))
        print(i)
    with open('files/corpus2.json', 'w') as outfile:
        json.dump(coef_i, outfile)
    with open('files/middle2.json', 'w') as outfile:
        json.dump(midle, outfile)


print(count_coef(poset, neg))
