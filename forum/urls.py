from django.conf.urls import url
from forum import views

urlpatterns = [
    url(r'^index$', views.Index.as_view(), name='index'),
    url(r'^post/(?P<pk>\d+)/$', views.ver_post, name='ver_post'),
    url(r'^novo_post/$', views.editar_post, name='novo_post'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.editar_post, name='editar_post'),
    url(r'^comment/(?P<pk>\d+)/edit/$', views.editar_comentario, name="editar_comentario"),
    url(r'^comment/(?P<pk>\d+)/delete/$', views.deletar_comentario, name="deletar_comentario")
]