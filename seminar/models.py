from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class UserInformation(models.Model):
    PROFESSION = [
        ('Student', 'Student'),
        ('Job Holder', 'Job Holder'),
        ('businessman', 'businessman'),
        ('Others', 'Others')
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True, default='')

    profession = models.CharField(
        max_length=20, null=True, blank=True, choices=PROFESSION)
    organization = models.CharField(
        max_length=500, blank=True, null=True, default='Unknown')
    image = models.ImageField(blank=True, null=True, upload_to='user images')

    def __str__(self):
        return self.user.email


class Organization(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True, default=' ')
    type = models.CharField(max_length=100, blank=True, null=True, default=' ')
    descriptiion = models.CharField(
        max_length=1000, blank=True, null=True, default='')
    location = models.CharField(
        max_length=500, blank=True, null=True, default='')
    link = models.CharField(max_length=500, blank=True, null=True, default=' ')
    additional_information = models.CharField(
        max_length=1000, blank=True, null=True, default='')

    image = models.ImageField(blank=True, null=True,
                              upload_to='organization images')

    def __str__(self):
        return str(self.name)


class Seminar(models.Model):
    TYPES = [
        ('Conference', 'Conference'),
        ('Seminar', 'Seminar'),
        ('Bootcamp', 'Bootcamp'),
        ('Workshop', 'Workshop'),
        ('Others', 'Others')
    ]
    name = models.CharField(max_length=100, blank=True, null=True, default='')

    type = models.CharField(max_length=20, null=True,
                            blank=True, choices=TYPES)

    category = models.CharField(
        max_length=100, blank=True, null=True, default='Technology')

    location = models.CharField(
        max_length=1000, blank=True, null=True, default='')

    description = models.CharField(
        max_length=1000, blank=True, null=True, default='')

    link = models.CharField(max_length=500, blank=True, null=True, default='')

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    length = models.IntegerField(blank=True, null=True, validators=[
                                 MaxValueValidator(10), MinValueValidator(1)])
    seat = models.IntegerField(blank=True, null=True)

    image = models.ImageField(blank=True, null=True,
                              upload_to='seminar images')

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Registration(models.Model):
    user = models.ForeignKey(
        UserInformation, on_delete=models.SET_NULL, blank=True, null=True)
    seminar = models.ForeignKey(
        Seminar, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
