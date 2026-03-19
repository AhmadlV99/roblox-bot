import os

class Config:
    BASE_URL = "https://friends.roblox.com/v1"
    MAX_FOLLOWS_PER_HOUR = 50
    REQUEST_DELAY = 5
    ACCOUNT_COOLDOWN = 60
    CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY", "")
    PROXY_FILE = "proxies.txt"
    ACCOUNTS_FILE = "accounts.json"
    USER_AGENT = "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36"
    LOG_FILE = "bot.log"
    
    @classmethod
    def get_headers(cls):
        return {
            "User-Agent": cls.USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": "https://www.roblox.com",
            "Referer": "https://www.roblox.com/"
        }
