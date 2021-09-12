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


class Traction(models.Model):

    class Meta:
        verbose_name = "کشش"
        verbose_name_plural = "کشش ها"

    diameter = models.IntegerField(default=0, verbose_name='قطر رشته')
    percentage_of_anneal = models.IntegerField(default=0, verbose_name='درصد انیل')
    resistance = models.IntegerField(default=0, verbose_name='مقاومت DC')
    material = models.ForeignKey('ConductiveMaterial', on_delete=models.CASCADE, verbose_name='جنس رشته')
    final_production = models.IntegerField(default=0, verbose_name='تولید نهایی')
    type_production = models.ForeignKey('TypeProduction', on_delete=models.DO_NOTHING, verbose_name="نوع تولید")

    def __str__(self):
        return self.type_production.name


class TypeProduction(models.Model):

    class Meta:
        verbose_name = "نوع تولید"
        verbose_name_plural = "نوع تولید ها"

    name = models.CharField(max_length=255, verbose_name='نام')

    def __str__(self):
        return self.name


class Extruder(models.Model):

    class Meta:
        verbose_name = "اکسترودر"
        verbose_name_plural = "اکسترودر ها"

    size_a = models.IntegerField(default=0, verbose_name='سایز A * ')
    size_b = models.IntegerField(default=0, verbose_name='سایز B * ')
    layer_thickness = models.IntegerField(default=0, verbose_name='ضخامت لایه')
    spark_voltage = models.IntegerField(default=0, verbose_name='ولتاژ اسپارک kv')
    final_thickness = models.IntegerField(default=0, verbose_name='قطر نهایی')
    final_thickness = models.IntegerField(default=0, verbose_name='قطر نهایی')
    amount_of_material = models.IntegerField(default=0, verbose_name='مواد مصرفی kg/km')
    conductive_material = models.ManyToManyField('ConductiveMaterial', verbose_name='مواد هادی مصرفی')
    non_conductive_material = models.ManyToManyField('NonConductiveMaterial', verbose_name='مواد عایق مصرفی')
    final_production = models.IntegerField(default=0, verbose_name='تولید نهایی')
    type_production = models.ForeignKey('TypeProduction', on_delete=models.DO_NOTHING, verbose_name="نوع تولید")

    def __str__(self):
        return self.type_production.name


class BATZ(models.Model):

    class Meta:
        verbose_name = "بانچر - استدلر - تابنده - زوج کن"
        verbose_name_plural = "بانچر - استدلر - تابنده - زوج کن"

    TYPE_BUNCHER = 0
    TYPE_ESTERANDER = 1
    TYPE_TABANDE = 2
    TYPE_ZOJ = 3

    TYPE_CHOICES = (
        (TYPE_BUNCHER, 'بانچر'),
        (TYPE_ESTERANDER, 'استدلر'),
        (TYPE_TABANDE, 'تابنده'),
        (TYPE_ZOJ, 'زوج کن'),
    )

    type_cart = models.SmallIntegerField(choices=TYPE_CHOICES, default=TYPE_BUNCHER)
    size_a = models.IntegerField(default=0, verbose_name='سایز A * ')
    size_b = models.IntegerField(default=0, verbose_name='سایز B * ')
    resistance = models.IntegerField(default=0, verbose_name='مقاومت DC')
    final_production_size_a = models.IntegerField(default=0, verbose_name='تولید نهایی سایز A *')
    final_production_size_b = models.IntegerField(default=0, verbose_name='تولید نهایی سایز B *')
    type_production = models.ForeignKey('TypeProduction', on_delete=models.DO_NOTHING, verbose_name="نوع تولید")

    def __str__(self):
        return self.type_production.name


class Shape(models.Model):

    class Meta:
        verbose_name = "شکل"
        verbose_name_plural = "شکل ها"

    name = models.CharField(max_length=255, verbose_name='نام')

    def __str__(self):
        return self.name


class CoverMaterial(models.Model):

    class Meta:
        verbose_name = "جنس روکش"
        verbose_name_plural = "جنس روکش ها"

    name = models.CharField(max_length=255, verbose_name='نام')

    def __str__(self):
        return self.name


class FillerMaterial(models.Model):

    class Meta:
        verbose_name = "جنس فیلر"
        verbose_name_plural = "جنس فیلر ها"

    name = models.CharField(max_length=255, verbose_name='نام')

    def __str__(self):
        return self.name


class Production(models.Model):

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصول ها"

    name = models.CharField(max_length=255, verbose_name='نام')
    description = models.TextField(max_length=1054, verbose_name='توضیحات')
    size_a = models.IntegerField(default=0, verbose_name='سایز A * ')
    size_b = models.IntegerField(default=0, verbose_name='سایز B * ')
    conductive = models.ForeignKey('ConductiveMaterial', on_delete=models.CASCADE, verbose_name='هادی مصرفی')
    Shape = models.ForeignKey('Shape', on_delete=models.CASCADE, verbose_name='شکل')
    conductive_size_a = models.IntegerField(default=0, verbose_name='سایز  هادی A * ')
    conductive_size_b = models.IntegerField(default=0, verbose_name='سایز هادی B * ')
    conductive_string = models.IntegerField(default=0, verbose_name='رشته هادی')
    non_conductive = models.ForeignKey('NonConductiveMaterial', on_delete=models.CASCADE, verbose_name='عایق مصرفی')
    cover_material = models.ForeignKey('CoverMaterial', on_delete=models.CASCADE, verbose_name='جنس روکش')
    min_voltage = models.IntegerField(default=0, verbose_name='ولتاژ پایین')
    max_voltage = models.IntegerField(default=0, verbose_name='ولتاژ بالا')
    conductive_weight = models.IntegerField(default=0, verbose_name='وزن هادی')
    filler_material = models.ForeignKey('FillerMaterial', on_delete=models.CASCADE, verbose_name='جنس فیلر')
    traction = models.ManyToManyField('Traction', verbose_name='کشش')
    extruder = models.ManyToManyField('Extruder', verbose_name='اکسترودر')
    batz = models.ManyToManyField('BATZ', verbose_name='بانچر - اترندر - تابنده - زوج کن')


    def __str__(self):
        return self.name
