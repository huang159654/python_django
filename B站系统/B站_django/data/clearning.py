import time
import jieba
import pandas
from jieba import analyse, posseg
from sklearn.decomposition._lda import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


class Clearing:

    def __init__(self, data=None):
        self.data = data

    def to_dataframe(self):
        dataframe = pandas.DataFrame(self.data, columns=['referenceId',
                                                         'create_time',
                                                         'update_time',
                                                         'create_date',
                                                         'update_date',
                                                         'create_user',
                                                         'productColor',
                                                         'location',
                                                         'content',
                                                         'productSize',
                                                         'referenceTime',
                                                         'referenceName',
                                                         'score',
                                                         'spider_id'])
        return dataframe

    def to_hot_dict(self):
        dataframe = pandas.DataFrame(self.data, columns=['aid', 'owner_name', 'bvid', 'category', 'pub_location',
                                                         'ctime', 'title', 'tname', 'view', 'danmaku', 'his_rank',
                                                         'like', 'reply', 'share', 'coin', 'desc', 'favorite',
                                                         'his_rank'])
        return dataframe

    def city(self):
        dataframe = self.to_hot_dict()
        city_data = dataframe['pub_location']
        city_count = city_data.value_counts().sort_index()
        return city_count.to_dict()

    def score(self):
        dataframe = self.to_hot_dict()
        score_data = dataframe['pub_location']
        score_count = score_data.value_counts()
        return score_count.to_dict()

    def categories_count(self):
        dataframe = self.to_hot_dict()
        data_ = dataframe['tname']
        info = data_.value_counts().sort_index()
        return info.to_dict()

    def date(self):
        dataframe = self.to_hot_dict()
        word = dataframe[['title', 'view', 'like', 'reply', 'share']].sort_values(by='view', ascending=False)[
               :10].values
        info = {'categories': [], 'bofang': [], 'dianzan': [], 'pinglun': [], 'zhuanfa': []}
        for w in word:
            info['categories'].append(w[0])
            info['bofang'].append(w[1])
            info['dianzan'].append(w[2])
            info['pinglun'].append(w[3])
            info['zhuanfa'].append(w[4])
        return info

    def cloud(self):
        dataframe = self.to_dataframe()
        word = dataframe['content'].values
        text = ''.join(word)
        keyword = analyse.extract_tags(text, topK=150, withWeight=True)
        word_count = []
        for kw in keyword:
            word_count.append(
                {
                    'name': kw[0],
                    'value': round(kw[1], 4)
                }
            )
        return word_count

    def aero(self):
        data_frame = self.to_hot_dict()
        aero_data = data_frame['ctime'].str.split('T', expand=True)[0]
        data_dict = aero_data.value_counts().sort_index().to_dict()
        data = {'categories': [], 'series': [{'name': '视频条数', 'data': []}]}
        for key, value in data_dict.items():
            data['categories'].append(key)
            data['series'][0]['data'].append(value)
        return data

    def three(self):
        data_frame = self.to_hot_dict()
        info = data_frame['ctime'].str.split('T', expand=True)[0]
        data = info.value_counts()
        data_dict = data.to_dict()
        sum_data = 0
        for value in data_dict.values():
            sum_data += value
        result = []
        for key in data_dict.keys():
            v = data_dict.get(key)
            result.append([key, round((v / sum_data) * 100, 2)])
        print(result)
        return result

    def s_city(self):
        dataframe = self.to_hot_dict()
        city_data = dataframe['tname']
        city_count = city_data.sort_values(axis=0, ascending=False).value_counts()[:10]
        return city_count.to_dict()

    def s_word_count(self):
        dataframe = self.to_hot_dict()
        word = dataframe['ctime'].str.split('T', expand=True)[0].value_counts()
        info = word.sort_index().to_dict()
        return info

    def s_score(self):
        dataframe = self.to_hot_dict()
        score_data = dataframe['pub_location']
        score_count = score_data.value_counts().sample(n=10)
        return score_count.to_dict()

    def s_date(self):
        data_frame = self.to_hot_dict()
        info = data_frame['ctime'].str.split('T', expand=True)[0]
        data = info.value_counts()
        data_dict = data.to_dict()
        return data_dict

    def video(self):
        dataframe = self.to_hot_dict()
        video = dataframe['pub_location'].sort_values(axis=0,ascending=False).value_counts()[:10]
        return video.to_dict()

    def video_overview(self):
        dataframe = self.to_hot_dict()
        data = dataframe[['title', 'view', 'reply', 'danmaku', 'coin']].sort_values(by='view', axis=0, ascending=False)[
               :10]
        return data.to_dict()

    def s_comment(self):
        data_frame = self.to_hot_dict()
        info = data_frame['tname'].str.split('T', expand=True)[0]
        data = info.value_counts().sample(n=10)
        data_dict = data.to_dict()
        return data_dict

    def video_city(self):
        dataframe = self.to_hot_dict()
        info = dataframe['pub_location'].value_counts()
        return info.to_dict()

    def screen(self):
        dataframe = self.to_hot_dict()
        data__ = dataframe['like'].sum()
        data_ = dataframe['title'].count()
        data = {'reply': data_, 'danmaku': data__}
        return data

    def hour(self):
        data_frame = self.to_hot_dict()
        info = data_frame['ctime'].str.split('-', expand=True)[2]
        time_ = info.str.split('T', expand=True)[1]
        data_ = time_.str.split(':', expand=True)[0].value_counts().to_dict()
        return data_



