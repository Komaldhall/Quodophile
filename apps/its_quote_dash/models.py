from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    birth=models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Quote(models.Model):
    author=models.CharField(max_length=100)
    quote=models.TextField()
    like=models.IntegerField(default=0)
    users=models.ForeignKey(User, related_name="posted_by",on_delete=models.CASCADE,blank=True, null=True)
    # job_owner = models.ForeignKey(User, related_name="my_jobs", null=True, blank=True, on_delete=models.CASCADE)
   
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Liked(models.Model):
    users_liked=models.ForeignKey(User, related_name="liked_by",on_delete=models.CASCADE,blank=True, null=True)
    quotes_liked=models.ForeignKey(Quote, related_name="quotes_likedby",on_delete=models.CASCADE,blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)  
