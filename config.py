import os

class Config:
    BASE_URL = "https://friends.roblox.com/v1"
    AUTH_URL = "https://auth.roblox.com/v2/login"
    MAX_FOLLOWS_PER_HOUR = 50
    REQUEST_DELAY = 3  # Reduced delay for faster following
    ACCOUNT_COOLDOWN = 60
    CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY", "")
    PROXY_FILE = "proxies.txt"
    ACCOUNTS_FILE = "accounts.json"
    USER_AGENT = "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36"
    LOG_FILE = "bot.log"
    
    @classmethod
    def get_headers(cls, csrf_token=None):
        headers = {
            "User-Agent": cls.USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if csrf_token:
            headers["X-CSRF-TOKEN"] = csrf_token
        return headers
