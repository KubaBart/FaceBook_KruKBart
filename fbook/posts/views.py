from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Post, Like
from profiles.models import Profile
from .form_post import PostModelForm
from .form_post import CommentModelForm

#widok tworzenia komentarzy
def post_create_comment(request):

    # przechowywanie wszystkich obiektów w zmiennej
    set_of_queries = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    form_post = PostModelForm()
    form_comment = CommentModelForm()

    # Informacje na temat konkretnego użytkownika
    profile = Profile.objects.get(user=request.user)

    #wartość początkowa
    new_post = False
    new_comment = False

    #formularz posta
    #Jeśli przesyłanie wykonuje się w żądaniu postu to formularz zostanie przesłany a następnie wykonuje się poniższy kod
    if 'submit_form_post' in request.POST:
        print(request.POST)
        form_post = PostModelForm(request.POST, request.FILES)
        # jesli formularz postu jest prawidłowy
        if form_post.is_valid():
            object = form_post.save(commit=False)
            # przypisz do zewnętrznego pola ten profil
            object.author = profile
            # zapisanie obiektu
            object.save()
            form_post = PostModelForm()
            new_post = True

    #formularz komentarza
    if 'submit_form_comment' in request.POST:
        form_comment = CommentModelForm(request.POST)
        # jeśli formularz komentarza jest prawidłowy
        if form_comment.is_valid():
            object2 = form_comment.save(commit=False)
            # to przypisz usera który jest aktualnie zalogowany
            object2.user = profile
            # pobranie wiadomości
            object2.post = Post.objects.get(id=request.POST.get('post_id'))
            # zapisanie obiektu
            object2.save()
            form_comment = CommentModelForm()
            new_comment = True

    #zmienne kontekstowe
    context={
        'new_post' : new_post,
        'set_of_queries' : set_of_queries,
        'profile' : profile,
        'form_post' : form_post,
        'form_comment' : form_comment,
        'new_comment' : new_comment
    }

    # zwrócenie widoku, powyższych kluczy można potem użyć w .html
    return render(request, 'posts/postuser.html', context)

def like_unlike_post(request):
    # jeśli użytkownik jest zalogowany to ustaw na tego użytkownika
    user = request.user
    # sprawdzenie czy mamy do czynienia z żądaniem wiadomości
    if request.method == 'POST':
        # pobierz identyfikator wiadomości
        post_id = request.POST.get('post_id')
        # uzyskanie obiektu posta
        post_x = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        # jeśli użytkownik już kliknął polubienie
        if profile in post_x.liked.all():
            # to jeśli kliknie drugi raz to odznaczy polubienie
            post_x.liked.remove(profile)
        else:
            # w przeciwnym razie, polubi ten post
            post_x.liked.add(profile)

        # reakcje pod postem, umożliwiające automatyczne wpisanie do bazy wartości
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        # pierwsze kliknięcie będzie polubieniem, zaś ponowne kliknięcie będzie unlikiem
        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
            post_x.save()
            like.save()
        else:
            like.value='Like'
            post_x.save()
            like.save()

    # zwrócenie widoku postu
    return redirect('posts:post-view')

#klasa do edycji posta
class PostUpdate(UpdateView):
    form_class = PostModelForm
    model = Post
    #wskazanie szablonu
    template_name = 'posts/postupdate.html'
    success_url = reverse_lazy('posts:post-view')
    # czy użytkownik jest autorem postu
    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        # jeśli nie jest to autor tego postu to nie edytuje tego postu
        if form.instance.author != profile:
            form.add_error(None, "Nie możesz edytować tego postu ponieważ nie jesteś jego autorem")
            return super().form_invalid(form)
        # w przeciwnym wypadku przejdzie do edycji postu
        else:
            return super().form_valid(form)

# klasa usuwania formularza
class PostDelete(DeleteView):
    #określenie modelu
    model = Post
    # wskazanie szablonu
    template_name = 'posts/postdel.html'
    # jeśli nastąpi pomyślnie usunięcie posta to wrócimy do głównej strony postów
    success_url = reverse_lazy('posts:post-view')
    # czy obecnie zalogowany użytkownik to autor postu
    def get_object(self, *args, **kwargs):
        #uzyskanie klucza głównego
        pk = self.kwargs.get('pk')
        x = Post.objects.get(pk=pk)
        # jeśli nie jest to autor tego postu to nie może go usunąć
        if not x.author.user == self.request.user:
            messages.warning(self.request, 'Nie można usunąć postu ponieważ nie jesteś autorem tego postu')
        return x