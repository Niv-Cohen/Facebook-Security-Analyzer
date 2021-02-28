from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password = None):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not name:
            raise ValueError("Fullname is required")
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            text_password = password
        )
        user.set_password(password)
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255, unique = True)
    text_password = models.CharField(max_length = 255, default = "")
    network = models.JSONField(default = None, blank = True, null = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email