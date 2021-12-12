from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify

# Create your models here.

#profil
#blanki zmienić potem
class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="brak biografii", max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    #etykieta
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    #wczyscy znajomi, widoczne jest to w pliku profileuser.html poprzez pętle for
    def get_friends(self):
        return self.friends.all()

    #ilość znajomych
    def get_friends_no(self):
        return self.friends.all().count()

    #stan profilu, który zawiera nazwę usera oraz czas w jakim został utworzony profil
    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    #nadawanie oryginalnej etykiety
    def save(self, *args, **kwargs):
        ex = False
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
#wybór
STATUS_CHOICES = (
    ('sent', 'sent'),
    ('accepted', 'accepted')
)

#relacje
class Relationship(models.Model):
    #nadawca
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    #odbiorca
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    #status
    status = models.CharField(max_length=8,choices=STATUS_CHOICES)
    #czas
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    #stan relacji, która zawiera odbiorcę, nadawcę i jej status, albo sent-wysłana czyli nieprzyjęta jeszcze przez drugiego użytkownika albo accepted-zaakceptowana
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"