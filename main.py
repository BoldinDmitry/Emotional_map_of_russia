#!/usr/bin/python3

import json

import time
from TwitterAPI import TwitterAPI
from flask import json
from sklearn.externals import joblib
import clean
import keys

consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
access_token_key = keys.access_token_key
access_token_secret = keys.access_token_secret
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

coordinates = {
    "mos": "37.21, 55.48, 37.86, 55.92",
    "nov": "30.85, 58.34, 31.56, 58.68",
    "vla": "131.8, 43.07, 132.27, 43.29",
    "eka": "60.44, 56.67, 60.78, 56.96",
    "kra": "38.85, 44.96, 39.18, 45.16",
    "mah": "47.38, 42.85, 47.51, 43.07",
    "oms": "73.03, 54.78, 73.42, 55.16",
    "per": "55.79, 57.79, 56.35, 58.20",
    "san": "30, 59.72, 30.64, 60.11",
    "soch": "39.68, 43.53, 39.77, 43.67",
    "tver": "35.65, 56.76, 36.1, 56.96",
    "ufa": "55.7, 54.65, 56.4, 54.99",
    "cheb": "47.08, 56.05, 47.41, 56.15",
    "mur": "32.95, 68.88, 33.2, 69.06",
    "volg": "44.29, 48.38, 44.83, 48.89",
    "volo": "39.71, 59.16, 40.06, 59.29",
}

ids = {
    "4303d1afc1e98c37": "mos",
    "d45aabeedb1ed3e5": "nov",
    "fed68b6202ec44f4": "vla",
    "3894e5388f482c23": "eka",
    "90bf79258d50f5be": "kra",
    "e4f274a90eb83aa7": "mah",
    "40c110b7cc33c32d": "oms",
    "f5dcd434a1d49fde": "per",
    "a76c0cd7d56c4836": "san",
    "73b30e5191bde95f": "soch",
    "3ab9598447aca64b": "tver",
    "64e10facc0bfdfcf": "ufa",
    "828195aa8b25a274": "cheb",
    "986e795b28a1d2c8": "mur",
    "ef5ec9e566f942df": "volg",
    "9b6d966595f5a86b": "volo"

}

average = {
    "mos": {"count": 0, "sum": 0},
    "nov": {"count": 0, "sum": 0},
    "vla": {"count": 0, "sum": 0},
    "eka": {"count": 0, "sum": 0},
    "kra": {"count": 0, "sum": 0},
    "mah": {"count": 0, "sum": 0},
    "oms": {"count": 0, "sum": 0},
    "per": {"count": 0, "sum": 0},
    "san": {"count": 0, "sum": 0},
    "soch": {"count": 0, "sum": 0},
    "tver": {"count": 0, "sum": 0},
    "ufa": {"count": 0, "sum": 0},
    "cheb": {"count": 0, "sum": 0},
    "mur": {"count": 0, "sum": 0},
    "volg": {"count": 0, "sum": 0},
    "volo": {"count": 0, "sum": 0}

}

corpus = json.loads(open('files/corpus.json', 'r').read())
vectorizer = joblib.load('files/vectorizer.pkl')
model = joblib.load('files/model.pkl')


def twit_grade(twits: list) -> list:
    """

    :param twits: list of twits needed to be predict§
    :return: dict of predicted coefs
    """
    predicted_twits = []

    p = 0
    for i2 in twits:
        c = 0
        p += 1
        twit = clean.text_clean(i2)
        twit2 = []
        for fp in twit:
            if corpus.get(fp) is None:
                twit.remove(fp)
                twit2.append(fp)
        if twit:
            matrix = vectorizer.transform(twit)
            predicted = list(model.predict(matrix))
            for j in predicted:
                c += j
            predicted_twits.append(round(c / len(predicted), 6))
            re_edu = json.loads(open('files/for_reeducate.json', 'r').read())
            if predicted_twits[0] >= 0:
                for d in twit:
                    re_edu[0].append(d)
                for n in twit2:
                    re_edu[0].append(n)
            elif predicted_twits[0] < 0:
                for d2 in twit:
                    re_edu[1].append(d2)
                for n2 in twit2:
                    re_edu[1].append(n2)
            file = open('files/for_reeducate.json', 'w')
            file.write(json.dumps(re_edu))
            file.close()
        else:
            predicted_twits.append(0)
    return predicted_twits


def get_twits():
    cities_emotion = json.loads(open("cities.json", "r").read())
    city_keys = coordinates.keys()
    all_coordinates = []
    list_ids = ids.keys()

    for i in city_keys:
        all_coordinates.append(coordinates[i])
    r = api.request('statuses/filter', {'locations': " , ".join(all_coordinates)})

    for item in r:
        if item["place"]["id"] in list_ids and item["lang"] == "ru" and item["text"] is not None:
            place_name = ids[item["place"]["id"]]
            grade = twit_grade([item["text"]])[0]
            n = average[place_name]["count"]

            city_sum = average[place_name]["sum"]
            city_sum = (n * city_sum + grade) / (n + 1)
            average[place_name]["count"] += 1
            average[place_name]["sum"] = city_sum
            cities_emotion[place_name] = city_sum

            f = open("cities.json", "w")
            f.write(json.dumps(cities_emotion))
            f.close()


def run_main():
    try:
        get_twits()
    except Exception as inst:
        time.sleep(1)
        print(inst)
        run_main()


run_main()

