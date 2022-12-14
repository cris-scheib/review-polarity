# -*- coding: utf-8 -*-
"""Polarity.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HXOjfV3SE1YYf7NZ2r0uL6hQGFYQBp_c
"""

import nltk
import random
import pickle
from nltk.corpus import sentence_polarity
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

nltk.download('sentence_polarity')
nltk.download('stopwords')

tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(sentence_polarity.raw())

stop_words = set(stopwords.words('english'))
filtered_sentence = [t.lower() for t in tokens if not t.lower() in stop_words]

freq_words = nltk.FreqDist(filtered_sentence)
word_features = list(freq_words.keys())[:3000]
documents = [(list(review.split(" ")), category)
                for category in sentence_polarity.categories()
                  for filename in sentence_polarity.fileids(category)
                    for review in sentence_polarity.raw(filename).splitlines()]

                    

random.shuffle(documents)

def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

featuresets = [(find_features(review), category) for (review, category) in documents]
sample_size = round(len(featuresets) / 2)
training_set = featuresets[:sample_size]
testing_set = featuresets[sample_size:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("\nAcurácia do Modelo: ")
print("Acurácia do Classificador:",(nltk.classify.accuracy(classifier, testing_set))*100)

print("\nFeatures mais informativas: ")
classifier.show_most_informative_features(15)

save_classifier = open("naivebayes.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

classifier_f = open("naivebayes.pickle", "rb")
classifier = pickle.load(classifier_f)
classifier_f.close()

classifier.train([(find_features("This is great"), 'pos')])
classifier.classify(find_features("surprising"))