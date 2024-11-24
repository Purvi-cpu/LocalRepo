from django.urls import path
from . import views

urlpatterns = [
    path('home', views.upload_image, name='upload_image'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]