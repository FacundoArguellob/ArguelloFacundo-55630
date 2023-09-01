from django.shortcuts               import get_object_or_404, redirect, render
from django.contrib.auth            import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins     import LoginRequiredMixin
from django.utils.decorators        import method_decorator
from django.views.generic.edit      import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms      import AuthenticationForm
from django.db.models               import Q
from django.contrib.auth.models     import User
from django.urls                    import reverse_lazy

from .forms                         import *
from .models                        import *


# TODO: FIX footer dashboard
# TODO: FIX comentarios post, se salen del border


def index(request):
    return render(request, 'index.html')

def about_me(request):
    return render(request, 'aboutMe.html')

#Login
def login_views(request):
    form = AuthenticationForm()
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                avatar = Avatar.objects.get(user_id=request.user.id).imagen.url
            except:
                avatar = "/media/avatares/default.png"
            finally:
                request.session["avatar"] = avatar
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'alert': 'Invalid username or password', 'form': form})
    return render(request, 'login.html', {'form': form})


#Logout
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
    try:
        avatar = Avatar.objects.get(user_id= request.user.id)
    except:
        avatar = 'media/avatares/default.png'
    return render(request, 'dashboard.html', {'posts': posts, 'comments': comments, 'avatar': avatar})


@login_required
def postDetails(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = ComentarioForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post  # Asocia el comentario con el post actual
            new_comment.author = request.user  # Asigna a el usuario logeado como el author
            new_comment.save()
            comment_form = ComentarioForm()
            return render(request, 'postDetails.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

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
    
    @method_decorator(login_required) #Esto evita que un usuario sin estar logeado pueda acceder a la creacion de posteos ya que el metodo dispatch() se ejecuta antes que cualquier otra accion en la clase
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

#Edit User
class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    fields = ['first_name','last_name','username', 'email']
    template_name = 'editUser.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.instance.user = self.request.user  # Asignar el usuario actual al perfil
        return super().form_valid(form)

#Mis posteos
@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'myPosts.html', {'posts': posts})


#Buscador
@login_required
def search_views(request):
    query = request.GET.get('q')  # Obtiene el valor de búsqueda desde la URL
    posts = []

    if query:
        # Realiza una búsqueda utilizando Q() para combinar las condiciones de búsqueda
        posts = Post.objects.filter(
            Q(title__icontains=query) |  # Busca en el título (insensible a mayúsculas/minúsculas)
            Q(category__name__icontains=query)  # Busca en la categoría (insensible a mayúsculas/minúsculas)
        )
    return render(request, 'dashboard.html', {'query': query, 'posts': posts})


class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = 'editPost.html'
    form_class = PostForm
    success_url = reverse_lazy('myPosts')

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'deletePost.html'
    success_url = reverse_lazy('myPosts')


@login_required
def add_avatar(request):
    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            u = User.objects.get(username=request.user)
            #Para borrar el avatar viejo
            avatarViejo = Avatar.objects.filter(user=u)
            if len(avatarViejo) > 0:
                for i in range(len(avatarViejo)):
                    avatarViejo[i].delete()
            #Guardar el nuevo
            avatar = Avatar(user=u, imagen=form.cleaned_data['imagen'])
            avatar.save()
            return redirect('dashboard')
    else:
        form = AvatarForm()
    return render(request, "addAvatar.html", {'form': form })