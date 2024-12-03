"""Main window implementation for the GUI."""
import customtkinter as ctk
import logging
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor
from bot.bot_manager import BotManager
from gui.components.header import create_header
from gui.components.input_form import create_input_form
from gui.components.status_panel import StatusPanel
from gui.theme import setup_theme

class MainWindow:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Bot Manager Pro")
        self.window.geometry("800x600")
        setup_theme()
        
        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        
        # Create components
        create_header(self.window)
        self.input_form = create_input_form(self.window, self.start_bots)
        self.input_form.on_stop = self.stop_bots
        self.status_panel = StatusPanel(self.window)
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging for the application."""
        logger = logging.getLogger('bot_app')
        logger.setLevel(logging.INFO)
        
    def start_bots(self, config: Dict[str, Any]):
        """Start bot operations with given configuration."""
        try:
            logging.info(f"Initializing bot manager with config: {config}")
            bot_manager = BotManager(config)
            self.current_bot_manager = bot_manager
            
            # Run bot manager in a separate thread
            self.executor = ThreadPoolExecutor(max_workers=1)
            self.executor.submit(bot_manager.run)
                
        except Exception as e:
            logging.error(f"Error starting bots: {str(e)}")
            
    def stop_bots(self):
        """Stop running bots."""
        if hasattr(self, 'current_bot_manager'):
            logging.info("Stopping all bots...")
            self.current_bot_manager.running = False
            if hasattr(self, 'executor'):
                self.executor.shutdown(wait=False)
            
    def run(self):
        """Start the GUI application."""
        self.window.mainloop()