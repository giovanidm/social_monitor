from .base_scraper import BaseSocialScraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import logging

class InstagramScraper(BaseSocialScraper):
    """Scraper específico para Instagram"""
    
    def __init__(self, headless=True, max_posts=100, wait_time=10):
        super().__init__(headless, max_posts, wait_time)
        self.driver = None
    
    def setup_driver(self):
        """Configura o webdriver para Instagram"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        return self.driver
    
    def authenticate(self, username: str, password: str):
        """
        Realiza login no Instagram
        
        :param username: Nome de usuário do Instagram
        :param password: Senha da conta
        """
        try:
            self.driver.get("https://www.instagram.com/accounts/login/")
            
            # Espera e preenche campos de login
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            username_input = self.driver.find_element(By.NAME, "username")
            password_input = self.driver.find_element(By.NAME, "password")
            
            username_input.send_keys(username)
            password_input.send_keys(password)
            
            # Submete o formulário
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Aguarda carregamento da página principal
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/direct/inbox/')]"))
            )
            
            return True
        except Exception as e:
            self.logger.error(f"Erro no login do Instagram: {e}")
            return False
    
    def extract_posts(self, profile_url: str):
        """
        Extrai posts de um perfil do Instagram
        
        :param profile_url: URL do perfil
        :return: Lista de posts
        """
        posts = []
        try:
            self.driver.get(profile_url)
            
            # Rola a página para carregar mais posts
            for _ in range(5):
                self.driver.execute_script("window.scroll")

                