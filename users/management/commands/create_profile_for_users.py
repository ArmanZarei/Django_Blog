from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tqdm import tqdm
from users.models import Profile


class Command(BaseCommand):
    help = 'Creates profile for users without an existing profile'

    def handle(self, *args, **kwargs):
        users_without_profile = User.objects.filter(profile__isnull=True)
        if len(users_without_profile) == 0:
            print("All the users have profile")
        else:
            for u in tqdm(users_without_profile):
                Profile.objects.create(user=u)
