from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager
from django.utils import timezone
import uuid

# Create your models here.

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name="date created",default=timezone.now)
    updated_at = models.DateTimeField(verbose_name="date updated",default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class AuthToken(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='auth_tokens')
    access_token = models.CharField(max_length=250)
    refresh_token = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)


class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", 'Pending'),
        ("accepted", 'Accepted'),
        ("rejected", 'Rejected'),
    ]

    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')