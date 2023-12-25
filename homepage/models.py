from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, user_name, user_email, password=None):
        if not user_name:
            raise ValueError('Users must have a username')
        if not user_email:
            raise ValueError('Users must have an email address')

        user = self.model(
            user_name=user_name,
            user_email=self.normalize_email(user_email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, unique=True)
    user_email = models.EmailField(max_length=254, unique=True)
    objects = UserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['user_email']

    def __str__(self):
        return self.user_name


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=20)
    post_description = models.CharField(max_length=200)
    post_content = models.CharField(max_length=300)
    post_creationdate = models.DateTimeField(default=timezone.now)
    post_ispublic = models.BooleanField(
        default=False)  # renamed from post_type
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_title


class Likes(models.Model):
    likes_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user.user_name} likes {self.post.post_title}'
