from django.shortcuts import render


from profiles.models import Profile

def home_view(request):
    user = request.user
    hello = 'Hello world'

    context = {
        'user' : user,
        'hello' : hello,
    }
    return render(request, 'main/home.html', context)


#wyszukiwanie znajomych
def search_friends(request):
    if request.method == "POST":
        que = request.POST['que']
        search = Profile.objects.filter(slug__contains=que)
        return render(request, 'profiles/search_friends.html', {'que':que, 'search':search, })
    else:
        return render(request, 'profiles/search_friends.html', {})

