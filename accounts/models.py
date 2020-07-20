from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid


class MyUserManager(BaseUserManager):
    def create_user(self, username, full_name, phone, password):
        if not username:
            raise ValueError('Users must have an email address')
        if not full_name:
            raise ValueError('Users must have a full name')
        if not phone:
            raise ValueError('Users must have a phone')
        if not password:
            raise ValueError('Password is mandatory to pass')
        elif len(password)<6 or len(password)>18:
            raise ValueError('Password should have a minimum 6 characters and a maximum of 18 characters')

        user = self.model(
            username=self.normalize_email(username),
            full_name=full_name,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, full_name, phone, password):
        user = self.create_user(
            username=self.normalize_email(username),
            full_name=full_name,
            phone=phone,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username 				= models.EmailField(verbose_name="username", max_length=253, unique=True)
    full_name               = models.CharField(verbose_name="fullname", max_length=60)
    phone                   = models.CharField(verbose_name="phone",max_length=20)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    is_blocked              = models.BooleanField(default=False)
    is_disqualified         = models.BooleanField(default=False)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name','phone']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admsin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


class ProfilePic(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    picture = models.FileField(upload_to='profiledps/')
    
    def __str__(self):
        return self.user.username