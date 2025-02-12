from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SocialNetwork(models.Model):
    """Modelo para representar diferentes redes sociais"""
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField()

    def __str__(self):
        return self.name

class MonitoredProfile(models.Model):
    """Perfis de redes sociais a serem monitorados"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monitored_profiles')
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    profile_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('social_network', 'username')

    def __str__(self):
        return f"{self.username} - {self.social_network.name}"

class KeywordMonitor(models.Model):
    """Palavras-chave para monitoramento"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='keywords')
    keyword = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword

class SocialPost(models.Model):
    """Modelo para armazenar publicações coletadas"""
    PLATFORM_CHOICES = [
        ('INSTAGRAM', 'Instagram'),
        ('TWITTER', 'Twitter/X'),
        ('FACEBOOK', 'Facebook'),
        ('THREADS', 'Threads'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    profile = models.ForeignKey(MonitoredProfile, on_delete=models.CASCADE, related_name='posts')
    post_id = models.CharField(max_length=300)
    content = models.TextField()
    published_at = models.DateTimeField()
    likes_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    
    # Flag para posts que contêm palavras-chave monitoradas
    contains_keywords = models.BooleanField(default=False)
    matched_keywords = models.ManyToManyField(KeywordMonitor, blank=True)

    class Meta:
        unique_together = ('platform', 'post_id')
        ordering = ['-published_at']

class SocialComment(models.Model):
    """Modelo para armazenar comentários coletados"""
    post = models.ForeignKey(SocialPost, on_delete=models.CASCADE, related_name='comments')
    comment_id = models.CharField(max_length=300)
    author_username = models.CharField(max_length=200)
    content = models.TextField()
    commented_at = models.DateTimeField()
    likes_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('post', 'comment_id')
        ordering = ['-commented_at']

class UserMention(models.Model):
    """Modelo para armazenar marcações de usuários"""
    post = models.ForeignKey(SocialPost, on_delete=models.CASCADE, related_name='mentions')
    mentioned_profile = models.CharField(max_length=200)
    mentioned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'mentioned_profile')

        