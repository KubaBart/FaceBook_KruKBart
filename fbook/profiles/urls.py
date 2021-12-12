from django.urls import path
from .views import profileuser_view

#adres url do profilu pojedynczego usera
app_name='profiles'
urlpatterns = [
    path('profileuser/', profileuser_view, name='profile-user-view')
]