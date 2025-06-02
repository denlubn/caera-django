import os
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from slugify import slugify


# from django.utils.text import slugify


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


class Like(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"

    VALUE_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.CharField(max_length=7, choices=VALUE_CHOICES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        unique_together = ("user", "content_type", "object_id")

    def __str__(self):
        return f"{self.user} - {self.value} - {self.content_object}"


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()

    # Generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"Comment by {self.user} on {self.content_object}"


def proposal_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("proposals", filename)


class Proposal(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to=proposal_image_file_path, null=True, blank=True)
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="proposals")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    comments = GenericRelation("Comment")
    likes = GenericRelation("Like")

    def like_count(self):
        return self.likes.filter(value=Like.LIKE).count()

    def dislike_count(self):
        return self.likes.filter(value=Like.DISLIKE).count()

    def get_user_like(self, user):
        if not user.is_authenticated:
            return None
        return self.likes.filter(user=user).first()

    def is_liked_by(self, user):
        like = self.get_user_like(user)
        return like and like.value == Like.LIKE

    def is_disliked_by(self, user):
        like = self.get_user_like(user)
        return like and like.value == Like.DISLIKE

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("caera:proposal-detail", kwargs={'pk': self.pk})


def project_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("projects", filename)


class Project(models.Model):
    title = models.CharField(max_length=250)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="projects")
    image = models.ImageField(upload_to=proposal_image_file_path, null=True, blank=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="projects")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    comments = GenericRelation("Comment")
    likes = GenericRelation("Like")

    def like_count(self):
        return self.likes.filter(value=Like.LIKE).count()

    def dislike_count(self):
        return self.likes.filter(value=Like.DISLIKE).count()

    def get_user_like(self, user):
        if not user.is_authenticated:
            return None
        return self.likes.filter(user=user).first()

    def is_liked_by(self, user):
        like = self.get_user_like(user)
        return like and like.value == Like.LIKE

    def is_disliked_by(self, user):
        like = self.get_user_like(user)
        return like and like.value == Like.DISLIKE


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("caera:project-detail", kwargs={'project_pk': self.pk, 'pk': self.proposal.pk})


class User(AbstractUser):
    pass
