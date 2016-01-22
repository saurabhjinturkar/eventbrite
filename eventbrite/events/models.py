from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=255)
	name_localized = models.CharField(max_length=255)
	category_id  = models.IntegerField()

	def __str__(self):
		return self.name + " " + str(self.category_id)

# class Event(models.Model):
# 	name = 