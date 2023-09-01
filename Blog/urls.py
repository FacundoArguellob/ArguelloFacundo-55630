from django.urls import path
from .views      import *



urlpatterns = [
    path('', index, name='index'),
    path('registro/', UsuarioCreateView.as_view(), name='registro'),
    path('login/', login_views, name='login'),
    path('logout/', logout_views, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('search/', search_views, name='search_views'),
    path('editUser/', UserUpdateView.as_view(), name='editUser'),
    path('addAvatar/', add_avatar, name='addAvatar'),
    path('editPost/<int:pk>', PostUpdateView.as_view(), name='editPost'),
    path('deletePost/<int:pk>', PostDeleteView.as_view(), name='deletePost'),
    path('myPosts/', my_posts, name='myPosts'),
    path('createPost/', PostCreateView.as_view(), name='createPost'),
    path('postDetails/<int:post_id>/', postDetails, name='postDetails'),
]