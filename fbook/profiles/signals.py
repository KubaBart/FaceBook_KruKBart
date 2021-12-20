from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from .models import Profile, Relationship

#połączenie i zapis usera z profilem
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#połaczenie i zapis relacji (jeśli drugi user zaakceptował zaproszenie) pomiędzy dwoma userami
@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()

#usunięcie ze znajomych (usunięcie występowania dwóch przycisków)
@receiver(pre_delete, sender=Relationship)
def pre_delete_friends_remove(sender, instance, **kwargs):
    sender = instance.sender
    receiver =instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    sender.save()
    receiver.save()