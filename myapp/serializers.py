from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Applicant, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ["region"]


class UserSerializer(serializers.ModelSerializer):

    profile = serializers.SerializerMethodField()
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "profile",
        ]

    def get_profile(self, user_obj):

        try:

            profile = user_obj.userprofile
            return UserProfileSerializer(profile).data
        except UserProfile.DoesNotExist:
            return None


class ApplicantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Applicant
        fields = "__all__"
