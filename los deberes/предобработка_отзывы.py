
import numpy as np
import pandas as pd
import re
import nltk
import string

from collections import Counter
from bs4 import BeautifulSoup
from pymorphy3 import MorphAnalyzer
from nltk import sent_tokenize, word_tokenize, regexp_tokenize


# Загрузка данных
df = pd.read_csv("reviews.csv", encoding="UTF-8", sep="\t")
print(df.head())


# Приведение текста к нижнему регистру и удаление пунктуации
df['text_lower'] = df['review'].str.lower()
df['text_lower'] = df['text_lower'].str.replace(r'[^\w\s]', '', regex=True)


# Удаление стоп-слов
STOPWORDS = set(pd.read_csv("stopwords.txt", encoding="UTF-8", header=None)[0])

def stopwords(text):
    return " ".join(
        word for word in str(text).split()
        if word not in STOPWORDS
    )

df["text_lower"] = df["text_lower"].apply(stopwords)


# Подсчёт частотности слов
cnt = Counter()

for text in df["text_lower"].values:
    for word in text.split():
        cnt[word] += 1

cnt.most_common(20)


# Удаление самых частотных слов
freq = set([w for (w, wc) in cnt.most_common(10)])

def freqwords(text):
    return " ".join(
        [word for word in str(text).split() if word not in freq]
    )

df["text_lower"] = df["text_lower"].apply(freqwords)


# Удаление низкочастотных слов
freq = pd.Series(' '.join(df['text_lower']).split()).value_counts()[-10:]
freq = list(freq.index)
df['text_lower'] = df['text_lower'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))


# Удаление эмодзи
def emoji(string):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', string)

df['text_lower'] = df['text_lower'].apply(emoji)


# Удаление цифр
df['text_lower'] = df['text_lower'].str.replace(r'\d+', '', regex=True)


# Удаление URL
def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\\.\S+')
    return url_pattern.sub(r'', text)

df['text_lower'] = df['text_lower'].apply(remove_urls)


# Удаление HTML-тегов
def html(text):
    return BeautifulSoup(text, "lxml").text

df['text_lower'] = df['text_lower'].apply(html)


# Токенизация
def tokenization(text):
    text = re.split(r'\W+', text)
    return text

df['ready'] = df['text_lower'].apply(lambda x: tokenization(x.lower()))


# Лемматизация
def tokenize_lemmas(sent, pat=r"(?u)\b\w\w+\b", morph=MorphAnalyzer()):
    return [
        morph.parse(tok)[0].normal_form
        for tok in regexp_tokenize(sent, pat)
    ]

df["text_lower"] = df["text_lower"].map(lambda x: " ".join(tokenize_lemmas(x)))



df['text_ready'] = df['review'].str.lower()
df['text_ready'] = df['text_ready'].str.replace(r'\d+', '', regex=True)
df['text_ready'] = df['text_ready'].str.replace(r'[^\w\s]', '', regex=True)

df["text_ready"] = df["text_ready"].apply(stopwords)
df['text_ready'] = df['text_ready'].apply(emoji)
df['text_ready'] = df['text_ready'].apply(remove_urls)
df['text_ready'] = df['text_ready'].apply(html)

df["text_ready"] = df["text_ready"].map(lambda x: " ".join(tokenize_lemmas(x)))



df.to_csv("reviews_preprocessed_2.csv",encoding="utf-8",index=False)
