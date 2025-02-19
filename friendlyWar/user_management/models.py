from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


# Define user

class UserAvatar(models.Model):
    """This model define user avatar for the application."""
    
    avatarName = models.CharField(_("avatar name"), max_length=50)
    avatar = models.ImageField(_("avatar"), upload_to="images/avatars/")
    
    def __str__(self):
        return self.avatarName


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """This model define users for the application."""
    
    username = models.CharField(_("username"), max_length=50, unique=True)
    email = models.EmailField(_("email"), unique=True)
    UserAvatar = models.ForeignKey(UserAvatar, verbose_name=_("avatar"), on_delete=models.CASCADE, blank=True, null=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username


class Matches(models.Model):
    """This model define matches for the application."""
    
    match_id = models.AutoField(_("match id"), primary_key=True)
    team1 = models.ForeignKey(CustomUser, verbose_name=_("team1"), related_name="team1_user", on_delete=models.CASCADE)
    team2 = models.ForeignKey(CustomUser, verbose_name=_("team2"), related_name="team2_user", on_delete=models.CASCADE)
    winner = models.ForeignKey(CustomUser, verbose_name=_("winner"), related_name="user_won",on_delete=models.CASCADE, blank=True, null=True)
    update_by = models.ForeignKey(CustomUser, verbose_name=_("update by"), related_name="updater",on_delete=models.CASCADE)
    date = models.DateTimeField(_("date"), auto_now_add=True)
    
    def __str__(self):
        return f"{self.team1} vs {self.team2}"
    