from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm


from .forms import *
from .models import *
# Create your views here.



# TODO:
# TODO:
# TODO: agregar los .os correspondientes para que el proyecto funcione en el equipo del tutor
# TODO: barra de busqueda para los posteos
# TODO: archivo readme.md con: (nombre del proyecto, objetivo funcional, descripcion de modelos, usuario admin + contraseña)


# Objetivos del proyecto final
# 1- diseño no usado en clase, con un menu con al menos 4 links
# 2- login, logout, registro, edit user + foto de perfil o avatar del usuario logeado
# 3- funcionalidad CRUD de al menos 4 modelos con sus formularios y unicamente habilitados para usuarios logueados
# 4- About me page con la informacion del alumno
# 5- video mostrando el uso de la pagina y sus funciones generales (no mas de 10min)
# 6- debe incluir un exel con al menos 5 casos de pruebas unitarias
# 7- puede uncluir un search como filtro para buscar informacion 





def index(request):
    return render(request, 'index.html')

#Login
def login_views(request):
    form = AuthenticationForm()
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'alert': 'Invalid username or password', 'form': form})
    return render(request, 'login.html', {'form': form})


def logout_views(request):
    logout(request)
    return redirect('login')


#Registro
class UsuarioCreateView(CreateView):
    form_class = RegistroForm 
    template_name = 'registro.html' 
    success_url = reverse_lazy('login') 

#Blog
@login_required
def dashboard(request):
    posts = Post.objects.order_by('-date_pub')
    comments = Comment.objects.all()
    contador_comentarios = 0
    for post in posts:
        for comment in comments:
            if post.id == comment.post_id:
                contador_comentarios += 1
                print(contador_comentarios)

    return render(request, 'dashboard.html', {'posts': posts})


def postDetails(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = ComentarioForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post  # Asocia el comentario con el post actual
            new_comment.author = request.user  # Assign the logged-in user as the author
            new_comment.save()
            return redirect(reverse_lazy('dashboard'))
    else:
        comment_form = ComentarioForm()
    return render(request, 'postDetails.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


class PostCreateView(CreateView):
    form_class = PostForm
    template_name = 'createPost.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Establecer el autor como el usuario actual
        return super().form_valid(form)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

#Edit User
@login_required
def edit_user(request):
    return render(request, 'editUser.html')
    