from .models import Profile, Relationship
#awatar obok nazwy użytkownika obecnie zalogowanego
def profile_img(request):
    if request.user.is_authenticated:
        x_profile = Profile.objects.get(user=request.user)
        image = x_profile.avatar
        #zwrócenie słownika kontekstowego
        return {
            'picture' : image
        }
    return {}

#liczba otrzymanych zaproszeń
def num_invatation_received(request):
    if request.user.is_authenticated:
        x_profile = Profile.objects.get(user=request.user)
        num_r_invata = Relationship.objects.invatations_received(x_profile).count()
        return {
            'count_invites_r' : num_r_invata
        }
    return {}
