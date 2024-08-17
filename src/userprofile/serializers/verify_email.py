import random

from rest_framework import serializers

from core.utils.email.verification import send_verification_code
from core.utils.phone.verification import send_sms_verification
from userprofile.models import UserProfile, CodeVerification


class CodeSendSerializer(serializers.ModelSerializer):
    isRegistered = serializers.ReadOnlyField()
    code = serializers.ReadOnlyField()
    phone = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(max_length=255, required=False)
    isCheck = serializers.BooleanField(required=False)

    class Meta:
        model = UserProfile
        fields = ('email', 'phone', 'isRegistered', 'code', 'isCheck')

        extra_kwargs = {
            'email': {'write_only': True},
            'phone_number': {'write_only': True},
        }

    def validate(self, attrs):
        if not attrs.get('email') and not attrs.get('phone'):
            raise serializers.ValidationError({'login': 'Email or phone number is required'})
        return attrs

    def create(self, validated_data):
        email = validated_data.get('email')
        phone = validated_data.get('phone')
        is_check = validated_data.get('isCheck')
        isRegistered = False
        if email and UserProfile.objects.filter(email=email).exists() or \
                phone and UserProfile.objects.filter(phone_number=phone).exists():
            isRegistered = True
        code = str(random.randint(1000, 9999))
        if not (is_check and isRegistered):
            CodeVerification.objects.create(email=email, phone=phone, code=code)
            if email:
                send_verification_code(email, code)
            elif phone:
                send_sms_verification(phone, code)
        return {'isRegistered': isRegistered, 'code': code, 'isCheck': is_check}

