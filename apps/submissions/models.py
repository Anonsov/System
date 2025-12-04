from django.db import models
from apps.problems.forms import CodeForm
from django.contrib.auth.models import User
# Create your models here.

def user_submission_path(instance, filename):
    return f"submissions/{instance.user.id}/{instance.id}/{filename}"


class Submission(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        RUNNING = "RUNNING", "Running"
        ACCEPTED = "AC", "Accepted"
        WRONG_ANSWER = "WA", "Wrong Answer"
        TIME_LIMIT = "TLE", "Time Limit Exceeded"
        RUNTIME_ERROR = "RE", "Runtime Error"
        MEMORY_LIMIT = "MLE", "Memory Limit Exceeded"
        COMPILATION_ERROR = "CE", "Compilation Error"
        SYSTEM_ERROR = "SE", "System Error"
    
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    problem = models.ForeignKey("problems.Problem", on_delete=models.CASCADE, related_name="submissions")
    code = models.TextField(null=True)
    language = models.CharField(max_length=100, choices=CodeForm.LanguageChoices.choices)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.PENDING)
    exec_time_ms = models.FloatField(null=True, blank=True)
    memory_kb = models.FloatField(null=True, blank=True)
    
    score = models.IntegerField(default=0)
    output = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        db_table = "problems_submission"
        
        
    def __str__(self):
        return f"Submission {self.id} by {self.user.username}"