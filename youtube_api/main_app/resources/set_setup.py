from .connect_api import ConnectApi
from .data_cleaning import DataCleaning
from .sentiment_analysis import SentimentAnalysis
from .statistics_generate import StatisticsGenerate


class SetSetup:
    def __init__(self, video_link):
        self.connect_api = ConnectApi(video_link)
        self.data_cleaning = DataCleaning()
        self.sentiment_analysis = SentimentAnalysis(self.data_cleaning.tokens_list)
        self.statistics = StatisticsGenerate()
        self.channel_id = self.connect_api.get_video_details()[0]['snippet']['channelId']

    def init_api(self):
        self.connect_api.get_video_comments()
        self.data_cleaning.steps_control_to_cleaning_dataset(self.connect_api.all_comments)
        self.sentiment_analysis.analysis()

        self.statistics.sentiment_plot(self.sentiment_analysis.polarity_data)
        self.statistics.time_series_plot(self.connect_api.comments_date, self.sentiment_analysis.all_polarity)
        self.statistics.word_cloud(self.data_cleaning.all_words)

    def channel_details(self):
        response = self.connect_api.get_channel_details(self.channel_id)[0]
        return {
            'title':response['snippet']['title'],
            'subs':response['statistics']['subscriberCount'],
            'views':response['statistics']['viewCount'],
            'profile_image_link':response['snippet']['thumbnails']['default']['url']
        }

    def video_details(self):
        response = self.connect_api.get_video_details()[0]
        return {
            'title':response['snippet']['title'],
            'description':response['snippet']['description'],
            'tags':', '.join(response['snippet']['tags'])
        }

    def statistics_details(self):
        return {
            'sentiment_result':'http://localhost:8000/media/main_app/resources/statistics_img/sentiment.png',
            'time_series':'http://localhost:8000/media/main_app/resources/statistics_img/time_series.png',
            'word_cloud':'http://localhost:8000/media/main_app/resources/statistics_img/word_cloud.png'
        }


