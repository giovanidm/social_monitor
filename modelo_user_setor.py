from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class Sector(models.Model):
    """
    Modelo para representar setores/departamentos da organização
    """
    name = models.CharField(_('Nome do Setor'), max_length=100, unique=True)
    description = models.TextField(_('Descrição'), blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Setor')
        verbose_name_plural = _('Setores')
        ordering = ['name']

class CustomUser(AbstractUser):
    """
    Modelo customizado de usuário com informações adicionais
    """
    # Validador de telefone
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message=_("Número de telefone deve ser inserido no formato: '+999999999'. Até 15 dígitos permitidos.")
    )
    
    # Campos adicionais
    full_name = models.CharField(
        _('Nome Completo'), 
        max_length=255, 
        blank=False, 
        null=False
    )
    
    email = models.EmailField(
        _('Endereço de E-mail'), 
        unique=True, 
        blank=False, 
        null=False
    )
    
    phone = models.CharField(
        _('Telefone'), 
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        null=True
    )
    
    sector = models.ForeignKey(
        Sector, 
        on_delete=models.SET_NULL, 
        verbose_name=_('Setor'), 
        related_name='users',
        blank=True, 
        null=True
    )
    
    # Campo para controle adicional
    is_active = models.BooleanField(
        _('Ativo'), 
        default=True,
        help_text=_('Designa se o usuário está ativo no sistema.')
    )
    
    # Campo para rastreamento
    created_at = models.DateTimeField(
        _('Data de Criação'), 
        auto_now_add=True
    )
    
    # Campos obrigatórios para substituir o usuário padrão do Django
    REQUIRED_FIELDS = ['email', 'full_name']
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')
        ordering = ['full_name']

        