"""Search behavior implementation."""
import random
import logging
from typing import Any

class SearchBehavior:
    def __init__(self, page: Any, logger: logging.Logger):
        self.page = page
        self.logger = logger
        
    def perform_search(self, keyword: str) -> bool:
        """Perform a search with human-like typing."""
        try:
            # Wait for search box with increased timeout
            search_box = self.page.wait_for_selector(
                'textarea[name="q"], input[name="q"]',
                state="visible",
                timeout=10000
            )
            self.logger.info(f"Typing search term: {keyword}")
            
            # Click search box
            search_box.click(delay=random.randint(200, 400))
            self.page.wait_for_timeout(random.randint(300, 600))
            
            # Clear any existing text
            search_box.fill("")
            self.page.wait_for_timeout(random.randint(200, 400))
            
            # Type with natural delays
            for char in keyword:
                if char in [' ', '-', '_']:
                    self.page.wait_for_timeout(random.randint(200, 400))
                else:
                    self.page.wait_for_timeout(random.randint(50, 150))
                
                self.page.keyboard.type(char)
                
                if random.random() < 0.1:
                    self.page.wait_for_timeout(random.randint(400, 800))
            
            self.page.wait_for_timeout(random.randint(800, 1500))
            self.page.keyboard.press("Enter")
            
            # Wait for results with fallback selectors
            try:
                self.page.wait_for_selector('div#search', state="visible", timeout=10000)
            except Exception as e:
                self.logger.warning(f"Timeout waiting for #search, trying alternative selectors...")
                # Try alternative selectors if div#search is not found
                for selector in ['div#main', 'div#rso', 'div.g']:
                    try:
                        self.page.wait_for_selector(selector, state="visible", timeout=5000)
                        self.logger.info(f"Found results with alternative selector: {selector}")
                        break
                    except Exception:
                        continue
                else:
                    raise Exception("No search results found with any selector")

            self.page.wait_for_timeout(random.randint(1000, 2000))
            return True
            
        except Exception as e:
            self.logger.error(f"Search error: {str(e)}")
            return False