from django import forms
from .models import Profile

#formularz aktualizowania danych, informacje zapożyczone z klasy profile
class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'country', 'avatar')