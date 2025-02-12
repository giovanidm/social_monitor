# celery_app.py
import os
from celery import Celery
from django.conf import settings

# Define a configuração padrão do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_monitor.settings')

# Cria a instância do aplicativo Celery
app = Celery('social_monitor')

# Usa a configuração do Django para configurar o Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carrega tarefas de todos os apps registrados no Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Tarefa de debug para verificar configuração do Celery"""
    print(f'Request: {self.request!r}')

# Tarefas de coleta de dados para redes sociais
@app.task
def collect_instagram_posts(profile_url):
    """
    Tarefa assíncrona para coletar posts do Instagram
    
    :param profile_url: URL do perfil do Instagram
    """
    from apps.social_scraper.instagram_scraper import InstagramScraper
    
    scraper = InstagramScraper()
    try:
        scraper.setup_driver()
        # Lógica de autenticação e coleta de posts
        posts = scraper.extract_posts(profile_url)
        return posts
    except Exception as e:
        # Registra erros de coleta
        print(f"Erro na coleta de posts do Instagram: {e}")
    finally:
        if scraper.driver:
            scraper.driver.quit()

@app.task
def analyze_collected_posts(posts):
    """
    Tarefa para análise de posts coletados
    
    :param posts: Lista de posts para análise
    """
    from apps.data_analysis.analysis import generate_post_analysis
    
    analysis_results = generate_post_analysis(posts)
    return analysis_results

# Tarefa periódica de monitoramento
@app.task
def periodic_social_media_monitoring():
    """
    Tarefa periódica para monitorar perfis e palavras-chave
    """
    from apps.core.models import MonitoredProfile, KeywordMonitor
    
    # Busca perfis ativos para monitoramento
    active_profiles = MonitoredProfile.objects.filter(is_active=True)
    keywords = KeywordMonitor.objects.filter(is_active=True)
    
    for profile in active_profiles:
        # Coleta de posts para cada perfil
        collect_instagram_posts.delay(profile.profile_url)
    
    return f"Monitoramento concluído para {len(active_profiles)} perfis"

