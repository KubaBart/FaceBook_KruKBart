from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile

#klasa posty
class Post(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['jpeg', 'jpg', 'png', 'bmp'])], blank=True)
    liked = models.ManyToManyField(Profile, related_name='likes', blank=True)

    #max 250 znaków tytuł posta
    def __str__(self):
        return str(self.content[:250])

    #licznik polubień pod postem
    def likes_number(self):
        return self.liked.all().count()

    #liczba komentarzy pod postem
    def comments_count(self):
        return self.comment_set.all().count()

    #komentarz posegregowane od najnowszego na górze do najstarszego na dole
    class comments:
        ordering = ('-author',)

#klasa komentarze
class Comment(models.Model):
    #klucz obcy z klasy profile
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #klucz obcy z klasy post
    post = models. ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=250)

    def __str__(self):
        return str(self.pk)

#wybór między polubieniem czy nie polubieniem
LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)

#klasa polubienia
class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=6)

    #reprezentacja tekstowa
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"

