from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    sat_score = models.IntegerField(default=0)
    ielts_score = models.FloatField(default=0.0) 
    budget = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile" if self.user else "Unassigned Profile"


class University(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default="Campus Base")
    cost_per_year = models.IntegerField()
    ielts_requirement = models.FloatField(default=6.5)
    sat_requirement = models.IntegerField(default=1200)
    match_status = models.CharField(max_length=50, default="Match")

    living_costs = models.IntegerField(default=15000, help_text="Estimated yearly living expenses")
    scholarship_available = models.BooleanField(default=True)

    acceptance_rate = models.IntegerField(default=15, help_text="Percentage value")
    application_deadline = models.CharField(max_length=100, default="January 15")
    required_essays = models.IntegerField(default=2)

    avg_starting_salary = models.IntegerField(default=75000, help_text="USD per year")
    top_recruiters = models.CharField(max_length=255, default="Google, Microsoft, McKinsey")

    def __str__(self):
        return self.name


class ApplicationDocument(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=50)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doc_type} - {self.profile}"