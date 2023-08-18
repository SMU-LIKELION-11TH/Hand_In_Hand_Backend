import string
import random

from django.core.mail import EmailMessage
from django.db import models

class User(models.Model):
    image = models.ImageField(upload_to='user/', null=True, default="simple.png")
    name = models.CharField(max_length=10,null=False, default='')
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=30)
    nickname = models.CharField(max_length=10,null=False, default='')
    date_of_birth = models.DateField(max_length=20)
    address = models.CharField(max_length=1000)
    point = models.IntegerField()
    adopt_count = models.IntegerField(default=0)
    area = models.ForeignKey('post.Area', on_delete=models.CASCADE, null=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        app_label = 'user'

class Attendance(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True)
    class Meta:
        app_label = 'user'

class EmailVerification(models.Model):
    email = models.EmailField(unique=True, max_length=30, null=True)
    token = models.CharField(max_length=100, null=True)
    is_verified = models.BooleanField(default=False)
    class Meta:
        app_label = 'user'
    def generate_verification_token(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=100))

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_verification_token()
        super().save(*args, **kwargs)

    def verify(self):
        self.is_verified = True

    def verification(self):
        return self.is_verified


class Token(models.Model):
    email=models.ForeignKey('user.User', on_delete=models.CASCADE)
    token = models.CharField(max_length=100, null=True)

    def generate_verification_token(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=100))


class PasswordVerification(models.Model):
    email = models.EmailField(unique=True, max_length=30, null=True)
    token = models.CharField(max_length=6, null=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        app_label = 'user'

    def generate_verification_token(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_verification_token()
        super().save(*args, **kwargs)

    def verify(self):
        self.is_verified = True

    def verification(self):
        return self.is_verified