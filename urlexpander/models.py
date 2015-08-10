from django.db import models
from django.utils import timezone

class URLExp(models.Model):
	shorturl = models.URLField(blank=True, null=True)
        httpstat = models.PositiveIntegerField(blank=True, null=True)
        finaldestination = models.URLField(blank=True, null=True)
        pagetitle = models.TextField(blank=True, null=True)
	
	def __str__(self):
		return self.shorturl
