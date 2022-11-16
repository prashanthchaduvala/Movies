from django.db import models


from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

from rest_framework_simplejwt.tokens import RefreshToken







class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given mobile and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        # email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)




class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True, null=True, blank=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
    password = models.CharField(_('password'), max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="created date", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="updated date",null=True)
    is_active = models.BooleanField(_('active'), default=True, null=True)


    objects = UserManager()

    USERNAME_FIELD = 'username'  # User should be able to login with
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def refresh(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh)

    def access(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)


# cast model
class Cast(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('name'), max_length=500, blank=True, null=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, default=False)
    dob = models.DateField(default=False, null=True)
    OnetoOneField_Creator = models.OneToOneField(UserProfile, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# movie model
class Movie(models.Model):
    castname= models.ForeignKey(Cast,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    title= models.CharField(_('title'), max_length=500, blank=True, null=True)
    created_at=models.DateTimeField(verbose_name="created at",null=True)
    updated_at=models.DateTimeField(verbose_name="updated at",null=True)
    runtime= models.DecimalField(max_digits = 7,decimal_places=3)
    language= models.CharField(_('language'), max_length=500, blank=True, null=True)
    tagline= models.CharField(_('tagline'), max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


