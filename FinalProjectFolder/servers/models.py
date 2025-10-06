from django.conf import settings
from django.db import models
from django.utils import timezone


class Server(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    upsellScore = models.IntegerField()
    sectionAssigned = models.CharField(max_length=50)
    timeIn = models.DateTimeField()
    hoursScheduled = models.IntegerField()
    length_of_employment = models.IntegerField()
    max_guests = models.IntegerField()
    pyos = models.IntegerField()
    pitty = models.IntegerField()

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
