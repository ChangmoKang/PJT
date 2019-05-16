from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

# followers 부분은 무조건 followers여야 한다.
# A(User)가 B(followers)라는 정보를 가지고 있을 때,
# A의 안에 있는 B가 A의 follower라는 사실은 무조건 성립하지만
# A가 B를 항상 following한다고 볼 수는 없다.

class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')
    watch = models.CharField(default='', max_length=300)
    
    def __str__(self):
        return self.username