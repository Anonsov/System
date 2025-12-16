from django.core.management.base import BaseCommand
from django.db import transaction

from apps.problems.models import Problem, Tag
from apps.archive.models import BookSection, BookProblem


class Command(BaseCommand):
    help = "Link Problems to BookSection based on slug prefix and optionally attach the corresponding Tag."

    def add_arguments(self, parser):
        parser.add_argument("--prefix", default="for", help='Slug prefix (default: "for").')
        parser.add_argument("--section-name", default="For", help='BookSection name (default: "For").')
        parser.add_argument("--section-slug", default="for", help='BookSection slug (default: "for").')
        parser.add_argument("--tag-name", default="for", help='Tag name to attach (default: "for").')
        parser.add_argument("--attach-tag", action="store_true", help="Also attach the Tag.")
        parser.add_argument("--dry-run", action="store_true", help="Do not write changes.")
        parser.add_argument("--skip-hidden", action="store_true", help="Skip problems with is_hidden=True.")

    @transaction.atomic
    def handle(self, *args, **opts):
        prefix = opts["prefix"].lower()
        section_slug = opts["section_slug"].lower()
        section_name = opts["section_name"]
        tag_name = opts["tag_name"]
        attach_tag = bool(opts["attach_tag"])
        dry_run = bool(opts["dry_run"])
        skip_hidden = bool(opts["skip_hidden"])

        section, _ = BookSection.objects.get_or_create(
            slug=section_slug,
            defaults={"name": section_name},
        )

        tag = None
        if attach_tag:
            tag, _ = Tag.objects.get_or_create(name=tag_name)

        qs = Problem.objects.filter(slug__istartswith=prefix)
        if skip_hidden and hasattr(Problem, "is_hidden"):
            qs = qs.filter(is_hidden=False)

        matched = qs.count()
        linked = 0
        tagged = 0

        for p in qs.iterator():
            # link to section
            exists = BookProblem.objects.filter(section=section, problem=p).exists()
            if not exists:
                linked += 1
                if not dry_run:
                    BookProblem.objects.create(section=section, problem=p)

            # attach tag (optional)
            if attach_tag and tag is not None:
                if not p.tags.filter(id=tag.id).exists(): #type: ignore
                    tagged += 1
                    if not dry_run:
                        p.tags.add(tag)

        if dry_run:
            self.stdout.write(f"[DRY RUN] matched={matched} would_link={linked} would_tag={tagged}")
        else:
            self.stdout.write(f"matched={matched} linked={linked} tagged={tagged}")