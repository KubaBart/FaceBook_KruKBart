from django.contrib import admin
from .models import Profile
from .models import Relationship

#zaimportowanie klas
admin.site.register(Profile)
admin.site.register(Relationship)