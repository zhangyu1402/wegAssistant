import pandas as pd
import json
from pandas.io.json import json_normalize
from sklearn.neighbors import NearestNeighbors
import random
import requests
import getData


class recommendation:
    def __init__(self, data, threshhold, alpha=0.7, beta=0.2, gamma=0.1):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.data = data
        self.threshhold = threshhold

    def preProcessing(self):
        self.data = json_normalize(self.data)
        self.data = self.data.set_index('sku')
        # self.data = self.data.drop("name", axis=1)
        # self.data = self.data.drop("Categories", axis=1)
        # self.data = self.categorytToNumbers(self.data)

    def categorytToNumbers(self, df):
        df = pd.get_dummies(df, columns=['Categories'])
        return df

    def filtering(self, data):
        data = data[data['Calories'] < self.threshhold]
        return data

    def recommendByRandom(self, df, nums):
        #     ls = preProcessing(data, threshold)
        # recommend = random.choices(ls, k=nums)
        recommend = df.sample(nums)
        return recommend

    def findNearest(self, df):
        nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(df)
        distances, indices = nbrs.kneighbors(df)
        return indices

    def recommendBySimilarity(self, neighbors, nums):
        neighbors = neighbors[1:]
        recommend = set(map(lambda x: random.choice(x), neighbors))
        #     recommend = list(map(lambda x: random.choices(x, k=1), indices))
        #     select multiple recommend items for every item.
        return self.recommendByRandom(recommend, nums)

    def final_recommend(self, history, nums=10):
        # history_filter = self.filtering(history)
        # history_recommend = self.recommendByRandom(history_filter, nums * 3 * self.alpha)
        # neighbors = self.findNearest(history_filter)
        # neighbor_recommend = self.recommendBySimilarity(neighbors, nums * 3 * self.beta)
        ls = self.filtering(self.data)
        random_recommend = self.recommendByRandom(ls, nums * 3 * self.gamma)
        # indices = list(set(history_recommend + neighbor_recommend + random_recommend)[:nums])
        # res = self.data.iloc[indices]
        # res = indices
        return random_recommend[:nums].to_json(orient='index')


if __name__=="__main__":
    data = getData.getData().getData("http://157.230.186.164:5000/products?page_size=2000&page_num=1")
    # print(data)
    system = recommendation(data, 150, 0, 0, 1)
    print(system.final_recommend(None, 10))