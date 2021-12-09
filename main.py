#!/bin/python3
import json, requests, datetime
import pandas as pd


class Report:

    def __init__(self):
        self.base_url = "https://eth.2miners.com"
        self.ts = datetime.timezone.utc
        self.date_time = datetime.datetime.now(self.ts)
        self.output_path = "reports"
        self.pub_key = "WALLET_ADDY"

    @property
    def getRewardsData(self):
        return requests.get(f"{self.base_url}/endpopint").json()

    @property
    def getPayoutData(self):
        return requests.get(f"{self.base_url}/api/payments").json()

    @property
    def getAccountData(self):
        return requests.get(f"{self.base_url}/api/accounts/{self.pub_key}").json()

    def generateCSV(self, data):
        df = pd.json_normalize(data)
        df['reward'] = df['reward'].astype('float')
        #print(df.dtypes)
        #df['reward'].round(decimals=18)
        print(df)
        df.to_csv(f"{self.output_path}/report-{self.date_time}.csv")


if __name__ == "__main__":
    report = Report()
    #report.generateCSV(json.loads(json.dumps(report.getPayoutData["payments"])))
    report.generateCSV(json.loads(json.dumps(report.getAccountData["rewards"])))

