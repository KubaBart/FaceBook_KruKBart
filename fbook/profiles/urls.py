from django.urls import path
from .views import profileuser_view
from .views import invites_received
from .views import list_of_profiles_to_invites
from .views import ProfileList
from .views import invatation_send
from .views import remove_friend
from .views import invite_remove, invite_accept
from .views import ProfileDetail

#zajerestrowanie adresu url profilu pojedynczego usera
app_name='profiles'
urlpatterns = [
    path('', ProfileList.as_view(), name='profiles-all'),
    path('profileuser/', profileuser_view, name='profile-user-view'),
    path('profilinvites/', invites_received, name='profile-invites'),
    path('profilestoinvite/', list_of_profiles_to_invites, name='profiles-to-invite'),
    path('sendinvatation/', invatation_send, name='invite-send'),
    path('removefriends/', remove_friend, name='remove-friends'),
    path('inviteremove/', invite_remove, name='invite-remove'),
    path('inviteaccept/', invite_accept, name='invite-accept'),
    path('<slug>/', ProfileDetail.as_view(), name='profile-detail')
]