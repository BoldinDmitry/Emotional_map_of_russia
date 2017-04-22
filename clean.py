import re
import pymorphy2


def clean_text(text: str) -> str:
    """

   :param text: текст, который нужно очистить
   :return: очищенный от частей речи, не несущих эмоциональной окраски, знаков препинания и ссылок текст
   """

    text = re.sub('^[\s\W]*|[^\w ]|\s(?=[\W\s]|$)(?u)', '', text)
    text = re.sub(r"http\S+", "", text)

    splited_text = text.split()

    return " ".join(splited_text)


def text_clean(text: str)-> list:
    """

    :param text: str of pure text
    :return: list of cleared words
    """
    morph = pymorphy2.MorphAnalyzer()
    text = clean_text(text).split()
    for_return = []
    for i in text:
        p = morph.parse(i)[0]
        if p.tag.POS not in ["PREP", "CONJ"]:
            for_return.append(p.normal_form)
    return for_return

