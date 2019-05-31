
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class User(models.Model):
    user_name = models.CharField(max_length=20)
    date_added = models.DateTimeField(default=timezone.now)


class Contact(models.Model):
    user_f_name = models.ForeignKey(User, on_delete=models.CASCADE)
    friend_name  = models.CharField(max_length=20, default='shark')
    created_date = models.DateTimeField(default=timezone.now)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def save_contact(self):
        self.save()

    def __str__(self):
        return self.friend_name

# Create your models here.
