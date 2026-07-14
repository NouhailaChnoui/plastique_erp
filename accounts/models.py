from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrateur"
        EMPLOYE = "employe", "Employé"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.EMPLOYE)
    telephone = models.CharField(max_length=30, blank=True)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def __str__(self):
        return self.get_full_name() or self.username
