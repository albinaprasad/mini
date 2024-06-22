
from django.db import models

import hashlib

class JobPreference(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    job_code = models.CharField(max_length=6)

class User(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, default="abc")
    password = models.CharField(max_length=100, blank=False, default="abc")
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to="user_images/")
    description = models.TextField()
    hash = models.CharField(max_length=256,unique=True)
    location = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    
    def save(self,*args, **kwargs):
        self.password=get_hash(self.password)
        self.hash = get_hash(self.name+self.password+self.email)
        super().save(*args, **kwargs)
        pass
    
class JobOpted(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    jobid = models.ForeignKey(JobPreference,on_delete=models.CASCADE)
    
class Jobs(models.Model):
    title=models.CharField(max_length=256)
    description = models.TextField()
    location = models.CharField(max_length=100)
    link = models.TextField()
    company = models.CharField(max_length=200)
    job_type = models.ForeignKey(JobPreference,on_delete=models.CASCADE)

class Review(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.IntegerField(default=0)
    
def get_hash(hash_string):
    return hashlib.sha256(hash_string.encode('utf-8')).hexdigest()
    
    