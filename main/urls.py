from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('agentes/<int:agent_id>/', views.agente, name = 'agente'),
    path('ajax_calls/search/', views.autocompleteModel, name='search'),
    path('agente/remove/<int:agent_id>', views.remove, name='remove'),
    path('login', views.user_login, name = 'user_login'),
    path('news',views.news, name = 'news'),
    path('registro', views.register, name = 'register'),
    path('gerarRelatorio/<int:agent_id>/', views.gerarRelatorio, name = 'gerar'),
    path('gerarRelatorio/', views.gerarRelatorioGlobal, name = 'gerarG'),
    path('newagent', views.newagent, name='newagent'),
    path('shazam/<int:crawler_id>', views.crawler, name='crawler'),
    path('play', views.play, name = 'play'),
    path('newhome', views.newhome, name = 'newhome'),
    path('updatehome', views.updateHome, name="update"),
    path('info', views.info, name = 'info'),
]
