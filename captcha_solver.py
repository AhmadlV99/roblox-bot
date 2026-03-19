import os
from twocaptcha import TwoCaptcha
import logging

logger = logging.getLogger(__name__)

class CaptchaSolver:
    def __init__(self):
        self.api_key = os.getenv("CAPTCHA_API_KEY")
        if not self.api_key:
            logger.warning("CAPTCHA_API_KEY not set in environment variables")
            self.solver = None
        else:
            self.solver = TwoCaptcha(self.api_key)
    
    def solve_recaptcha_v2(self, site_key, page_url):
        """Solve reCAPTCHA v2 challenge"""
        if not self.solver:
            logger.error("Captcha solver not initialized - no API key")
            return None
        
        try:
            result = self.solver.recaptcha(
                sitekey=site_key,
                url=page_url,
                version="v2"
            )
            logger.info(f"Captcha solved successfully: {result['code'][:50]}...")
            return result['code']
        except Exception as e:
            logger.error(f"Failed to solve captcha: {e}")
            return None
