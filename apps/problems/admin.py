from django.contrib import admin

from .models import Tag, Problem, Submission

admin.site.register(Tag)
admin.site.register(Problem)
admin.site.register(Submission)


