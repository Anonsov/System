from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .forms import CodeForm


from django.urls import reverse
import shutil
import os
from .utils import Runner
import uuid


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]
    
    title = models.CharField(max_length=200)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, blank=True)

    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)

    time_limit_ms = models.PositiveIntegerField(default=1000)
    memory_limit_mb = models.PositiveIntegerField(default=256)

    statement = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()

    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    etalon_solution = models.FileField(default=None, null=True)
    generator_test = models.FileField(default=None, null=True)
    checker = models.FileField(default=None, null=True)
    
    note = models.TextField(default="")
    
    
    def __get_path(self) -> str:
        directory = "apps/problems/testcases/"
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        directory += str(self.uuid)
        os.makedirs(directory + "/generator")
        os.makedirs(directory + "/solution")
        os.makedirs(directory + "/tests")
        os.makedirs(directory + "/checkers")
        return directory
    
    def __make_etalons(self, etalon_thing, directory: str, is_generator_test=False):
        if etalon_thing:
            if not is_generator_test:
                dest_path = f"{directory}/solution/{os.path.basename(etalon_thing.name)}"
            else:
                os.makedirs(f"{directory}/generator", exist_ok=True)
                dest_path = f"{directory}/generator/{os.path.basename(etalon_thing.name)}"
            with open(dest_path, 'wb+') as destination:
                for chunk in etalon_thing.chunks():
                    destination.write(chunk)
        
            
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        directory = self.__get_path()
        
        #generate etalon_solution file for a new task
        self.__make_etalons(self.etalon_solution, directory)
        
        #generate generator_task file for a new task
        self.__make_etalons(self.generator_test, directory, is_generator_test=True)
        
        solution_path = directory + "/solution/" + self.etalon_solution.name
        generator_path = directory + "/generator/" + self.generator_test.name
        tests_path = directory + "/tests/"
        
        
        ### object runner in order to run files
        runner = Runner(
            solution_path=solution_path,
            generator_path=generator_path,
            tests_path=tests_path,
            score=30
        )
        
        runner.main_generator()

        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        directory = "apps/problems/testcases/" + str(self.uuid)
        deleted_files_directory = "deleted_testcases/"
        
        if not os.path.exists(deleted_files_directory):
            os.makedirs(deleted_files_directory)
        
        if os.path.exists(directory):
            destination = os.path.join(deleted_files_directory, str(self.uuid))
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
    
    
    def __str__(self):
        return self.title

