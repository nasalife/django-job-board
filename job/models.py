from django.db import models

# Create your models here.
''' 
 Django model field : 
     - html widget 
     - validation 
     - db size 
'''
JOB_TYPE = (
        ('full time','part time'),
        ('part time','full time'),
)
class Job(models.Model): # table
        title = models.CharField(max_length=100)    #culumn
        # Location 
        job_type  = models.CharField(max_length=15, choices=JOB_TYPE)
        description = models.TextField(max_length=1000)
        published_at = models.DateTimeField(auto_now=True)
        vacancy = models.IntegerField(default=1)
        salary = models.IntegerField(default=0)
        experience = models.IntegerField(default=1)
        category = models.ForeignKey('Category',on_delete=models.CASCADE)
        def __str__(self): 
                return self.title
        
class Category(models.Model):
        name =models.CharField(max_length=25)

        def __str__(self):
                return self.name




        




