from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password


# Create your models here.
class users_manager(BaseUserManager):
    def create_user(self, email, phone, name, password=None):

        user = self.model(email=self.normalize_email(email),
                          phone=phone,
                          name=name,
                          password=make_password(password))
    
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, name, password=None):
        User.objects.create(email=self.normalize_email(
            email), phone=phone, name=name, password=make_password(password), is_admin=True)


class User(AbstractBaseUser):
    name = models.CharField(max_length=25, null=False,
                            blank=False, default=True)
    email = models.EmailField(
        max_length=50, null=False, blank=False, unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    password = models.CharField(max_length=1024, null=True, blank=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone"]

    objects = users_manager()

    def __str__(self):
        return self.email

