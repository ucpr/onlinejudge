from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class AuthUserManager(BaseUserManager):

    def create_user(self, username, email, password):
        """ Create user """
        if not username or not email or not password:
            raise ValueError("Users must have an (username | email | password)")

        user = self.model(username = username,
                          email = email,
                          password = password)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user


class AuthUser(AbstractBaseUser, PermissionsMixin):
    """
    ユーザ情報を管理する
    """
    class Meta:
        verbose_name = 'ユーザ'
        verbose_name_plural = 'ユーザ'

    username = models.CharField(verbose_name='ユーザID',
                                unique=True,
                                max_length=30)
    email = models.EmailField(verbose_name='メールアドレス',
                              null=True,
                              default=None)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(verbose_name='有効フラグ',
                                    default=True)
    is_staff = models.BooleanField(verbose_name='管理サイトアクセス権限',
                                   default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'last_name', 'first_name']
    objects = AuthUserManager()

    def __str__(self):
        return self.last_name + ' ' + self.first_name

