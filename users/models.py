from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def _create_user(self, first_name, last_name, email, password, **extra_fields):
        """
        Create and save a user with the given first_name, last_name, email, and password.
        """
        if (not first_name) or (not last_name):
            raise ValueError('The given first_name and last_name must be set')
        email = self.normalize_email(email)
        # username = self.model.normalize_username(username)
        user = self.model(first_name=first_name,
                          last_name=last_name, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        # user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(first_name, last_name, email, password, **extra_fields)

    def create_superuser(self, first_name, last_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(first_name, last_name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Lutan User Model Class

    User.is_staff: 
        Designates whether the user can log into admin sites.
    User.is_active: 
        Designates whether this user should be treated as active.
        Unselect this instead of deleting accounts.

    Args:
        models ([type]): [description]
    """
    objects = CustomUserManager()

    # LOGIN_FIELD
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    first_name = models.CharField(
        _('first name'), max_length=30, null=False, blank=False)
    last_name = models.CharField(
        _('last name'), max_length=150, null=False, blank=False)
    email = models.EmailField(
        _('email address'), null=False, blank=False, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    signature = models.CharField(max_length=255, null=True, blank=True)

    followings = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False,
    )

    blockings = models.ManyToManyField(
        "self", related_name="blockers", symmetrical=False
    )


class UserProxy(User):
    class Meta:
        proxy = True
