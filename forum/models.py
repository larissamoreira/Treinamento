from django.db import models

# Create your models here.


class Post(models.Model):
    titulo = models.CharField(max_length=1024, verbose_name="Título")
    conteudo = models.TextField(verbose_name="Conteúdo")
    usuario = models.ForeignKey(
        "auth.User", null=True, on_delete=models.SET_NULL, verbose_name="Usuário"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de criação"
    )

    def __str__(self):
        return f"{self.titulo} - {self.data_criacao}"


class Comment(models.Model):
    texto = models.TextField(verbose_name="Comentário")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Post")
    data = models.DateTimeField(auto_now_add=True, verbose_name="Data")
    usuario = models.ForeignKey(
        "auth.User", null=True, on_delete=models.SET_NULL, verbose_name="Usuário"
    )

