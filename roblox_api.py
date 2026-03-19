import requests
import time
import logging
import json
from config import Config
from captcha_solver import CaptchaSolver

logger = logging.getLogger(__name__)

class RobloxAPI:
    def __init__(self, proxies=None):
        self.session = requests.Session()
        self.headers = Config.get_headers()
        self.csrf_token = None
        self.proxies = proxies
        self.captcha_solver = CaptchaSolver()
        if proxies:
            self.session.proxies = proxies
    
    def get_csrf_token(self):
        """Get CSRF token from Roblox"""
        try:
            # First request to get CSRF token
            response = self.session.post(
                "https://auth.roblox.com/v2/logout",
                headers=self.headers
            )
            if "x-csrf-token" in response.headers:
                self.csrf_token = response.headers["x-csrf-token"]
                logger.info("CSRF token obtained successfully")
                return True
        except Exception as e:
            logger.error(f"Failed to get CSRF token: {e}")
        return False
    
    def authenticate(self, username, password):
        """Authenticate with Roblox"""
        if not self.get_csrf_token():
            logger.error("Could not obtain CSRF token")
            return False
        
        # Update headers with CSRF token
        self.headers = Config.get_headers(self.csrf_token)
        
        try:
            # Login request
            payload = {
                "ctype": "Username",
                "cvalue": username,
                "password": password
            }
            
            response = self.session.post(
                Config.AUTH_URL,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                # Check if account data is in response
                if 'userId' in response.text:
                    logger.info(f"Successfully authenticated as {username}")
                    return True
            elif response.status_code == 403:
                # Handle CAPTCHA requirement
                logger.warning(f"CAPTCHA required for {username}")
                return self.handle_captcha_login(username, password)
            else:
                logger.error(f"Login failed for {username}: Status {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Auth error for {username}: {e}")
            return False
        
        return False
    
    def handle_captcha_login(self, username, password):
        """Handle login with CAPTCHA solving"""
        # This is a simplified version - actual implementation would need
        # to extract sitekey and page_url from Roblox's response
        logger.info(f"Attempting CAPTCHA solve for {username}")
        
        # Note: Roblox CAPTCHA solving requires extracting the sitekey
        # from the response and using 2captcha to solve it
        # This is a placeholder for the actual implementation
        return False
    
    def follow_user(self, user_id, roblosecurity_cookie=None):
        """Follow a user on Roblox"""
        url = f"{Config.BASE_URL}/users/{user_id}/follow"
        
        # Update headers for follow request
        follow_headers = Config.get_headers(self.csrf_token)
        if roblosecurity_cookie:
            follow_headers["Cookie"] = f".ROBLOSECURITY={roblosecurity_cookie}"
        
        try:
            response = self.session.post(
                url,
                headers=follow_headers,
                json={'userId': user_id},
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Successfully followed user {user_id}")
                return True
            elif response.status_code == 429:
                logger.warning(f"Rate limited for user {user_id}")
                return False
            else:
                logger.warning(f"Failed to follow user {user_id}: Status {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error following user {user_id}: {e}")
            return False
    
    def batch_follow(self, user_ids, delay=3, roblosecurity_cookie=None):
        """Follow multiple users with delay"""
        successful = 0
        for user_id in user_ids:
            if self.follow_user(user_id, roblosecurity_cookie):
                successful += 1
            time.sleep(delay)
        return successful
