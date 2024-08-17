from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        try:
            data.update({'role': self.user.role.name})
            data.update({'user_id': self.user.id})
            self.user.last_login = timezone.now()
            self.user.save()
        except AttributeError:
            data.update({'role': None})
        # username = attrs.get('username')
        # if '@' in username:
        #     if not self.user.email_verified:
        #         send_email_verification(self.user)
        #         raise serializers.ValidationError({'email': 'Email is not verified. Verfication send!!!'})
        # else:
        #     if not self.user.phone_verified:
        #         # send_sms_verification(self.user) TODO
        #         raise serializers.ValidationError({'phone': 'Phone is not verified. Verfication send!!!'})
        return data


