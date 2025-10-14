from django.conf import settings
from django.db import models
from django.utils import timezone
import os
import django
import sys
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
    def server_section_score(self):
        """Calculate this server's section score based on weighted factors."""
        # --- weights ---
        employment_weight = 1
        blast_weight = 1
        pitty_weight = 1
        capacity_weight = 1
        random_weight = 1
        # --- formula ---
        score = (
            (self.upsellScore / 10 * blast_weight)
            + (self.length_of_employment ** (1 / (3.5 * employment_weight)))
            + (self.pitty * pitty_weight)
            + ((self.max_guests * capacity_weight) / 2)
            + (r.randint(1, 10 * random_weight))
        )
        # round it for cleaner display
        return round(score, 2)
#--------------------------------

class Section(models.Model):
    Section_ID = models.IntegerField()
    Tables = models.CharField(max_length=50) 
    Guest_count = models.IntegerField()
    Outwork_ID = models.IntegerField()
    Sidework_ID = models.IntegerField()
    Expected_in_time = models.TimeField()

class Outwork:
    Outwork_ID2 = models.IntegerField()
    Section_ID2 = models.IntegerField()
    Outwork_label = models.CharField() 
    Outwork_difficulty = models.IntegerField()

class Sidework:
    Sidework_ID3= models.IntegerField()
    Section_ID3= models.IntegerField()
    Sidework_label= models.CharField()
    Sidework_difficulty= models.IntegerField()

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
