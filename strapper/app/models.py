
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
    email = models.EmailField(default="abc@gmail.com")
    image = models.ImageField(upload_to="user_images/")
    description = models.TextField()
    hash = models.CharField(max_length=256)
    location = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    
    def save(self,*args, **kwargs):
        self.password=get_hash(self.password)
        self.hash = get_hash(self.name+self.password)
        super().save(*args, **kwargs)
        pass
    
class JobOpted(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    jobid = models.ForeignKey(JobPreference,on_delete=models.CASCADE)
    
def get_hash(hash_string):
    return hashlib.sha256(hash_string.encode('utf-8')).hexdigest()
    
    
    