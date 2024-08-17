from rest_framework import serializers

from userprofile.models import UserProfile


class ProfileInfoSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name')

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'phone_number',
            'email',
            'first_name',
            'middle_name',
            'last_name',
            'username',
            'role',
        )

