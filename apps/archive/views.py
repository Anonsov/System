from typing import Any
from django.views.generic import ListView, DetailView
from .models import BookProblem, BookSection


class ArchiveMainPageView(ListView):
    model = BookSection
    template_name = "archive/archive.html"
    context_object_name = "sections"


class ArchiveSectionDetailView(DetailView):
    model = BookSection
    template_name = "archive/archive_detail.html"
    context_object_name = "section"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["book_problems"] = (
            self.object.problems.select_related("problem").all()  # type: ignore
        )
        return context