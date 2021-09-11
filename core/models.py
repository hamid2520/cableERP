from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, \
    PermissionsMixin, AnonymousUser
from django.db.models import JSONField
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver


# from notification.models import Message
from django.apps import apps
import uuid
import os
import datetime

# Create your models here.


class ConductiveMaterial(models.Model):

    class Meta:
        verbose_name = "مواد رسانا"
        verbose_name_plural = "مواد های رسانا"

    name = models.CharField(max_length=255, verbose_name='نام')

    def __str__(self):
        return self.name


class NonConductiveMaterial(models.Model):

    class Meta:
        verbose_name = "مواد نارسانا"
        verbose_name_plural = "مواد های نارسانا"

    name = models.CharField(max_length=255, verbose_name='نام')

    def __str__(self):
        return self.name


class Company(models.Model):

    class Meta:
        verbose_name = "شرکت"
        verbose_name_plural = "شرکت ها"

    name = models.CharField(max_length=255, verbose_name='نام')

    def __str__(self):
        return self.name


class Buy(models.Model):

    class Meta:
        verbose_name = "خرید"
        verbose_name_plural = "خرید ها"

    material = models.ForeignKey('ConductiveMaterial', on_delete=models.CASCADE)
    import_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=1)
    company_batch_number = models.IntegerField(default=1)
    company = models.ForeignKey('Company', on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        if not Buy.objects.count():
            self.id = 100
        else:
            self.id = Buy.objects.last().id + 1
        super(Buy, self).save(*args, **kwargs)

    def __str__(self):
        return self.material.name


