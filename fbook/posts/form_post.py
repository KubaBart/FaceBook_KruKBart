from django import forms
from .models import Post
from .models import Comment

#formularz postu
class PostModelForm(forms.ModelForm):
    # określenie wielkości formularza postu do trzech wierszy
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = Post
        fields = ('content', 'image')

#formularz komentarza
class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder' : 'Dodaj komentarz'}))
    class Meta:
        model = Comment
        fields = ('body',)