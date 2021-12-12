from django.shortcuts import render
from .models import Profile
from .form_update import ProfileModelForm
# Create your views here.

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

    context = {
        'profile' : profile,
        'form_upd' : form_upd,
        'confirm_form': confirm_form,
    }
    return render(request, 'profiles/profileuser.html', context)