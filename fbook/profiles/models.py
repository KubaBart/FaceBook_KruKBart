from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.shortcuts import reverse

# Create your models here.

class ProfileManage(models.Manager):

    #uzyskanie wszystkich profilów z wyjątkiem naszego
    def get_profiles_all(self, myprof):
        #wszystkie profile oprócz mojego
        profiles = Profile.objects.all().exclude(user=myprof)
        return profiles

    #wszystkie profile które możemy zaprosić (z którymi nie mamy relacji)
    def get_profiles_all_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        #wszystkie relacje w których jesteśmy nadawcą lub odbiorcą zaproszenia
        set_of_queries = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        #lista wszystkich znajomych
        invites_accepted = set([])
        print(set_of_queries)
        #przejście przez zestaw zapytań
        for relation in set_of_queries:
            #czy zaproszenie zostało zaakceptowane
            if relation.status == 'accepted':
                invites_accepted.add(relation.receiver)
                invites_accepted.add(relation.sender)
        print(invites_accepted)
        #wszystkie dostępne profile do zaproszenia oprócz własnego profilu oraz dodanych znajomych
        profiles_to_invite = [profile for profile in profiles if profile not in invites_accepted]
        print(profiles_to_invite)
        return profiles_to_invite

#profil
#blanki zmienić potem
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    bio = models.TextField(default="brak biografii", max_length=300)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #etykieta
    slug = models.SlugField(unique=True, blank=True)
    objects = ProfileManage()

    #wczyscy znajomi, widoczne jest to w pliku profileuser.html poprzez pętle for
    def get_friends(self):
        return self.friends.all()

    #ilość znajomych
    def get_count_friends(self):
        return self.friends.all().count()

    #tytuł profilu, który zawiera nazwę usera oraz czas w jakim został utworzony profil, reprezentacja tekstowa
    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    #nadawanie oryginalnej etykiety
    #*args i **kwargs pozwalają na przekazanie nieokreślonej liczby argumentów do funkcji, nie trzeba wiedzieć ile argumentów zostaje przekazanych do funkcji
    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        #jeśli identyfikator jest pusty bądź jest zmieniony, nie jest równe początkowemu
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug == "":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

    #licznik danych postów przez użytkownika
    def get_count_posts(self):
        return self.posts.all().count()

    def get_authors_all_posts(self):
        return self.posts.all()

    #licznik danych polubień przez użytkownika
    def get_count_likes(self):
        total_liked = 0
        liked = self.like_set.all()
        for x in liked:
            if x.value == 'Like':
                total_liked +=1
        return total_liked

    #licznik danych nie polubień przez użytkownika
    def get_count_unlikes(self):
        total_unliked = 0
        Unlikes = self.like_set.all()
        for x in Unlikes:
            if x.value == 'Unlike':
                total_unliked +=1
        return total_unliked

    #liczba otrzymanych polubień/nie polubień, aktywność
    #pobieramy konkretny post, uzyskujemy dostęp do pola polubień
    #następnie pobieramy wszystkie polubienia poszczególnych postów oraz liczymy je
    def get_count_received_likes(self):
        total_liked = 0
        posts = self.posts.all()
        for x in posts:
            total_liked+=x.liked.all().count()
        return total_liked

    #zobacz profil
    def get_show_profil(self):
        return reverse("profiles:profile-detail", kwargs={"slug": self.slug})


#wybór między wysłanym zaproszeniem do znajomych a zaakceptowanym
STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

#menadżer relacji
class RelationshipManage(models.Manager):
    def invatations_received(self, receiver):
        set_of_queries = Relationship.objects.filter(receiver=receiver, status='send')
        return set_of_queries

#relacje
class Relationship(models.Model):
    #nadawca
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    #odbiorca
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    #status
    status = models.CharField(max_length=8,choices=STATUS_CHOICES)
    objects = RelationshipManage()
    #tytuł relacji, która zawiera odbiorcę, nadawcę i jej status, albo sent-wysłana czyli nieprzyjęta jeszcze przez drugiego użytkownika albo accepted-zaakceptowana, reprezentacja tekstowa
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
