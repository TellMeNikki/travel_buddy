from django.db import models
import re
from datetime import date, datetime


class UserManager(models.Manager):
  def validador_basico(self, postData):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')
    errors = {}

    if len(postData['name']) < 4:
        errors['firstname_len'] = "User name should be at least 4 characters";
    if not EMAIL_REGEX.match(postData['email']):
        errors['email'] = "Invalid E-mail address"
    if not SOLO_LETRAS.match(postData['name']):
        errors['solo_letras'] = "Only letter"
    if len(postData['password']) < 8:
        errors['password'] = "Invalid password, it should be at least 4 characters";
    if postData['password'] != postData['password_confirm'] :
        errors['password_confirm'] = "Passwords didn't match. Please try again "
    return errors


class TravelManager(models.Manager):
  def validador_basico(self, postData): 
    errors={}
    if len(postData['destination']) < 1:
      errors['destination'] = "destination can't be in blank"
    if len(postData['description']) < 4:
      errors['description'] = "tell us what are your plans?"
    if datetime.strptime(postData['s_travel'],"%Y-%m-%d") > datetime.strptime(postData['e_travel'],"%Y-%m-%d"):
      errors['e_travel']="return date must be after depart day" 
    try:
      if datetime.strptime(postData['s_travel'],"%Y-%m-%d")< datetime.today():
          errors['s_travel'] = "the depart must be since today"
    except ValueError:
      errors['s_travel'] = 'You should pick a date'
    try:
      if datetime.strptime(postData['e_travel'],"%Y-%m-%d")< datetime.today():
          errors['e_travel'] = "the return must be after depart"
    except ValueError:
      errors['s_travel'] = 'You should pick a date'
    return errors


class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=CHOICES)
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class Travel(models.Model):
    destination=models.CharField(max_length=45)
    description=models.TextField()
    start_travel=models.DateTimeField()
    end_travel=models.DateTimeField()
    creator=models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE)
    users=models.ManyToManyField(User, related_name="travels")
    created_at=models.DateTimeField(auto_now_add=True)   
    updated_at=models.DateTimeField(auto_now=True)
    objects=TravelManager()

    def __repr__(self):
        return f"User: {self.destination}"