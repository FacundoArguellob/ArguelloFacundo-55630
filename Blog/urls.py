from django.urls import path
from .views      import *

urlpatterns = [
    #Login, Registro, Index, Sobre mi
    path('login/', login_views, name='login'),
    path('registro/', UsuarioCreateView.as_view(), name='registro'),
    path('', index, name='index'),
    path('aboutMe', about_me, name='aboutMe'),

    #Dashboard
    path('dashboard/', dashboard, name='dashboard'),

    #Crear post, Editar post, delete post
    path('myPosts/', my_posts, name='myPosts'),
    path('editPost/<int:pk>', PostUpdateView.as_view(), name='editPost'),
    path('deletePost/<int:pk>', PostDeleteView.as_view(), name='deletePost'),
    path('createPost/', PostCreateView.as_view(), name='createPost'),

    #Editar User, logout, addAvatar
    path('editUser/', UserUpdateView.as_view(), name='editUser'),
    path('logout/', logout_views, name='logout'),
    path('search/', search_views, name='search_views'),
    path('addAvatar/', add_avatar, name='addAvatar'),

    #Detalles de posteo, comentarios
    path('postDetails/<int:post_id>/', postDetails, name='postDetails'),
]