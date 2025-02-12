from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Sector

class UserRegistrationForm(UserCreationForm):
    """
    Formulário para registro de novos usuários
    """
    sector = forms.ModelChoiceField(
        queryset=Sector.objects.all(), 
        required=False, 
        label='Setor'
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 
            'full_name', 
            'email', 
            'phone', 
            'sector', 
            'password1', 
            'password2'
        ]
    
    def clean_email(self):
        """
        Validação de e-mail único
        """
        email = self.cleaned_data['email']
        
        # Verifica se já existe um usuário com este e-mail
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Um usuário com este e-mail já está cadastrado.")
        
        return email
    
    def save(self, commit=True):
        """
        Salva o usuário com informações adicionais
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        
        if commit:
            user.save()
        
        return user

class UserUpdateForm(UserChangeForm):
    """
    Formulário para atualização de usuários
    """
    sector = forms.ModelChoiceField(
        queryset=Sector.objects.all(), 
        required=False, 
        label='Setor'
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 
            'full_name', 
            'email', 
            'phone', 
            'sector', 
            'is_active'
        ]
    
    def clean_email(self):
        """
        Validação de e-mail único, excluindo o usuário atual
        """
        email = self.cleaned_data['email']
        
        # Verifica se já existe um usuário com este e-mail, 
        # excluindo o usuário atual
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("Um usuário com este e-mail já está cadastrado.")
        
        return email

class SectorForm(forms.ModelForm):
    """
    Formulário para criação e edição de setores
    """
    class Meta:
        model = Sector
        fields = ['name', 'description']
        labels = {
            'name': 'Nome do Setor',
            'description': 'Descrição'
        }