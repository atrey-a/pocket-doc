from django.db import models
import uuid

class Gender(models.TextChoices):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'

class Language(models.TextChoices):
    ENGLISH = 'English'
    HINDI = 'Hindi'
    TAMIL = 'Tamil'
    TELUGU = 'Telugu'
    KANNADA = 'Kannada'
    MALAYALAM = 'Malayalam'
    BENGALI = 'Bengali'
    GUJARATI = 'Gujarati'
    MARATHI = 'Marathi'
    ORIYA = 'Oriya'
    PUNJABI = 'Punjabi'

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, auto_created=True, default = uuid.uuid4, editable=False, unique=True)
    client_id = models.CharField(db_index=True, max_length=50, null=True)
    name = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=20,choices=Gender.choices, null=True)
    age = models.IntegerField(null=True)
    mobile = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=100, null=True)
    symptoms = models.CharField(max_length=1000, null=True)
    diagnosis = models.CharField(max_length=1000, null=True)
    preferred_language = models.CharField(max_length=20,choices=Language.choices, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
