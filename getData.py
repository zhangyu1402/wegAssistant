import json
import requests
from pandas.io.json import json_normalize


class getData:
    def getData(self, api):
        # raw = requests.get("http://127.0.0.1:5000/products?page_size=1000&page_num=1")
        raw = requests.get(api)
        raw = raw.text
        raw_json = json.loads(raw)
        df = json_normalize(raw_json)
        df = df.set_index('sku')
        filter_cols = ["Calcium", "Calories", "Calories from Fat", "Cholesterol", "Dietary Fiber",
                       "Flavor", "Folic Acid", "Iron", "Kosher", "Niacin", "Protein", "Riboflavin",
                       "Saturated Fat", "Sodium", "Sugars", "Thiamine", "Total Carbohydrate", "Total Fat",
                       "Trans Fat", "Vitamin A", "Vitamin C"]
        df = df[filter_cols]
        df = df.dropna(how='all')
        rows = df.shape[0]
        cols = []
        for col in filter_cols:
            if df[col].isna().sum() / rows <= 0.3:
                cols.append(col)
        df = df[cols]
        df = df.interpolate(method='linear', limit_direction='forward')
        return df