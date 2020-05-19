from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    photo = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255)
    password_changed_at = models.BigIntegerField(null=True)
    password_reset_token = models.CharField(null=True, max_length=255)
    password_reset_expires = models.BigIntegerField(null=True)

    def __str__(self):
        return self.name
