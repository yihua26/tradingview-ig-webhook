import requests
from config import *

class IGClient:
    def __init__(self):
        self.api_key = IG_API_KEY
        self.username = IG_USERNAME
        self.password = IG_PASSWORD
        self.api_url = IG_API_URL
        self.account_id = IG_ACCOUNT_ID
        self.session = requests.Session()
        self.authenticated = False
        self.access_token = None
        self.cst = None

    def login(self):
        headers = {
            "X-IG-API-KEY": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "identifier": self.username,
            "password": self.password
        }

        res = self.session.post(f"{self.api_url}/session", json=payload, headers=headers)
        if res.status_code == 200:
            self.cst = res.headers.get("CST")
            self.access_token = res.headers.get("X-SECURITY-TOKEN")
            self.authenticated = True
            print("✅ IG login successful")
        else:
            print(f"❌ Login failed: {res.text}")
            raise Exception("Login failed")

    def place_order(self, direction, epic, size):
        if not self.authenticated:
            self.login()

        headers = {
            "X-IG-API-KEY": self.api_key,
            "CST": self.cst,
            "X-SECURITY-TOKEN": self.access_token,
            "Version": "2",
            "Content-Type": "application/json"
        }

        payload = {
            "epic": epic,
            "expiry": "-",
            "direction": direction,
            "size": size,
            "orderType": "MARKET",
            "guaranteedStop": False,
            "currencyCode": "USD",
            "forceOpen": True,
            "accountId": self.account_id
        }

        res = self.session.post(f"{self.api_url}/positions/otc", json=payload, headers=headers)
        print(f"🚀 Order Response: {res.status_code}, {res.text}")
        return res.json()