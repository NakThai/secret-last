"""Bot manager for handling multiple bot instances."""
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any
from bot.bot_instance import BotInstance
class BotManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger('bot_app.manager')
        self.running = True
        
    def run(self):
        """Run multiple bots concurrently."""
        with ThreadPoolExecutor(max_workers=self.config['bot_count']) as executor:
            bot_count = self.config['bot_count']
            self.logger.info(f"Starting {bot_count} bots...")
            
            futures = []            
            for i in range(bot_count):
                proxy = None
                if self.config.get('use_proxies'):
                    proxies = self.config.get('proxies', [])
                    if proxies:
                        proxy = proxies[i % len(proxies)]
                
                self.logger.info(f"Initializing bot {i+1}/{bot_count}")
                bot = BotInstance(
                    keyword=self.config['keyword'],
                    target_site=self.config['target_site'],
                    proxy=proxy,
                    use_france_gps=self.config.get('use_france_gps', False),
                    google_domain=self.config.get('google_domain', 'google.fr'),
                    visit_competitors=self.config.get('visit_competitors', False),
                    competitors_count=self.config.get('competitors_count', 0),
                    pages_to_visit=self.config.get('pages_to_visit', 3),
                    config=self.config  # Pass the entire config for additional settings
                )
                futures.append(executor.submit(bot.run))
            
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    self.logger.error(f"Bot execution error: {str(e)}")
                if not self.running:
                    self.logger.info("Stop signal received, terminating bots...")