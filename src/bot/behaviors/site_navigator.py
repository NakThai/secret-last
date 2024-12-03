"""Site navigation behavior."""
import random
import random
import logging
from typing import Any

class SiteNavigator:
    def __init__(self, page: Any, logger: logging.Logger):
        self.page = page
        self.logger = logger

    def navigate_site(self, time_on_site: int, pages_to_visit: int):
        """Navigate through the site naturally."""
        self.logger.info("Navigation sur le site...")
        total_scroll_time = 0
        max_time_on_site = time_on_site * 1000
                    
        for _ in range(pages_to_visit):
            wait_time = random.randint(2000, 4000)
            self.page.wait_for_timeout(wait_time)
            total_scroll_time += wait_time
                    
            # Natural scrolling with pauses
            scroll_height = self.page.evaluate("() => document.body.scrollHeight")
            viewed_height = 0
            
            while viewed_height < scroll_height and total_scroll_time < max_time_on_site:
                scroll_amount = random.randint(100, 300)
                self.page.mouse.wheel(0, scroll_amount)
                viewed_height += scroll_amount
                        
                if random.random() < 0.3:
                    wait_time = random.randint(800, 1500)
                    self.page.wait_for_timeout(wait_time)
                    total_scroll_time += wait_time
            if total_scroll_time >= max_time_on_site:
                self.logger.info("Temps maximum atteint sur le site")