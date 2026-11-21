
import numpy as np
import pandas as pd
import re
import nltk
import string

from collections import Counter
from bs4 import BeautifulSoup
from pymorphy3 import MorphAnalyzer
from nltk import regexp_tokenize
from gensim.models import Word2Vec

with open("замок.test", "r", encoding="UTF-8") as file:
    lines = file.readlines()

df = pd.DataFrame({"text": lines})
print(df.head())

df["text_lower"] = df["text"].str.lower()
df["text_lower"] = df["text_lower"].str.replace("`", "S", regex=False)


df["text_lower"] = df["text_lower"].str.replace(r'[^\w\s]', '', regex=True)
df["text_lower"] = df["text_lower"].str.replace(r'\d+', '', regex=True)

STOPWORDS = set( pd.read_csv("stopwords.txt",encoding="UTF-8",header=None)[0])

def stopwords(text):
    return " ".join(
        word for word in str(text).split()
        if word not in STOPWORDS
    )

df["text_lower"] = df["text_lower"].apply(stopwords)

def tokenization(text):
    return re.findall(r'(?u)\b\w+\b', text)

df["ready"] = df["text_lower"].apply(tokenization)

morph = MorphAnalyzer()

def tokenize_lemmas(sent, pat=r"(?u)\b\w+\b"):
    tokens = regexp_tokenize(sent, pat)

    return [
        tok if "S" in tok else morph.parse(tok)[0].normal_form
        for tok in tokens
    ]

df["text_lower"] = df["text_lower"].map(
    lambda x: " ".join(tokenize_lemmas(x))
)


dataset = [s.split() for s in df["text_lower"]]
print(dataset[:5])


w2v_model = Word2Vec(
    min_count=10,
    window=4,
    vector_size=300,
    negative=10,
    alpha=0.03,
    min_alpha=0.0007,
    sample=6e-5,
    sg=1
)

w2v_model.build_vocab(corpus_iterable=dataset)

total_examples = w2v_model.corpus_count

w2v_model.train(
    corpus_iterable=dataset,
    total_examples=total_examples,
    epochs=6
)



print(*w2v_model.wv.most_similar(positive=['замоSк'], topn=30), sep='\n')

print('======================================')

print(*w2v_model.wv.most_similar(positive=['заSмок'], topn=30), sep='\n')
