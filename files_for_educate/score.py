import json

from sklearn.externals import joblib

from files_for_educate import config

poset = config.poset
neg = config.neg
try_values = {}
values = []

corpus = json.loads(open('files/corpus2.json', 'r').read())
vectorizer = joblib.load('files/vectorizer.pkl')
model = joblib.load('files/model.pkl')
for i in corpus:
    if neg.count(i) > poset.count(i) or poset.count(i) is None:
        try_values[i] = -1
    elif poset.count(i) > neg.count(i) or neg.count(i) is None:
        try_values[i] = 1
    elif poset.count(i) == neg.count(i):
        try_values[i] = 0
print(len(corpus))
print(len(try_values))

matrix = vectorizer.transform(corpus)
print(try_values.values())
x = model.score(matrix, list(try_values.values()))
print(x)
