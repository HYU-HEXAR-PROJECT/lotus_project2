from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from core.models import LotusModel
    
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_arguments):
        """
        creates user with email and password
        """
        if not email:
            raise ValueError("Users must have an valid email address")
        
        now = timezone.now()
        user = self.model(
            email=email,is_staff=False, is_active=True, is_superuser=False, 
            date_joined=now, **extra_arguments
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        su = self.create_user(email, password, **extra_fields)
        su.is_active = True
        su.is_staff = True
        su.is_superuser = True
        su.save(using=self._db)
        return su

class LotusAbstractUser(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(_('staff status'),
                                   default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    email = models.EmailField(_('Email'),
                              max_length=255,
                              db_index=True,
                              unique=True)
    user_name = models.CharField(max_length=255, null=False)
    limit_virtual_server = models.IntegerField(_(u'limit virtual server'), 
                                               default=1, 
                                               help_text=_(u'The number of servers that user can create.'))
    objects = UserManager()
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name',]

    class Meta:
        abstract = True
    
    def get_full_name(self):
        return self.user_name
    
    def get_short_name(self):
        return self.user_name
    
    def get_email(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    
    def get_area(self):
        if not self.family:
            return None
        return self.family.area.area_name

    def __unicode__(self):
        return self.user_name
    
    

class User(LotusAbstractUser):
    class Meta:
        verbose_name=_(u'user')
        verbose_name_plural = _(u'users')        

