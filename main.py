#!/bin/python3
import json, requests, datetime
import pandas as pd


class Report:

    def __init__(self):
        self.base_url = "https://eth.2miners.com"
        self.ts = datetime.timezone.utc
        self.date_time = datetime.datetime.now(self.ts)
        self.output_path = "reports"

    @property
    def getRewardsData(self):
        return requests.get(f"{self.base_url}/endpopint").json()

    @property
    def getPayoutData(self):
        return requests.get(f"{self.base_url}/api/payments").json()

    def generateCSV(self, data):
        df = pd.json_normalize(data)
        print(df)
        df.to_csv(f"{self.output_path}/report{self.date_time}.csv")



report = Report()
report.generateCSV(json.loads(json.dumps(report.getPayoutData["payments"])))
"""
report.generateCSV(report.getPayoutData()['payments'])"""