import matplotlib.pyplot as plt
import matplotlib.dates as md
from pandas.plotting import register_matplotlib_converters
import dateutil
import statistics
import seaborn as sn
from wordcloud import WordCloud, ImageColorGenerator

register_matplotlib_converters()

class StatisticsGenerate:
    def sentiment_plot(self, list):
        labels = ['Negative', 'Neutral', 'Positive']
        colors = ['lightcoral', 'yellowgreen', 'lightskyblue']

        circle = plt.Circle((0,0), 0.7, color='white')

        plt.pie(list, labels=labels, colors=colors, wedgeprops={'linewidth':7, 'edgecolor':'white'})
        p = plt.gcf()
        p.gca().add_artist(circle)
        plt.savefig('main_app/resources/statistics_img/sentiment.png')
        plt.close(fig=None)

    def time_series_plot(self, date_list, all_polarity):
        my_dict = self.treat_date(date_list, all_polarity)

        sn.set_context('paper')
        sn.set_style('whitegrid')
        sn.despine()

        dates = [dateutil.parser.parse(i) for i in my_dict.keys()]
        xmft = md.DateFormatter('%Y-%m-%d')
        ax = plt.gca()
        ax.xaxis.set_major_formatter(xmft)
        plt.xticks(rotation=35)

        new_polarity_list = dict()
        new_polarity_list['negative'] = [statistics.mean(i['negative']) for i in my_dict.values() if len(i['negative']) > 0]
        new_polarity_list['neutral'] = [statistics.mean(i['neutral']) for i in my_dict.values() if len(i['neutral']) > 0]
        new_polarity_list['positive'] = [statistics.mean(i['positive']) for i in my_dict.values() if len(i['positive']) > 0]

        if len(new_polarity_list['negative']) != len(dates):
            x = len(dates) - len(new_polarity_list['negative'])
            dates = dates[:len(dates) - x]

        plt.plot(dates, new_polarity_list['negative'], label='Negative', color='red')
        plt.plot(dates, new_polarity_list['neutral'], label='Neutral', color='grey')
        plt.plot(dates, new_polarity_list['positive'], label='Positive', color='dodgerblue')

        plt.ylabel("Polarity")
        plt.xlabel("Date")
        plt.legend()
        plt.savefig('main_app/resources/statistics_img/time_series.png')
        plt.close(fig=None)

    @staticmethod
    def treat_date(date_list, all_polarity):
        my_dict = dict()

        for i in date_list:
            date = i.split('T')[0]
            my_dict[date] = dict()
            my_dict[date]['negative'] = list()
            my_dict[date]['neutral'] = list()
            my_dict[date]['positive'] = list()

        for i in range(len(all_polarity)):
            date = date_list[i].split('T')[0]

            if all_polarity[i] <= -0.5:
                my_dict[date]['negative'].append(all_polarity[i])
            elif -0.5 < all_polarity[i] <= 0.5 and all_polarity[i] > 0:
                my_dict[date]['neutral'].append(all_polarity[i])
            elif all_polarity[i] > 0.5:
                my_dict[date]['positive'].append(all_polarity[i])

        return my_dict

    def word_cloud(self, words):
        words = ' '.join(words)
        wordcloud = WordCloud(background_color='white').generate(words)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('main_app/resources/statistics_img/word_cloud.png')
        plt.close(fig=None)