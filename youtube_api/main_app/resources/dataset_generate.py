import sys
sys.path.append('../.././')
import csv
import nltk
import requests
from nltk.corpus import stopwords
from connect_api import ConnectApi
from data_cleaning import DataCleaning
from monkeylearn import MonkeyLearn
from connect_api import ConnectApi, DataCleaning

class DatasetGenerate:
    def __init__(self):
        self.monkey = MonkeyLearn('2354da6812b69f75537dcb4597bb9a1b2dd5c295')
        self.model_id = 'cl_Y7H23UfW'
        self.positive_tag_id = '117943466'
        self.negative_tag_id = '117943465'
        self.neutral_tag_id = '117943464'
        self.video_list = ['https://www.youtube.com/watch?v=VetniQG_yDk',
                           'https://www.youtube.com/watch?v=OhCXHY66zKo',
                           'https://www.youtube.com/watch?v=WolZclHkEaM',
                           'https://www.youtube.com/watch?v=cX8245J7xLc',
                           'https://www.youtube.com/watch?v=UqXFKSWniVU']

    def load_comments_and_write_csv(self):
        for i in range(len(self.video_list)):
            result = self.load_comments(self.video_list[i])
            self.write_in_csv_file(result, '../dataset/validation/video' + str(i) + '.csv')

    @staticmethod
    def load_comments(self, link):
        result = list()
        api = ConnectApi(link)
        api.get_video_comments()
        result = api.all_comments
        return DataCleaning().steps_control_to_cleaning_dataset(result)

    def monkey_response(self):
        response = list()
        response.append(self.monkey_learn_words_request_and_preprocess('postivie', self.positive_tag_id))
        response.append(self.monkey_learn_words_request_and_preprocess('neutral', self.neutral_tag_id))
        response.append(self.monkey_learn_words_request_and_preprocess('negative', self.negative_tag_id))

        self.write_in_csv_file(response, '../dataset/bags/bag.csv')

    def monkey_learn_words_request_and_preprocess(self, tag, tag_id):
        response = self.monkey.classifiers.tags.detail(self.model_id, tag_id)
        list_result = list()
        for i in response.body['stats']['keywords']:
            list_result.append({'term':i['term'], 'tag':tag})
        return list_result

    @staticmethod
    def write_in_csv_file(data, file_name):
        with open(file_name, 'w', newline='\n') as file:
            for i in data:
                for j in i:
                    file.write(j['term'] + ';' + j['tag'])
                    file.write('\n')

