from django.shortcuts import render
from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Profile
from .models import Relationship
from .form_update import ProfileModelForm

#widok pojedynczego usera, poprzez przekazanie informacji usera
#widok aktualizacji profilu
def profileuser_view(request):
    profile = Profile.objects.get(user=request.user)

    # aktualizowanie konkretnego profilu
    form_upd = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile )
    confirm_form = False
    not_confirm_form = False

    #sprawdzenie poprawności, czy formularz jest poprawny
    if request.method == 'POST':
        if form_upd.is_valid():
            form_upd.save()
            confirm_form = True
        else:
            not_confirm_form = True

    #zmienne kontekstowe
    context = {
        'profile' : profile,
        'form_upd' : form_upd,
        'confirm_form': confirm_form,
    }
    #zwrócenie widoku
    return render(request, 'profiles/profileuser.html', context)

#widok otrzymanego zaproszenia
def invites_received(request):
    profile = Profile.objects.get(user=request.user)
    set_of_queries = Relationship.objects.invatations_received(profile)
    empty = False
    res=list(map(lambda x: x.sender, set_of_queries))
    #jeśli nie ma żadnych zaproszeń
    if len(res)==0:
        empty=True
    #zmienne kontekstowe
    context = {
        'empty' : empty,
        'set_of_queries' : res,
    }
    #zwrócenie widoku
    return render(request, 'profiles/profilinvites.html', context)

#lista profili
def list_of_profiles(request):
    user = request.user
    set_of_queries = Profile.objects.get_profiles_all(user)

    # zmienne kontekstowe
    context = {
        'set_of_queries': set_of_queries,
    }
    # zwrócenie widoku
    return render(request, 'profiles/list_profiles.html', context)

#lista możliwych zaproszeń
def list_of_profiles_to_invites(request):
    user = request.user
    set_of_queries = Profile.objects.get_profiles_all_invite(user)

    # zmienne kontekstowe
    context = {
        'set_of_queries': set_of_queries,
    }
    # zwrócenie widoku
    return render(request, 'profiles/available_invites.html', context)

class ProfileList(ListView):
    #określenie modelu
    model = Profile
    #wskazanie szablonu do widoku
    template_name = 'profiles/list_profiles.html'
    #określenie listy obiektów do wyświetlenia
    def get_queryset(self):
        set_of_queries = Profile.objects.get_profiles_all(self.request.user)
        return set_of_queries

    #metoda służąca do wypełnienia słownika która używana jest jako kontekst szablonu
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        # przechowywanie relacji w których zaprosiliśmy innych użytkowników do znajomych
        receiver_relation = Relationship.objects.filter(sender=profile)
        #relacja zapoczątkowana od innych użytkowników
        sender_relation = Relationship.objects.filter(receiver=profile)
        sender_relation_list = []
        receiver_relation_list = []
        #dołączenie relacji do list
        for y in receiver_relation:
            receiver_relation_list.append(y.receiver.user)
        for y in sender_relation:
            sender_relation_list.append(y.sender.user)
        #zmienne kontekstowe
        context["receiver_relation_list"] = receiver_relation_list
        context["sender_relation_list"] = sender_relation_list
        #jeśli długość naszego zapytania jest równa zero
        context['is_empty'] = False
        #to tworzymy inny klucz w słowniku kontekstowym
        if len(self.get_queryset()) == 0:
            context['is empty'] = True
        return context

#wysyłanie zaproszeń do znajomych
def invatation_send(request):
    #jeśli mamy do czynienia z żądaniem post, uzyskujemy dostęp do tego adresu URL który zamierzamy zarejestrować
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        relat = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:profile-user-view')

#usuwanie ze znajomych
def remove_friend(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        relat = Relationship.objects.get((Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)))
        relat.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:profile-user-view')

#widok zaakceptowanego zaproszenia
def invite_accept(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        relat = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if relat.status == 'send':
            relat.status = 'accepted'
            relat.save()
    return redirect('profiles:profile-invites')

#widok usuniętego zaproszenia
def invite_remove(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        relat = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        relat.delete()
    return redirect('profiles:profile-invites')

#widok profilu innego użytkownika
class ProfileDetail(DetailView):
    model = Profile
    template_name = 'profiles/profile_particular.html'
    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        # przechowywanie relacji w których zaprosiliśmy innych użytkowników do znajomych
        receiver_relation = Relationship.objects.filter(sender=profile)
        #relacja zapoczątkowana od innych użytkowników
        sender_relation = Relationship.objects.filter(receiver=profile)
        sender_relation_list = []
        receiver_relation_list = []
        #dołączenie relacji do list
        for y in receiver_relation:
            receiver_relation_list.append(y.receiver.user)
        for y in sender_relation:
            sender_relation_list.append(y.sender.user)
        #zmienne kontekstowe
        context["receiver_relation_list"] = receiver_relation_list
        context["sender_relation_list"] = sender_relation_list
        #wszystkie posty użytkownika
        context["posts"] = self.get_object().get_authors_all_posts()
        context["post_user_len"] = True \
            if len(self.get_object().get_authors_all_posts()) >0 else False
        return context