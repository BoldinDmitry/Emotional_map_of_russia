from sklearn.feature_extraction.text import CountVectorizer
import json
from sklearn.externals import joblib
from sklearn import linear_model

corpus = json.loads(open('files/corpus.json', 'r').read())


def educate(corpus: dict)-> None:
    """

    :param corpus:dict of shape word:coef
    :return: machine learning model and its vectorizer
    """
    vectorizer = CountVectorizer()
    regration = linear_model.LinearRegression()
    matrix = vectorizer.fit_transform(corpus)
    print(list(corpus.values()))

    regration.fit(matrix, list(corpus.values()))

    print('don')
    joblib.dump(regration, 'files/model.pkl')
    joblib.dump(vectorizer, 'files/vectorizer.pkl')


educate(corpus)
