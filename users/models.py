from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.http import urlquote
import tbapy
import requests
from django.utils import timezone
from PIL import Image


# Create your models here.
#Custom user model
class CustomUserManager(BaseUserManager):

    
    def create_user(self, username, email, password, **kwargs):
        if not email:
            raise ValueError("Email must be present")

        email = self.normalize_email(email)
        user = self.model(
                username = username,
                email = self.normalize_email(email),
              
                password = CustomUser.objects.make_random_password(),
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        is_careGiver = True
        user.save(using=self._db)
        return user



class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=254, unique=True)
    email = models.EmailField(unique=True)

    date_joined = models.DateTimeField(default=timezone.now())

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_careGiver = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def get_absolute_url(self):
        return '/users/%s/' % urlquote(self.email)

    #def get_short_name(self):
    #    return self.first_name

    def has_perm(self, perm, obj=None):
        if self.is_admin:
            return True
        else:
            return False

    def has_module_perms(self, app_label):
        return True

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    image = models.ImageField(default='default.jpg', upload_to='profile-pics')
    first_name = models.CharField(verbose_name="First Name", max_length=254, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=254, blank=True)
    
    def __str__(self):
        return f'{self.user.username}';

class Reminders(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reminderType = models.IntegerField(verbose_name="Reminder Type")
    name = models.CharField(max_length=250)
    date = models.DateField(verbose_name="Date")
    time = models.CharField(max_length=100)
    priority = models.IntegerField(verbose_name="Priority")
    isAttached = models.BooleanField(default="False")

    #reminder type
        #0 - Simple Reminder
        #1 - Location
        #2 - Event
        #3 - Appointment

    #priority
        #0 - Low
        #1 - Medium
        #2 - High