from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

class Document(models.Model):

	docfile = models.FileField(upload_to='documents/%Y/%m/%d')
	printJobStatus = models.IntegerField(default=0)




	# filename = models.CharField(max_length=10, default='myfile')
	# # clientId = models.IntegerField()
	# # numPages = models.IntegerField
	# def save(self, *args, **kwargs):
	# 	tmpfilename = self.docfile.split('/')[-1]
	# 	self.filename = tmpfilename[0:10]
	# 	super().save(*args, **kwargs)
