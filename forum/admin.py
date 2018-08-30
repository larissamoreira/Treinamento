from django.contrib import admin

# Register your models here.

from forum import models
from django.forms import HiddenInput

admin.site.register(models.Comment)

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_criacao', 'usuario')
    # list_filter = ('usuario', ) # não precisa filtrar por usuário já que tá mostrando os posts só de um.
    search_fields = ('titulo', 'conteudo')
    date_hierarchy = 'data_criacao'

    def get_form(self, request, *args, **kwargs): # vai mostrar só o usuário logado
        form = super().get_form(request, *args, **kwargs)
        qs = form.base_fields['usuario'].queryset
        form.base_fields['usuario'].queryset = qs.filter(id=request.user.id)
        form.base_fields['usuario'].widget = HiddenInput()
        return form
        
    def get_changeform_initial_data(self, request): # o usuário logado já vai vir selecionado
        return {'usuario': request.user}

    def has_change_permission(self, request, obj=None):
        perm = super().has_change_permission(request, obj)
        if obj:
            return perm and obj.usuario == request.user
        return perm
    
    def has_delete_permission(self, request, obj=None):
        perm = super().has_delete_permission(request, obj)
        if obj:
            return perm and obj.usuario == request.user
        return perm
    
    def get_actions(self, request):
        return []

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['usuario']
        return []
    
    def get_queryset(self, request): # define qual lista de objetos o usuario vai ver
        qs = super().get_queryset(request) # retorna todos os elementos posts
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario = request.user.id)
