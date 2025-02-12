from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    PermissionRequiredMixin
)
from django.urls import reverse_lazy

from .models import CustomUser, Sector
from .forms import (
    UserRegistrationForm, 
    UserUpdateForm, 
    SectorForm
)

# Views baseadas em função para usuários
@login_required
@permission_required('core.add_customuser', raise_exception=True)
def user_create(request):
    """
    View para criação de novo usuário
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuário {user.full_name} criado com sucesso!')
            return redirect('user_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/user_form.html', {'form': form})

@login_required
@permission_required('core.view_customuser', raise_exception=True)
def user_list(request):
    """
    View para listar usuários
    """
    users = CustomUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@login_required
@permission_required('core.change_customuser', raise_exception=True)
def user_update(request, pk):
    """
    View para atualização de usuário
    """
    user = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuário {user.full_name} atualizado com sucesso!')
            return redirect('user_list')
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, 'users/user_form.html', {'form': form})

@login_required
@permission_required('core.delete_customuser', raise_exception=True)
def user_delete(request, pk):
    """
    View para exclusão de usuário
    """
    user = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'Usuário {user.full_name} excluído com sucesso!')
        return redirect('user_list')
    
    return render(request, 'users/user_confirm_delete.html', {'user': user})

# Views baseadas em classe para setores
class SectorListView(LoginRequiredMixin, ListView):
    """
    View para listar setores
    """
    model = Sector
    template_name = 'users/sector_list.html'
    context_object_name = 'sectors'

class SectorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    View para criação de setor
    """
    model = Sector
    form_class = SectorForm
    template_name = 'users/sector_form.html'
    success_url = reverse_lazy('sector_list')
    permission_required = 'core.add_sector'

    def form_valid(self, form):
        messages.success(self.request, 'Setor criado com sucesso!')
        return super().form_valid(form)

class SectorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    View para atualização de setor
    """
    model = Sector
    form_class = SectorForm
    template_name = 'users/sector_form.html'
    success_url = reverse_lazy('sector_list')
    permission_required = 'core.change_sector'

    def form_valid(self, form):
        messages.success(self.request, 'Setor atualizado com sucesso!')
        return super().form_valid(form)

class SectorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    View para exclusão de setor
    """
    model = Sector
    template_name = 'users/sector_confirm_delete.html'
    success_url = reverse_lazy('sector_list')
    permission_required = 'core.delete_sector'

    def form_valid(self, form):
        messages.success(self.request, 'Setor excluído com sucesso!')
        return super().form_valid(form)
    