from django.db import models

# Create your models here.
class User(models.Model):
	gw_id = models.CharField(max_length = 100,default = '123456')
	gw_address = models.CharField(max_length = 100,default = '192.168.1.1')
	mac = models.CharField(max_length = 100,default = '')
	gw_port = models.CharField(max_length = 100,default = '2060')
	url = models.CharField(max_length = 100,default = '')
	token = models.CharField(max_length = 100,default = '')
	stage = models.CharField(max_length = 100,default = '')
	ip = models.CharField(max_length = 100,default = '')
	incoming = models.FloatField(default = 0)
	outgoing = models.FloatField(default = 0)
	def __str__(self):
		return self.mac

class FL_freq(models.Model):
	max_freq = models.FloatField()
	min_freq = models.FloatField()