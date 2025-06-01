from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class City(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Proposal(models.Model):
    title = models.CharField(max_length=250)
    image_url = models.URLField(null=True, blank=True)
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="proposals")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("caera:proposal-detail", kwargs={'pk': self.pk})


class Project(models.Model):
    title = models.CharField(max_length=250)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="projects")
    image_url = models.URLField(null=True, blank=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="projects")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("caera:proposal-detail", kwargs={'pk': self.pk})


class User(AbstractUser):
    pass
