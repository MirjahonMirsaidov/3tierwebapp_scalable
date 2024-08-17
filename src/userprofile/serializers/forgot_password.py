from rest_framework import serializers

from userprofile.models import UserProfile


class ForgotPasswordSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(max_length=255, required=False)
    password = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = UserProfile
        fields = ('email', 'phone', 'password')

        extra_kwargs = {
            'email': {'write_only': True},
            'phone_number': {'write_only': True},
        }

    def validate(self, attrs):
        if not attrs.get('email') and not attrs.get('phone'):
            raise serializers.ValidationError({'login': 'Email or phone number is required'})
        return attrs

    def validate_email(self, email):
        if email and not UserProfile.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exists')
        return email

    def validate_phone(self, phone):
        if phone and not UserProfile.objects.filter(phone_number=phone).exists():
            raise serializers.ValidationError('Phone number does not exists')
        return phone

    def create(self, validated_data):
        email = validated_data.get('email')
        phone = validated_data.get('phone')
        if email and UserProfile.objects.filter(email=email).exists():
            user = UserProfile.objects.filter(email=email).first()
        elif phone and UserProfile.objects.filter(phone_number=phone).exists():
            user = UserProfile.objects.filter(phone_number=phone).first()
        user.set_password(validated_data.get('password'))
        user.save()
        return validated_data


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255, required=True)
    new_password = serializers.CharField(max_length=255, required=True)

    def validate_old_password(self, old_password):
        if not self.context['request'].user.check_password(old_password):
            raise serializers.ValidationError('Old password is incorrect')
        return old_password

    def create(self, validated_data):
        self.context['request'].user.set_password(validated_data.get('new_password'))
        self.context['request'].user.save()
        return validated_data
