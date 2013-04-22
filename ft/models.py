#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.db import models
from django.utils import timezone

# Create your models here.

class Restaurant(models.Model):
  name = models.CharField(max_length=200, verbose_name="餐厅名", unique=True)

  class Meta:
    verbose_name = '餐厅'

  def __unicode__(self):
    return self.name

class People(models.Model):
  name = models.CharField(max_length=200, verbose_name="姓名", unique=True)

  class Meta:
    verbose_name = '人'

  def __unicode__(self):
    return self.name
 
class Deal(models.Model):
  restaurant = models.ForeignKey(Restaurant, verbose_name="餐厅")
  pay_people = models.ForeignKey(People, verbose_name="付款人", help_text="充值和取现只填付款人, 下面参与人留空")
  deal_date = models.DateTimeField('date dealed', default=timezone.now(), help_text="为避免 django 框架时区处理错误, 时间请统一选中午")
  charge = models.FloatField(default=0, verbose_name="消费", help_text="消费金额, 付款和充值用正的, 取现用负数")
  peoples = models.ManyToManyField(People, related_name='join+', blank=True)

  class Meta:
    verbose_name = '消费记录'
    ordering = ['deal_date']

  def __unicode__(self):
    return self.pay_people.name + " paid " + \
            str(self.charge) + " at " + \
            self.restaurant.name + " on " + \
            self.deal_date.strftime("%Y-%m-%d")

  def get_peoples(self):
    return '\n'.join([p.name for p in self.peoples.all()])

  def per_charge(self):
    if self.peoples.count():
      return self.charge / self.peoples.count()
    else:
      return 0

