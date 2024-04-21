from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class PhoneUser(AbstractUser):
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('username',)

    username = models.CharField(max_length=30, null=True, unique=False)
    phone_number = PhoneNumberField(unique=True)
    invite_token = models.CharField(max_length=6, unique=True)
    referred_by = models.ForeignKey(
        'PhoneUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='referent'
    )

    def __str__(self):
        return str(self.phone_number)


class PhoneVerification(models.Model):
    phone_number = PhoneNumberField(unique=True)
    verification_code = models.CharField(max_length=4)
    is_verified = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['phone_number', 'verification_code'],
                name='unique verification'
            )
        ]