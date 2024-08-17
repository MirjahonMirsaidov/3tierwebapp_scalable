from rest_framework import serializers

from dataset.core_serializers.region import RegionCoreSerializer
from userprofile.models import UserProfile


class ProfileCoreSerializer(serializers.ModelSerializer):
    # region = RegionCoreSerializer()

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'phone_number',
            'email',
            'first_name',
            'middle_name',
            'last_name',
            'region',
            'chat_id',
            'last_login',
        )


class ProfileGetCoreSerializer(serializers.ModelSerializer):
    region = RegionCoreSerializer()

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'phone_number',
            'email',
            'first_name',
            'middle_name',
            'last_name',
            'region',
            'chat_id',
            'last_login',
        )
