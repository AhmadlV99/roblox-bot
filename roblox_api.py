import requests
import time
import logging
from config import Config

logger = logging.getLogger(__name__)

class RobloxAPI:
    def __init__(self, username=None, password=None, proxies=None):
        self.session = requests.Session()
        self.headers = Config.get_headers()
        if proxies:
            self.session.proxies = proxies
    
    def authenticate(self, username, password):
        try:
            response = self.session.post(
                "https://auth.roblox.com/v2/login",
                json={"ctype": "Username", "cvalue": username, "password": password},
                headers=self.headers,
                timeout=30
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Auth error: {e}")
            return False
    
    def follow_user(self, user_id):
        url = f"{Config.BASE_URL}/users/{user_id}/follow"
        try:
            response = self.session.post(url, headers=self.headers, json={'userId': user_id})
            return response.status_code == 200
        except:
            return False
    
    def batch_follow(self, user_ids, delay=5):
        successful = 0
        for user_id in user_ids:
            if self.follow_user(user_id):
                successful += 1
            time.sleep(delay)
        return successful
