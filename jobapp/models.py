from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

JOB_CATEGORIES = [
    ('Software', 'Software Development'),
    ('Data', 'Data Science'),
    ('Cloud', 'Cloud Engineer'),
    ('Devops', 'DevOps Engineer'),
    ('Marketing', 'Marketing'),
    ('Design', 'Design'),
    ('Sales', 'Sales'),
    ('HR', 'Human Resources'),
    ('Finance', 'Finance'),
]


class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=JOB_CATEGORIES, default='Software')
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.IntegerField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    posted_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('job', 'applicant')  # ✅ Prevents duplicates at DB level

    def __str__(self):
        return f"{self.name} applied for {self.job.title}"

class Profile(models.Model):
    ROLE_CHOICES = [
        ('jobseeker', 'Job Seeker'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('employer', 'Employer'), ('jobseeker', 'Job Seeker')])

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)