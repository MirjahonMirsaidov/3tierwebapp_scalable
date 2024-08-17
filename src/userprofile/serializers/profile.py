from rest_framework import serializers

from userprofile.models import UserProfile


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'first_name',
            'middle_name',
            'last_name',
        )

