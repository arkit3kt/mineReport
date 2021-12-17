#!/bin/python3
import json, requests, datetime
import pandas as pd
import numpy as np
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from db.db import *

class Report:

    def __init__(self):
        self.base_url = "https://eth.2miners.com"
        self.base_url_cc = "https://min-api.cryptocompare.com/data/v2/histoday"
        self.ts = datetime.timezone.utc
        self.date_time = datetime.datetime.now(self.ts)
        self.output_path = "reports"
        self.pub_key = ""
        self.crypto_compare_key = ""

    @property
    def getRewardsData(self):
        return requests.get(f"{self.base_url}/endpopint").json()

    @property
    def getPayoutData(self):
        return requests.get(f"{self.base_url}/api/payments").json()

    @property
    def getAccountData(self):
        return requests.get(f"{self.base_url}/api/accounts/{self.pub_key}").json()

    def getPriceData(self, ticker, limit):
        return requests.get(f"{self.base_url_cc}?fsym={ticker}&tsym=USD&limit={limit}&toTs=1639550873&api_key={self.crypto_compare_key}").json()['Data']['Data']


    def generateCSV(self, data):
        df = pd.json_normalize(data)
        df['date'] = pd.to_datetime(df['timestamp'], unit='s').dt.date
        grouped = df.groupby('date', as_index=False)['reward'].sum()
        grouped['reward'] = grouped['reward'].apply(lambda x: float('.{0:0>9}'.format(x)))
        #grouped['reward'].
        length = len(df['timestamp'])

        """floor = np.floor(df['timestamp'])
        ceiling = np.ceil(df['timestamp'])"""
        grouped['timestamp'] = [df['timestamp'][length-1], df['timestamp'][0]]

        num_rows = len(grouped.index) - 1
        price_data = self.getPriceData("ETH", num_rows)
        prices = [x['close'] for x in price_data]
        grouped['price'] = prices
        grouped['earned'] = grouped['reward'] * grouped['price']
        grouped.to_csv(f"{self.output_path}/report-{self.date_time}.csv")

    def powerConversion(self, wattage):
        kwh = wattage * 24 / 1000 # 24 hrs
        cents = 100
        return kwh * self.electric / cents

    def extract(self):
        check_rewards = session.query(Rewards).all()

        print(f"Count of rewards stored = {len(check_rewards)}")
        data = json.loads(json.dumps(self.getAccountData))
        """if len(data["rewards"]) > 0:
            for i in data["rewards"]:
                new_reward = Rewards(blockheight=i['blockheight'],
                                     timestamp=i['timestamp'],
                                     reward=i['reward'],
                                     percent=i['percent'],
                                     immature=i['immature'],
                                     orphan=i['orphan'],
                                     uncle=i['uncle'])
                session.add(new_reward)
            session.commit()
                #last_four = list(map(lambda element: str(element)[1:4], alist))
        check_rewards = session.query(Rewards).all()

        print(f"Count of rewards stored = {len(check_rewards)}")
        print("Printing each row : ")
        for i in check_rewards:
            print(i)"""
        sum_rewards = data["sumrewards"]

        if len(sum_rewards) > 0:

            for i in sum_rewards:
                print(i)
                new_reward = RewardSums(interval=i['inverval'],
                                     reward=i['reward'],
                                     numreward=i['numreward'],
                                     name=i['name'],
                                     offset=i['offset'])
                session.add(new_reward)
            session.commit()
                #last_four = list(map(lambda element: str(element)[1:4], alist))
        check_rewards = session.query(RewardSums).all()

        print(f"Count of rewards stored = {len(check_rewards)}")
        print("Printing each row : ")
        for i in check_rewards:
            print(i)
if __name__ == "__main__":
    report = Report()
    #report.generateCSV(json.loads(json.dumps(report.getPayoutData["payments"])))
    #report.generateCSV(json.loads(json.dumps(report.getAccountData["rewards"])))
    #data = json.loads(json.dumps(report.getAccountData["rewards"]))
    #report.extract()
    report.generateCSV(json.loads(json.dumps(report.getAccountData["rewards"])))

