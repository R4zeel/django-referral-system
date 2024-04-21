from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from users.models import PhoneUser, PhoneVerification


class UserProfileSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    referents = serializers.SerializerMethodField('get_referents')

    class Meta:
        model = PhoneUser
        fields = ('id', 'phone_number', 'invite_token', 'referents')

    def get_referents(self, instance):
        user = PhoneUser.objects.get(id=instance.id)
        queryset = user.referent.all()
        return ReferentSerializerForRead(queryset, many=True).data


class ReferentSerializerForRead(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = PhoneUser
        fields = ('id', 'phone_number')


class ReferralSerializer(serializers.Serializer):
    invite_token = serializers.CharField(required=True)

    def validate(self, attrs):
        referrer = PhoneUser.objects.filter(
            invite_token=attrs['invite_token']
        )
        if not referrer.exists():
            raise serializers.ValidationError('Введён некорректный код.')
        if referrer.first() == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя использовать собственный код.'
            )
        if self.context['request'].user.referred_by:
            raise serializers.ValidationError('Нельзя ввести новый код.')
        attrs['referrer'] = referrer.first()
        return attrs

    def create(self, validated_data):
        current_uesr = PhoneUser.objects.filter(
            id=self.context['request'].user.id
        ).update(referred_by=validated_data['referrer'])
        return current_uesr

    def to_representation(self, instance):
        return UserProfileSerializer(
            instance=PhoneUser.objects.get(id=self.context['request'].user.id)
        ).data


class PhoneUserSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(required=True)

    def validate(self, attrs):
        phone = attrs['phone_number']
        if PhoneUser.objects.filter(
            phone_number=phone
        ).exists():
            raise serializers.ValidationError(
                'Данный номер занят.'
            )
        return attrs


class PhoneVerificationSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(required=True)
    verify_code = serializers.CharField(required=True)

    def validate(self, attrs):
        phone_number = attrs['phone_number']
        verification_code = attrs['verify_code']
        verify_object = PhoneVerification.objects.filter(
            phone_number=phone_number,
            verification_code=verification_code
        )
        if not verify_object.exists():
            raise serializers.ValidationError(
                'Введён неверный код, попробуйте ввести код корректно либо \
                запросите новый'
            )
        return attrs
