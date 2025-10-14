from django.conf import settings
from django.db import models
from django.utils import timezone
import random as r



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


class Section(models.Model):
    Section_ID = models.IntegerField(primary_key=True)
    Tables = models.CharField(max_length=50) 
    Guest_count = models.IntegerField()
    Expected_in_time = models.TimeField()
    Section_score = models.IntegerField(default=0)

    def __str__(self):
        return f"Section {self.Section_ID}"   # fixed lowercase bug


class Outwork(models.Model):   # must inherit from models.Model
    Outwork_ID = models.IntegerField(primary_key=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="outworks")
    Outwork_label = models.CharField(max_length=100)   # added max_length
    Outwork_difficulty = models.IntegerField()

    def __str__(self):
        return self.Outwork_label   # fixed attribute name


class Sidework(models.Model):   # must inherit from models.Model
    Sidework_ID = models.IntegerField(primary_key=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="sideworks")  # unique related_name
    Sidework_label = models.CharField(max_length=100)   # added max_length
    Sidework_difficulty = models.IntegerField()

    def __str__(self):
        return self.Sidework_label   # fixed attribute name


class Host(models.Model):
    Host_ID = models.IntegerField(primary_key=True)
    Host_name = models.CharField(max_length=100)

    def __str__(self):
        return self.Host_name

class Sa(models.Model):
    sa_ID = models.IntegerField(primary_key=True)
    sa_name = models.CharField(max_length=100)

    def __str__(self):
        return self.sa_name
