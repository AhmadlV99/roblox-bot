#!/usr/bin/env python3
import json
import logging
from config import Config
from roblox_api import RobloxAPI

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RobloxBot:
    def __init__(self):
        self.target_ids = []
    
    def load_targets(self):
        try:
            with open('targets.txt', 'r') as f:
                self.target_ids = [int(line.strip()) for line in f if line.strip()]
        except:
            self.target_ids = []
    
    def run(self):
        try:
            with open('accounts.json', 'r') as f:
                accounts = json.load(f)
        except:
            print("Error: accounts.json not found!")
            return
        
        for acc in accounts:
            api = RobloxAPI()
            print(f"Logging in as: {acc['username']}")
            if api.authenticate(acc['username'], acc['password']):
                print(f"Following targets for {acc['username']}")
                result = api.batch_follow(self.target_ids)
                print(f"Successfully followed {result} users")
            else:
                print(f"Failed to login: {acc['username']}")

if __name__ == "__main__":
    setup_logging()
    bot = RobloxBot()
    bot.load_targets()
    print(f"Loaded {len(bot.target_ids)} target users")
    bot.run()
