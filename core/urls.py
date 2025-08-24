from django.contrib import admin
from django.urls import path
from pro import views 

urlpatterns = [
    #rota,view responsavel, nome de referencia 
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('questionario/', views.questionario, name='questionario'),
    path('area/', views.area, name='area'),
    path('area/', views.area, name='area'),
    path('responder/', views.responder, name='responder'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('conclusaoform/', views.conclusaoform, name='conclusaoform'),
    path('dash/', views.dash, name='dash'),
    path('cadastrar/', views.cadastrar_colaborador, name='cadastrar_colaborador'),

    


    # path("dashboard/", views.dashboard, name="dashboard"),
    
]
