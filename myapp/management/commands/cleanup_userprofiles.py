
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import UserProfile
from collections import defaultdict

class Command(BaseCommand):
    help = 'Remove duplicate UserProfile entries and retain only one per user.'

    def handle(self, *args, **kwargs):
        duplicates = defaultdict(list)
        for profile in UserProfile.objects.all():
            duplicates[profile.user_id].append(profile)

        total_removed = 0
        for user_id, profiles in duplicates.items():
            if len(profiles) > 1:
                self.stdout.write(f"Duplicate profiles for user_id={user_id}: {len(profiles)}")
                # Keep the first, delete the rest
                for profile in profiles[1:]:
                    profile.delete()
                    total_removed += 1

        self.stdout.write(self.style.SUCCESS(f"Removed {total_removed} duplicate UserProfiles."))
