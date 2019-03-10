from django.db import models
import datetime
import hashlib
from django.db.models import Max
import random
from django.db.models import Count

class profiles(models.Model):
    resumeId = models.CharField(max_length=255)
    resume = models.TextField()
    tempUserId = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        _resume = self.resume
        _resume = _resume.replace('\\n|\n','<br/>')
        self.resume = _resume
        super(profiles, self).save(*args, **kwargs)


class intermidiate(models.Model):
    resumeId = models.CharField(max_length=255)
    userName = models.CharField(max_length=255)
    tempUserId = models.CharField(max_length=255)
    resume = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class processed(models.Model):
    resumeId = models.CharField(max_length=255)
    userName = models.CharField(max_length=255)
    approverName = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    resume = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class temp_annotated_data(models.Model):
    resumeId = models.CharField(max_length=255)
    userName = models.CharField(max_length=255)
    tagId = models.CharField(max_length=255)
    annotaedData = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

class approver_annotated_data(models.Model):
    resumeId = models.CharField(max_length=255)
    userName = models.CharField(max_length=255)
    approverName = models.CharField(max_length=255)
    tagId = models.CharField(max_length=255)
    annotaedData = models.CharField(max_length=5000)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    

class user(models.Model):
    userName = models.CharField(max_length=255)
    loginKey = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if None ==  self.id and self.loginKey == "9d0a7445f26ddcb89ef2f3ed05cb6380":  # for post call
            username = self.userName + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("saving ---->" , username)
            username = username.encode('utf-8')
            hash_object = hashlib.md5(username)
            self.loginKey = hash_object.hexdigest()    
            super(user, self).save(*args, **kwargs)
        else:  # to update the database
            print("update ---->" , self)
            self.loginKey = ""
            super(user, self).save(*args, **kwargs) 
             