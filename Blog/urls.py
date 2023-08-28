from django.urls import path
from .views import *



urlpatterns = [
    path('', index, name='index'),
    path('registro/', UsuarioCreateView.as_view(), name='registro'),
    path('login/', login_views, name='login'),
    path('logout/', logout_views, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('editUser/', edit_user, name='editUser'),
    path('createPost/', PostCreateView.as_view(), name='createPost'),
]