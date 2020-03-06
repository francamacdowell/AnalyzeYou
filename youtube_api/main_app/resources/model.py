import csv
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score, classification_report


class Model:
    def __init__(self):
        self.test_tags = list()
        self.train_tags = list()
        self.train_data = list()
        self.test_data = list()

        self.data_encoded = list()
        self.tags_encoded = list()

    def load_data(self):
        dataset = pd.read_csv('dataset/bags/bag.csv', sep = ';')
        data = dataset['Term']
        tags = dataset['Tag']

        self.train_data, self.test_data, self.train_tags, self.test_tags = train_test_split(data, tags,
                                                                                            test_size=0.33,
                                                                                            random_state=10)

    def encoding_features(self):
        le = preprocessing.LabelEncoder()
        self.train_data = list(le.fit_transform(self.train_data))
        self.train_data = np.reshape(self.train_data, (len(self.train_data), 1), 'C')

        self.test_data = list(le.fit_transform(self.test_data))
        self.test_data = np.reshape(self.test_data, (len(self.test_data), 1), 'C')

        self.train_tags = list(le.fit_transform(self.train_tags))
        self.test_tags = list(le.fit_transform(self.test_tags))

    def model_generate(self):
        clf = svm.SVC(1, kernel='rbf', gamma='auto')
        clf.fit(self.train_data, self.train_tags)
        prediction = clf.predict(self.test_data)
        self.define_metrics(prediction)

    def define_metrics(self, prediction):
        accuracy = accuracy_score(self.test_tags, prediction)
        precision = precision_score(self.test_tags, prediction, average=None)
        recall = recall_score(self.test_tags, prediction, average=None)
        f1 = f1_score(self.test_tags, prediction, average=None)

        report = classification_report(self.test_tags, prediction, output_dict=True)
        # print('Negative: ', report['0'])
        # print('Neutral: ', report['1'])
        # print('Positive: ', report['2'])

        print('Accuracy: ', accuracy)
        print('Precision: ', np.ndarray.tolist(precision)[1])
        print('Recall: ', np.ndarray.tolist(recall)[1])
        print('F1: ', np.ndarray.tolist(f1)[1])

naive = Model()
naive.load_data()
naive.encoding_features()
naive.model_generate()