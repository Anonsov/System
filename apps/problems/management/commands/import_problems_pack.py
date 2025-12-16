import importlib.util

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from apps.problems.models import Problem, Tag
import os

def load_pack(module_path: str, var_name: str):
    if not os.path.exists(module_path):
        raise CommandError(f"Pack module not found: {module_path}")

    spec = importlib.util.spec_from_file_location("problems_pack", module_path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(mod)  # type: ignore

    if not hasattr(mod, var_name):
        raise CommandError(f"Variable `{var_name}` not found in {module_path}")
    data = getattr(mod, var_name)
    if not isinstance(data, list):
        raise CommandError(f"`{var_name}` must be a list of dicts")
    return data


class Command(BaseCommand):
    help = "Mass import problems from a Python 'pack' (list of dicts) and generate tests via Problem.save()."

    def add_arguments(self, parser):
        parser.add_argument("--module", required=True, help="Path to python file containing pack variable.")
        parser.add_argument("--var", default="for_tasks", help="Variable name inside module (default: for_tasks).")
        parser.add_argument("--hidden", action="store_true", help="Set is_hidden=True on imported problems (requires field).")
        parser.add_argument("--dry-run", action="store_true", help="Only validate, do not write into DB.")

    def handle(self, *args, **opts):
        tasks = load_pack(opts["module"], opts["var"])

        created = 0
        skipped = 0

        for t in tasks:
            title = t["title"].strip()
            # Validate required file paths (Problem.save will need .path)
            for key in ("etalon_solution_path", "generator_path", "checker_path"):
                path = t.get(key)
                if not path or not os.path.exists(path):
                    raise CommandError(f"[{title}] Missing file: {key} -> {path}")

            if opts["dry_run"]:
                self.stdout.write(f"[DRY] {title}")
                continue

            tag_name = t.get("tag") or "imported"
            tag, _ = Tag.objects.get_or_create(name=tag_name)

            p = Problem(
                title=title,
                statement=t["statement"],
                input_format=t.get("input_format"),
                output_format=t.get("output_format"),
                difficulty=t.get("difficulty", Problem.Difficulty.EASY),
                note=t.get("note", ""),
            )

            if hasattr(p, "is_hidden"):
                p.is_hidden = bool(opts["hidden"])

            with open(t["etalon_solution_path"], "rb") as f:
                p.etalon_solution.save(os.path.basename(t["etalon_solution_path"]), File(f), save=False)
            with open(t["generator_path"], "rb") as f:
                p.generator_test.save(os.path.basename(t["generator_path"]), File(f), save=False)
            with open(t["checker_path"], "rb") as f:
                p.checker.save(os.path.basename(t["checker_path"]), File(f), save=False)

            p.save()
            p.tags.add(tag)

            created += 1
            self.stdout.write(self.style.SUCCESS(f"Imported: {title}"))

        self.stdout.write(self.style.SUCCESS(f"Done. created={created}"))