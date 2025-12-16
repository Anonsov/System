from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .forms import CodeForm

from django.urls import reverse
import shutil
import os
from .utils import Runner, TestcaseReturner
import uuid
from system import settings

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def upload_to(instance, filename):
    return f"problems/{instance.uuid}/{filename}"


class Problem(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"

    
    title = models.CharField(max_length=200)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, blank=True)

    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.EASY
    )
    time_limit_ms = models.PositiveIntegerField(default=1000)
    memory_limit_mb = models.PositiveIntegerField(default=256)

    statement = models.TextField()
    input_format = models.TextField(null=True)
    output_format = models.TextField(null=True)

    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    etalon_solution = models.FileField(upload_to=upload_to, default=None, null=True)
    generator_test = models.FileField(upload_to=upload_to,default=None, null=True)
    checker = models.FileField(upload_to=upload_to, default=None, null=True)
    score = models.IntegerField(default=0, editable=False)
    is_hidden = models.BooleanField(default=False)
    note = models.TextField(default="", null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        solution_path = self.etalon_solution.path
        generator_path = self.generator_test.path
        base_dir = os.path.dirname(self.generator_test.path)
        tests_path = os.path.join(base_dir, "tests")
        
        runner = Runner(
            solution_path=solution_path,
            generator_path=generator_path,
            tests_path=tests_path,
            timeout=self.time_limit_ms / 1000
        )
        
        runner.main_generator()
        self.score = len(os.listdir(tests_path)) // 2
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        print("XUYNYA")
        directory = os.path.join(settings.PROBLEMS_PATH, str(self.uuid))
        destination = os.path.join(settings.STORAGE_PATH, str(self.slug))
        
        if not os.path.exists(destination):
            os.makedirs(destination)
        
        if os.path.exists(directory):
            shutil.copytree(directory, destination, dirs_exist_ok=True)
            shutil.rmtree(directory)
            
        super().delete(*args, **kwargs)
        
        
    def get_category_slug(self):
        first_tag = self.tags.first()
        if first_tag:
            if not hasattr(first_tag, 'slug') or not first_tag.slug:
                return slugify(first_tag.name)
            return first_tag.slug
        return 'general'
    
    
    def get_absolute_url(self):
        return reverse('problems:detail', kwargs={
            'category_slug': self.get_category_slug(),
            'slug': self.slug
        })
        
        
    def show_testcases(self):
        directory = os.path.join(settings.PROBLEMS_PATH, str(self.uuid))
        tests_path = os.path.join(directory, "tests")
        examples = TestcaseReturner(tests_path=tests_path)
        return examples.show_testcases(limit=3)

        
        
    def __str__(self):
        return self.title

