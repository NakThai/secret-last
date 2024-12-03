"""Competitor site visiting behavior."""
import random
import random
import logging
from typing import Any

class CompetitorVisitor:
    def __init__(self, page: Any, logger: logging.Logger):
        self.page = page
        self.logger = logger
        self.keyword = ""  # Will be set during visit

    def visit_competitors(self, count: int):
        """Visit competitor sites before target site."""
        try:
            # Attendre que les résultats soient chargés
            self.page.wait_for_selector('div#search', state="visible", timeout=10000)
            self.page.wait_for_timeout(random.randint(1000, 2000))

            # Trouver tous les résultats organiques
            organic_results = self.page.locator('div#search div.g:not([data-hveid*="CAA"]) a[href^="http"]')
            visited_count = 0
            
            for i in range(organic_results.count()):
                if visited_count >= count:
                    break
                    
                link = organic_results.nth(i)
                href = link.get_attribute("href")
                
                if href:
                    self.logger.info(f"Visite du concurrent {visited_count + 1}: {href}")
                    self._visit_competitor_site(link)
                    visited_count += 1
                    
            self.logger.info(f"Visite de {visited_count} sites concurrents terminée")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la visite des concurrents: {str(e)}")

    def _visit_competitor_site(self, link: Any):
        """Visit a single competitor site with natural behavior."""
        try:
            # Scroll to link
            link.scroll_into_view_if_needed()
            self.page.wait_for_timeout(random.randint(800, 1500))
            
            # Click and wait for load
            link.click()
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            
            # Natural scrolling behavior
            visit_time = random.randint(8000, 15000)
            start_time = self.page.evaluate("() => Date.now()")
            elapsed = 0
            
            while elapsed < visit_time:
                self.page.mouse.wheel(0, random.randint(100, 300))
                self.page.wait_for_timeout(random.randint(200, 400))
                
                if random.random() < 0.3:
                    self.page.wait_for_timeout(random.randint(800, 1500))
                
                elapsed = self.page.evaluate("() => Date.now()") - start_time
                
            # Return to search results
            self.page.go_back()
            self.page.wait_for_selector('div#search', state="visible", timeout=5000)
            self.page.wait_for_timeout(random.randint(2000, 4000))
            
        except Exception as e:
            self.logger.warning(f"Erreur pendant la visite: {str(e)}")
            # Retour à la recherche si nécessaire
            self.page.goto(f"https://www.google.fr/search?q={self.keyword}")
            self.page.wait_for_selector('div#search', state="visible", timeout=5000)
            self.page.wait_for_timeout(random.randint(1000, 2000))