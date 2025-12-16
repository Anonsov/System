from django.db import models
from apps.problems.models import Problem
from django.utils.text import slugify
# Create your models here.

class BookSection(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    
class BookProblem(models.Model):
    section = models.ForeignKey(BookSection, related_name='problems', on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

