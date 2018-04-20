from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from apps.base.models import ActiveStatusModel
from libs.managers import QueryManager
from libs.utils import get_verification_code


class UserManager(BaseUserManager, QueryManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Email is required')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, ActiveStatusModel):

    class Role:
        CUSTOMER = 1
        ADMIN = 2

        Choices = (
            (CUSTOMER, 'CUSTOMER'),
            (ADMIN, 'ADMIN'),
        )

    class Gender:
        UNKNOWN = 3
        MALE = 1
        FEMALE = 2

        Choices = (
            (UNKNOWN, 'Unknown'),
            (FEMALE, 'Female'),
            (MALE, 'Male')
        )

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    joined_on = models.DateTimeField(_('date joined'), default=timezone.now,
                                     help_text=_('Designates when the user joined the system.'))

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into admin site.'))

    gender = models.IntegerField(_('gender'), choices=Gender.Choices, default=Gender.UNKNOWN)
    address = models.CharField(_('address'), max_length=255, blank=True, null=True)
    phone = models.CharField(_('phone'), max_length=255, blank=True, null=True)
    role = models.IntegerField(default=Role.CUSTOMER)
    verification_code = models.CharField(max_length=6, db_index=True, blank=True, null=True)
    verified = models.BooleanField(default=False, db_index=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def status(self):
        if self.active:
            return "ACTIVE"
        else:
            return "BLOCKED"

    def get_gender(self):
        for choice in User.Gender.Choices:
            if choice[0] == self.gender:
                return choice[1]

    @staticmethod
    def is_exists(email):
        user = User.objects.filter(email=email).first()
        if user:
            return True
        return False

    def generate_code_for_user(self):
        self.verification_code = get_verification_code()
        self.save()
        return self.verification_code
