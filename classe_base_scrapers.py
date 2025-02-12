import abc
import logging
from typing import List, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import pandas as pd
from .models import SocialPost, SocialComment, KeywordMonitor

class BaseSocialScraper(abc.ABC):
    """Classe base abstrata para scrapers de redes sociais"""
    
    def __init__(self, 
                 headless: bool = True, 
                 max_posts: int = 100, 
                 wait_time: int = 10):
        """
        Inicializa o scraper base
        
        :param headless: Executa o navegador em modo headless
        :param max_posts: Número máximo de posts para coletar
        :param wait_time: Tempo máximo de espera para carregar elementos
        """
        self.headless = headless
        self.max_posts = max_posts
        self.wait_time = wait_time
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @abc.abstractmethod
    def setup_driver(self):
        """Configura o webdriver específico para cada plataforma"""
        pass
    
    @abc.abstractmethod
    def authenticate(self, username: str, password: str):
        """Realiza autenticação na plataforma"""
        pass
    
    @abc.abstractmethod
    def extract_posts(self, profile_url: str) -> List[Dict[str, Any]]:
        """
        Extrai posts de um perfil específico
        
        :param profile_url: URL do perfil a ser coletado
        :return: Lista de dicionários com informações dos posts
        """
        pass
    
    @abc.abstractmethod
    def extract_comments(self, post_url: str) -> List[Dict[str, Any]]:
        """
        Extrai comentários de uma publicação específica
        
        :param post_url: URL da publicação
        :return: Lista de dicionários com informações dos comentários
        """
        pass
    
    def check_keywords(self, post_content: str, keywords: List[KeywordMonitor]) -> List[KeywordMonitor]:
        """
        Verifica se o post contém palavras-chave monitoradas
        
        :param post_content: Conteúdo do post
        :param keywords: Lista de palavras-chave a verificar
        :return: Lista de palavras-chave encontradas
        """
        matched_keywords = []
        for keyword in keywords:
            if keyword.keyword.lower() in post_content.lower():
                matched_keywords.append(keyword)
        return matched_keywords
    
    def save_post(self, post_data: Dict[str, Any], 
                  profile, 
                  keywords: List[KeywordMonitor] = None) -> SocialPost:
        """
        Salva um post no banco de dados
        
        :param post_data: Dicionário com dados do post
        :param profile: Perfil associado ao post
        :param keywords: Lista de palavras-chave
        :return: Instância do post salvo
        """
        try:
            # Verifica se o post já existe
            social_post, created = SocialPost.objects.get_or_create(
                platform=post_data['platform'],
                post_id=post_data['post_id'],
                defaults={
                    'profile': profile,
                    'content': post_data['content'],
                    'published_at': post_data['published_at'],
                    'likes_count': post_data.get('likes_count', 0),
                    'shares_count': post_data.get('shares_count', 0)
                }
            )
            
            # Verifica palavras-chave se fornecidas
            if keywords:
                matched_kw = self.check_keywords(post_data['content'], keywords)
                if matched_kw:
                    social_post.contains_keywords = True
                    social_post.save()
                    social_post.matched_keywords.set(matched_kw)
            
            return social_post
        except Exception as e:
            self.logger.error(f"Erro ao salvar post: {e}")
            return None
    
    def save_comments(self, social_post: SocialPost, 
                      comments: List[Dict[str, Any]]):
        """
        Salva comentários associados a um post
        
        :param social_post: Post ao qual os comentários pertencem
        :param comments: Lista de comentários
        """
        for comment_data in comments:
            try:
                SocialComment.objects.get_or_create(
                    post=social_post,
                    comment_id=comment_data['comment_id'],
                    defaults={
                        'author_username': comment_data['author_username'],
                        'content': comment_data['content'],
                        'commented_at': comment_data['commented_at'],
                        'likes_count': comment_data.get('likes_count', 0)
                    }
                )
            except Exception as e:
                self.logger.error(f"Erro ao salvar comentário: {e}")
    
    def generate_analysis_report(self, posts: List[SocialPost]) -> pd.DataFrame:
        """
        Gera relatório de análise a partir dos posts coletados
        
        :param posts: Lista de posts
        :return: DataFrame com análise dos posts
        """
        data = []
        for post in posts:
            data.append({
                'platform': post.platform,
                'profile': post.profile.username,
                'published_at': post.published_at,
                'likes_count': post.likes_count,
                'shares_count': post.shares_count,
                'contains_keywords': post.contains_keywords,
                'comment_count': post.comments.count()
            })
        
        return pd.DataFrame(data)


        