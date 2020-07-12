from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.contrib.auth import get_user_model
from PIL import Image

from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    domain = models.CharField(max_length=40,unique=True)
    email = models.EmailField(max_length=70,blank=True)
    customer = models.BooleanField(default=False)
    reseller = models.BooleanField(default=False)
    logo = models.ImageField(blank=True)
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Reseller(MPTTModel):
    #user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
    Application_name = models.CharField(max_length=40,unique=True)
    reseller_name = models.CharField(max_length=40)
    #reseller_domain = models.CharField(max_length=40)
    #reseller_email = models.EmailField(max_length=70,blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['reseller_name']

    def __str__(self):
        return self.reseller_name


class Customer(models.Model):
    #user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
    Application_name = models.CharField(max_length=40, unique=True)
    customer_name = models.CharField(max_length=40)
    #customer_domain = models.CharField(max_length=40)
    #customer_email = models.EmailField(max_length=70,blank=True)
    reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE, null=True, blank=True, related_name='cust_children')

    def __str__(self):
        return self.customer_name
