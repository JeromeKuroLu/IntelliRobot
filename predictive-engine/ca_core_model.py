import csv
import os
import re
import scipy
import string
# import np
# import pandas as pd

import numpy
from nltk.cluster import KMeansClusterer, GAAClusterer, euclidean_distance
import nltk.corpus
import nltk.stem
from nltk.corpus import wordnet

from sklearn import feature_extraction
from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import stopwords

from sklearn.externals import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
# from sklearn.neural_network import MLPClassifier

import csv

tfidfTransformerDataPath = './data/tfid.tarnformer' 
# rawTrainingDataDataPath = './data/text-learning-raw-2016-01-15.csv'
# rawTrainingDataDataPath = './data/text-learning-data-2016-02-24.csv'
baseFilePath = './data/'

sgdTrainingModelDataPath = './data/sgdTrainingModel.model'
nbTrainingModelDataPath = './data/nbTrainingModel.model'

class Intention(object):
    name = ''
    prob = 0

class TrainingClassifer(object):
    classifer = {}
    dataPath = ''

def extractFeatures(raw_data):
    print ('Start: Extract feature')
    stop_words = stopwords.words('english')
    tfidf_transformer = TfidfVectorizer(use_idf=False, stop_words=stop_words, ngram_range=(1, 2))
    transformed_data = tfidf_transformer.fit_transform(raw_data).todense()
    joblib.dump(tfidf_transformer, tfidfTransformerDataPath)

    return transformed_data, tfidf_transformer

def buildTrainingData(sourceFileName):
    print ('buildTrainingData: Start')
    trainingData = []
    trainingLabel = []
    f = open(baseFilePath + sourceFileName, 'r')  
    for row in csv.reader(f):
        trainingLabel.append(row[0].split('!@#')[0])
        trainingData.append(row[0].split('!@#')[1])
    f.close()

    print ('buildTrainingData: End')
    return trainingLabel, trainingData

def trainModel(classifier, modelDataPath, transformed_train_data, trainingLabel):
    # print (classifier)
    model = classifier.fit(transformed_train_data, trainingLabel)
    joblib.dump(model, modelDataPath)

def intentionRecognition(trainingModelDataPath, phrase):
    tfidf_transformer = joblib.load(tfidfTransformerDataPath)
    model = joblib.load(trainingModelDataPath)

    transformed_data = tfidf_transformer.transform([phrase])
    featureNames = model.classes_

    if (transformed_data.nonzero()[1].size == 0):
        return []

    else:
        predictionResult = []
        predictDataProb = model.predict_proba(transformed_data)
        print('Probability of Intetnion')
        pos = 0
        for prob in predictDataProb[0]:
            intention = Intention()
            intention.name = featureNames[pos]
            intention.prob = round(prob * 100, 3)
            predictionResult.append(intention)
            # predictionResult.append()
            # print (featureNames[pos] + ':' + str(prob))
            # print (intention.name + ':' + intention.prob)
            pos = pos +1

        # print (sorted(predictionResult, key=lambda result: result.prob))
        # print (predictionResult)

        return sorted(predictionResult, key=lambda result: result.prob, reverse=True)
        # return predictionResult


def training(sourceFileName):
    print ('Training: ================== Start ')
    print ('Training: start load data')

    classifierList = []
    trainingRawLabel, trainingRawData = buildTrainingData(sourceFileName)

    print ('Training: finish load data')
    trainingDataRatio = 0.6
    testDataRatio = 0.2
    validationDataRatio = 0.2

    print ('Training: start ')
    # trainingData, testValidationData = train_test_split(trainingRawData, train_size = trainingDataRatio)
    # trainingLabel, testValidationLabel = train_test_split(trainingRawLabel, train_size = trainingDataRatio)
    # testData, validationData = train_test_split(data, train_size = trainingDataRatio)
    
    transformed_train_data, tfidf_transformer = extractFeatures(trainingRawData)
    print ('End: Extract feature')

    # Native Bayes
    nbClassifer = TrainingClassifer()
    nbClassifer.classifier = MultinomialNB()
    nbClassifer.dataPath = nbTrainingModelDataPath
    classifierList.append(nbClassifer)
    # SGD
    sgdClassifer = TrainingClassifer()
    sgdClassifer.classifier = SGDClassifier(loss='log', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)
    sgdClassifer.dataPath = sgdTrainingModelDataPath
    classifierList.append(sgdClassifer)

    for target in classifierList:
        # print ('Start training')
        # print (target)
        trainModel(target.classifier, target.dataPath, transformed_train_data, trainingRawLabel)

    return 'completed'

def predict(type, phrase):
    print ('Start prediction ' + phrase)
    if type == 'sgd':        
        return intentionRecognition(sgdTrainingModelDataPath, phrase)
    elif type == 'nb':
        return intentionRecognition(nbTrainingModelDataPath, phrase)


# training()
# print (predict('sgd', 'do you offer any vessel go to Kaohsiung?'))