from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.user_detail, name='user-detail'),
    path('random/', views.random_user, name='random-user'),
    path('', views.index, name='index'),
]
