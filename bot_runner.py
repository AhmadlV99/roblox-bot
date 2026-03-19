#!/usr/bin/env python3
import json
import logging
import time
import os
from config import Config
from roblox_api import RobloxAPI

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler()
        ]
    )

class RobloxBot:
    def __init__(self):
        self.target_ids = []
        self.accounts = []
    
    def load_targets(self):
        """Load target user IDs from file"""
        try:
            with open('targets.txt', 'r') as f:
                self.target_ids = [int(line.strip()) for line in f if line.strip()]
            logging.info(f"Loaded {len(self.target_ids)} target users")
        except Exception as e:
            logging.error(f"Error loading targets: {e}")
            self.target_ids = []
    
    def load_accounts(self):
        """Load accounts from JSON file"""
        try:
            with open(Config.ACCOUNTS_FILE, 'r') as f:
                self.accounts = json.load(f)
            logging.info(f"Loaded {len(self.accounts)} accounts")
        except Exception as e:
            logging.error(f"Error loading accounts: {e}")
            self.accounts = []
    
    def run(self):
        """Main bot execution"""
        self.load_targets()
        self.load_accounts()
        
        if not self.target_ids:
            logging.error("No targets loaded. Add user IDs to targets.txt")
            return
        
        if not self.accounts:
            logging.error("No accounts loaded. Add accounts to accounts.json")
            return
        
        logging.info(f"Starting bot with {len(self.accounts)} accounts and {len(self.target_ids)} targets")
        
        for acc in self.accounts:
            username = acc.get('username', 'Unknown')
            password = acc.get('password', '')
            roblosecurity = acc.get('roblosecurity', '')  # Optional cookie-based auth
            
            logging.info(f"Processing account: {username}")
            
            if roblosecurity:
                # Use cookie-based authentication
                api = RobloxAPI()
                logging.info(f"Using cookie authentication for {username}")
                result = api.batch_follow(
                    self.target_ids,
                    delay=Config.REQUEST_DELAY,
                    roblosecurity_cookie=roblosecurity
                )
                logging.info(f"Account {username} followed {result} users")
            else:
                # Use username/password authentication
                api = RobloxAPI()
                if api.authenticate(username, password):
                    logging.info(f"Authenticated as {username}, following targets...")
                    result = api.batch_follow(
                        self.target_ids,
                        delay=Config.REQUEST_DELAY
                    )
                    logging.info(f"Account {username} followed {result} users")
                else:
                    logging.error(f"Failed to authenticate {username}")
            
            # Respect rate limits between accounts
            time.sleep(Config.ACCOUNT_COOLDOWN)
        
        logging.info("Bot execution completed")

if __name__ == "__main__":
    setup_logging()
    bot = RobloxBot()
    bot.run()
