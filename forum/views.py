from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils.timezone import now
from django.views import generic
from forum import models, forms
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
# Create your views here.


class Index(generic.ListView):
    template_name = 'index.html'
    model = models.Post
    context_object_name = 'posts'  # object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Fórum bugado'
        return context


# class PostView(generic.DetailView):
#     template_name = 'ver_post.html'
#     model = models.Post
#     context_object_name = 'post'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['titulo'] = self.get_object().titulo
#         return context

def ver_post(request, pk):
    post = get_object_or_404(models.Post, pk=pk)

    if request.method == 'POST':
        dados = request.POST
    else:
        dados = None

    form = forms.CommentForm(dados, initial={'usuario': request.user.id, 'post': post})
    form.fields['usuario'].queryset = User.objects.filter(id=request.user.id)
    form.fields['post'].queryset = models.Post.objects.filter(id=post.id)
    if form.is_valid():
        form.save()

    return render(request, 'ver_post.html', {'post': post, 'titulo': post.titulo, 'form': form})

@login_required
def editar_comentario(request, pk):
    comentario = get_object_or_404(models.Comment, pk=pk)
    if comentario.usuario != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        dados = request.POST
    else:
        dados = None

    form = forms.CommentForm(dados, instance = comentario, initial={'usuario': request.user.id, 'post': comentario.post})
    form.fields['usuario'].queryset = User.objects.filter(id=request.user.id)
    form.fields['post'].queryset = models.Post.objects.filter(id=comentario.post.id)
    if form.is_valid():
        form.save()
        return redirect('ver_post', pk = comentario.post.id)

    return render(request, 'editar_comentario.html', {'form': form})

def deletar_comentario(request, pk):
    comentario = get_object_or_404(models.Comment, pk=pk)
    id_post = comentario.post.id
    if request.user != comentario.usuario:
        raise PermissionDenied
    if request.method == 'POST':
        comentario.delete()
    
    return redirect('ver_post', pk = id_post)

@login_required
def editar_post(request, pk=None):
    if pk:
        post = get_object_or_404(models.Post, pk=pk)
        if post.usuario != request.user:
            raise PermissionDenied
    else:
        post = None

    if request.method == 'GET':
        dados = None
    elif request.method == 'POST':
        dados = request.POST

    form = forms.PostForm(dados, instance=post)
    form.fields['usuario'].queryset = User.objects.filter(id=request.user.id)
    if form.is_valid():
        form.save()
        return redirect('index')

    return render(request, 'novo_post.html', {'form': form})
