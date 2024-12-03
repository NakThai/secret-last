"""Individual bot instance implementation."""
from typing import Optional
import random
import logging
import time
from playwright.sync_api import sync_playwright
from utils.fingerprint_masking import FingerprintMasker
from .behaviors.competitor_visitor import CompetitorVisitor
from .behaviors.site_navigator import SiteNavigator
from .behaviors.search_behavior import SearchBehavior

class BotInstance:
    def __init__(
        self,
        keyword: str,
        target_site: str,
        proxy: Optional[str] = None,
        use_france_gps: bool = False,
        google_domain: str = "google.fr",
        visit_competitors: bool = False,
        competitors_count: int = 0,
        pages_to_visit: int = 3,
        config: dict = None,
        min_type_delay: int = 100,
        max_type_delay: int = 300
    ):
        self.keyword = keyword
        self.target_site = target_site
        self.proxy = proxy
        self.use_france_gps = use_france_gps
        self.google_domain = google_domain
        self.visit_competitors = visit_competitors
        self.competitors_count = competitors_count
        self.pages_to_visit = pages_to_visit
        self.time_on_site = (config.get('time_on_site', 30) if config else 30) * 1000  # Convert to milliseconds
        self.min_type_delay = min_type_delay
        self.max_type_delay = max_type_delay
        self.logger = logging.getLogger(f'bot.{id(self)}')

    def run(self):
        """Execute bot operations."""
        try:
            with sync_playwright() as playwright:
                # Launch browser with specific configurations
                browser = playwright.chromium.launch(
                    headless=False,
                    args=[
                        '--no-sandbox',
                        '--start-maximized'
                    ]
                )
                
                # Create context with specific settings
                # Set language based on domain
                browser_language = "fr-FR" if self.google_domain == "google.fr" else "de-DE"
                
                # Set language based on domain
                browser_language = "fr-FR" if self.google_domain == "google.fr" else "de-DE"
                
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                    proxy={"server": self.proxy} if self.proxy else None,
                    proxy={"server": self.proxy} if self.proxy else None,
                    locale=browser_language
                )
                
                if self.use_france_gps:
                    context.set_geolocation({"latitude": 48.8566, "longitude": 2.3522})
                    context.grant_permissions(['geolocation'])
                
                page = context.new_page()

                # Initialize behaviors
                self.search_behavior = SearchBehavior(page, self.logger)
                self.competitor_visitor = CompetitorVisitor(page, self.logger)
                self.site_navigator = SiteNavigator(page, self.logger)

                FingerprintMasker(page).apply_masks()
                
                # Aller sur Google
                self.logger.info("Accès à Google...")
                page.goto(f"https://www.{self.google_domain}")
                page.wait_for_load_state("networkidle")
                
                # Handle cookie popup
                try:
                    # Attendre que le popup soit visible
                    time.sleep(3)  # Utiliser time.sleep au lieu de wait_for_timeout
                    
                    # Essayer différents sélecteurs dans l'ordre
                    selectors = [
                        'button:has-text("Tout accepter")',
                        'button[aria-label="Tout accepter"]',
                        '[aria-modal="true"] button:has-text("Tout accepter")',
                        '[aria-modal="true"] button:has-text("Alle akzeptieren")',
                        'form button:has-text("Tout accepter")',
                        'form button:has-text("Alle akzeptieren")',
                        'div[role="dialog"] button:has-text("Tout accepter")',
                        'div[role="dialog"] button:has-text("Alle akzeptieren")'
                    ]
                    
                    accept_button = None
                    for selector in selectors:
                        try:
                            accept_button = page.wait_for_selector(
                                selector,
                                state="visible",
                                timeout=2000
                            )
                            if accept_button:
                                break
                        except Exception:
                            continue
                            
                    if accept_button:
                        self.logger.info("Bouton de cookies trouvé, tentative de clic...")
                        # Attendre un peu avant de cliquer
                        page.wait_for_timeout(random.randint(500, 1000))
                        accept_button.click(delay=random.randint(200, 500))
                        page.wait_for_timeout(random.randint(2000, 3000))
                        self.logger.info("Cookies acceptés avec succès")
                    else:
                        self.logger.info("Aucun bouton de cookies trouvé")
                except Exception as e:
                    self.logger.warning(f"Erreur lors de la gestion des cookies: {str(e)}")
                    # Continuer même si on n'arrive pas à gérer les cookies

                # Perform search
                self.logger.info(f"Recherche du mot-clé: {self.keyword}")
                if not self.search_behavior.perform_search(self.keyword):
                    self.logger.error("Search failed")
                    raise
                
                # Attendre les résultats de recherche
                page.wait_for_selector('div#search', state="visible", timeout=10000)
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(random.randint(1000, 2000))

                # Visit competitors if enabled
                if self.visit_competitors and self.competitors_count > 0:
                    self.competitor_visitor.visit_competitors(self.competitors_count)
                
                # Rechercher le site cible dans les pages de résultats
                site_found = False
                current_page = 1
                max_pages = 10
                
                while current_page <= max_pages and not site_found:
                    self.logger.info(f"Recherche dans la page {current_page} des résultats")
                    
                    # Scroll aléatoire dans la page courante
                    for _ in range(random.randint(3, 6)):
                        page.mouse.wheel(0, random.randint(100, 300))
                        page.wait_for_timeout(random.randint(800, 2000))
                    
                    # Chercher uniquement dans les résultats organiques
                    links = page.locator('div#search div.g a[href*="' + self.target_site + '"]')
                    
                    if links.count() > 0:
                        self.logger.info(f"Site cible trouvé sur la page {current_page}: {self.target_site}")
                        links.first.scroll_into_view_if_needed()
                        page.wait_for_timeout(random.randint(1000, 2000))
                        links.first.click()
                        page.wait_for_load_state("networkidle")
                        site_found = True
                        
                        # Navigation sur le site cible
                        self.site_navigator.navigate_site(self.time_on_site, self.pages_to_visit)
                    else:
                        # Passer à la page suivante si disponible
                        next_button = page.locator('a#pnnext')
                        if next_button.count() > 0:
                            self.logger.info(f"Passage à la page {current_page + 1}")
                            next_button.first.click()
                            page.wait_for_load_state("networkidle")
                            page.wait_for_timeout(random.randint(2000, 4000))
                            current_page += 1
                        else:
                            self.logger.error(f"Site cible non trouvé après {current_page} pages")
                            break
                
                if not site_found:
                    self.logger.error(f"Site cible non trouvé dans les {max_pages} premières pages")
                
                # Cleanup
                self.logger.info("Fermeture du navigateur...")
                context.close()
                browser.close()
                
        except Exception as e:
            self.logger.error(f"Bot error: {str(e)}")