from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Person(models.Model):
    last_name = models.TextField()
    first_name = models.TextField()
    courses = models.ManyToManyField("Course", blank=True)
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    class Meta:
        verbose_name_plural = "People"

class Course(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    
    def __str__(self):
        return f"{self.name}, {self.year}"

    class Meta:
        unique_together = ("name", "year", )

class Grade(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.grade}, {self.person}, {self.course}"

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
    
    
    