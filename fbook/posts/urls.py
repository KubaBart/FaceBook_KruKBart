from django.urls import path
from .views import post_create_comment
from .views import like_unlike_post
from .views import PostDelete
from .views import PostUpdate

#zarejestrowanie adresu url postu
app_name='posts'

urlpatterns = [
    path('', post_create_comment, name='post-view'),
    path('liked/', like_unlike_post, name='like-post'),
    path('<pk>/update/', PostUpdate.as_view(), name='post-edit'),
    path('<pk>/delete/', PostDelete.as_view(), name='post-delete'),
]