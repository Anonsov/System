import os
import importlib.util
import logging

from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings

from apps.problems.models import Problem, Tag
from apps.archive.models import BookSection, BookProblem

logger = logging.getLogger(__name__)

SERIES_ROOT = os.path.join(settings.BASE_DIR, "Abramyan", "series")


META = {
    "series1": {
        "title": "Series1",
        "statement": r"Given ten real numbers, find their sum.",
        "input_format": r"10 real numbers, one per line",
        "output_format": r"Single real: sum",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series2": {
        "title": "Series2",
        "statement": r"Given ten real numbers, find their product.",
        "input_format": r"10 real numbers, one per line",
        "output_format": r"Single real: product",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series3": {
        "title": "Series3",
        "statement": r"Given ten real numbers, find their average.",
        "input_format": r"10 real numbers, one per line",
        "output_format": r"Single real: average",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series4": {
        "title": "Series4",
        "statement": r"An integer \(N\) and a sequence of \(N\) real numbers are given. Output the sum and the product of all elements of this sequence.",
        "input_format": r"\(N\) then \(N\) real numbers, one per line",
        "output_format": r"Two real numbers: sum and product",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series5": {
        "title": "Series5",
        "statement": r"An integer \(N\) and a sequence of \(N\) positive real numbers are given. Output in the same order the integer parts of all elements of this sequence (as real numbers with zero fractional part). Also output the sum of all integer parts.",
        "input_format": r"\(N\) then \(N\) positive real numbers, one per line",
        "output_format": r"\(N\) lines: integer parts. Last line: sum",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series6": {
        "title": "Series6",
        "statement": r"An integer \(N\) and a sequence of \(N\) positive real numbers are given. Output in the same order the fractional parts of all elements of this sequence (as real numbers with zero integer part). Also output the product of all fractional parts.",
        "input_format": r"\(N\) then \(N\) positive real numbers, one per line",
        "output_format": r"\(N\) lines: fractional parts. Last line: product",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series7": {
        "title": "Series7",
        "statement": r"An integer \(N\) and a sequence of \(N\) real numbers are given. Output in the same order the rounded values of all elements of this sequence to the nearest whole number (as integers). Also output the sum of all rounded values.",
        "input_format": r"\(N\) then \(N\) real numbers, one per line",
        "output_format": r"\(N\) lines: rounded integers. Last line: sum",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series8": {
        "title": "Series8",
        "statement": r"An integer \(N\) and a sequence of \(N\) integers are given. Output in the same order all even-valued elements of the sequence and also their amount \(K\).",
        "input_format": r"\(N\) then \(N\) integers, one per line",
        "output_format": r"Even elements in order, one per line; last line: \(K\)",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series9": {
        "title": "Series9",
        "statement": r"An integer \(N\) and a sequence of \(N\) integers are given. Output in the same order the order numbers of all odd-valued elements of the sequence and also their amount \(K\).",
        "input_format": r"\(N\) then \(N\) integers, one per line",
        "output_format": r"Indices (1-based) of odd elements, one per line; last line: \(K\)",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series10": {
        "title": "Series10",
        "statement": r"An integer \(N\) and a sequence of \(N\) integers are given. Output the logical value True if the sequence contains positive-valued elements, otherwise output False.",
        "input_format": r"\(N\) then \(N\) integers, one per line",
        "output_format": r"True or False",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series11": {
        "title": "Series11",
        "statement": r"Integers \(K\), \(N\) and a sequence of \(N\) integers are given. Output False if the sequence contains elements with value less than \(K\), otherwise output True.",
        "input_format": r"\(K\)\n\(N\) then \(N\) integers, one per line",
        "output_format": r"True or False",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series12": {
        "title": "Series12",
        "statement": r"A sequence of nonzero integers terminated by zero is given (the final zero is not an element of the sequence). Output the length of the sequence.",
        "input_format": r"Nonzero integers, one per line, terminated by 0",
        "output_format": r"Single integer: length",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series13": {
        "title": "Series13",
        "statement": r"A sequence of nonzero integers terminated by zero is given. Output the sum of all positive-valued elements of the sequence. If the sequence does not contain the required elements then output 0.",
        "input_format": r"Nonzero integers, one per line, terminated by 0",
        "output_format": r"Single integer: sum of positives",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series14": {
        "title": "Series14",
        "statement": r"An integer \(K\) and a sequence of nonzero integers terminated by zero are given (the final zero is not an element of the sequence). Output the amount of elements whose value less than \(K\).",
        "input_format": r"\(K\) then sequence terminated by 0",
        "output_format": r"Single integer",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series15": {
        "title": "Series15",
        "statement": r"An integer \(K\) and a sequence of nonzero integers terminated by zero are given. Output the order number of the first element whose value greater than \(K\). If the sequence does not contain the required elements then output 0.",
        "input_format": r"\(K\) then sequence terminated by 0",
        "output_format": r"Single integer",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series16": {
        "title": "Series16",
        "statement": r"An integer \(K\) and a sequence of nonzero integers terminated by zero are given. Output the order number of the last element whose value greater than \(K\). If the sequence does not contain the required elements then output 0.",
        "input_format": r"\(K\) then sequence terminated by 0",
        "output_format": r"Single integer",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series17": {
        "title": "Series17",
        "statement": r"A real number \(B\), an integer \(N\) and a sequence of \(N\) real numbers are given. The values of elements are in ascending order. Output the number \(B\) jointly with the elements of the sequence so that all output numbers were in ascending order.",
        "input_format": r"\(B\)\n\(N\) then \(N\) reals in ascending order",
        "output_format": r"\(N+1\) real numbers in ascending order, one per line",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series18": {
        "title": "Series18",
        "statement": r"An integer \(N\) and a sequence of \(N\) integers are given. The values of elements are in ascending order, the sequence may contain equal elements. Output in the same order all distinct elements of the sequence.",
        "input_format": r"\(N\) then \(N\) integers (non-decreasing)",
        "output_format": r"Distinct integers in order, one per line",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series19": {
        "title": "Series19",
        "statement": r"An integer \(N (> 1)\) and a sequence of \(N\) integers are given. Output the elements that are less than their left-side neighbor. Also output the amount \(K\) of such elements.",
        "input_format": r"\(N\) then \(N\) integers",
        "output_format": r"Elements (each on new line), last line: \(K\)",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series20": {
        "title": "Series20",
        "statement": r"An integer \(N (> 1)\) and a sequence of \(N\) integers are given. Output the elements that are less than their right-side neighbor. Also output the amount \(K\) of such elements.",
        "input_format": r"\(N\) then \(N\) integers",
        "output_format": r"Elements (each on new line), last line: \(K\)",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series21": {
        "title": "Series21",
        "statement": r"An integer \(N (> 1)\) and a sequence of \(N\) real numbers are given. Output True if the values of elements are in ascending order, otherwise output False.",
        "input_format": r"\(N\) then \(N\) reals",
        "output_format": r"True or False",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series22": {
        "title": "Series22",
        "statement": r"An integer \(N (> 1)\) and a sequence of \(N\) real numbers are given. Output 0 if the values of elements are in descending order, otherwise output the order number of the first element that breaks the required order.",
        "input_format": r"\(N\) then \(N\) reals",
        "output_format": r"Single integer",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series23": {
        "title": "Series23",
        "statement": r"An integer \(N (> 2)\) and a sequence of \(N\) real numbers are given. A sequence is called a sawtooth one if each inner element is either greater or less than both of its neighbors (each inner element is a tooth). Output 0 if the sequence is a sawtooth one, otherwise output the order number of the first element that is not a tooth.",
        "input_format": r"\(N\) then \(N\) reals",
        "output_format": r"Single integer",
        "difficulty": Problem.Difficulty.HARD,
    },
    "series24": {
        "title": "Series24",
        "statement": r"An integer \(N\) and a sequence of \(N\) integers are given. The sequence contains at least two zero-valued elements. Output the sum of the values of elements placed between two last zero-valued elements. If two last zero-valued elements are placed side by side then output 0.",
        "input_format": r"\(N\) then \(N\) integers",
        "output_format": r"Single integer",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series25": {
        "title": "Series25",
        "statement": r"An integer \(N\) and a sequence of \(N\) integers are given. The sequence contains at least two zero-valued elements. Output the sum of the values of elements placed between the first and the last zero-valued elements. If the first and the last zero-valued elements are placed side by side then output 0.",
        "input_format": r"\(N\) then \(N\) integers",
        "output_format": r"Single integer",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series26": {
        "title": "Series26",
        "statement": r"Positive integers \(K\), \(N\) and a sequence of \(N\) real numbers \(A_1,\dots,A_N\) are given. For each element output its value raised to the power \(K\).",
        "input_format": r"\(K\)\n\(N\) then \(N\) reals",
        "output_format": r"\(N\) real numbers, one per line",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series27": {
        "title": "Series27",
        "statement": r"An integer \(N\) and a sequence of \(N\) real numbers \(A_1,\dots,A_N\) are given. Output \(A_1, A_2^2, \dots, A_{N-1}^{N-1}, A_N^N\).",
        "input_format": r"\(N\) then \(N\) reals",
        "output_format": r"\(N\) real numbers, one per line",
        "difficulty": Problem.Difficulty.HARD,
    },
    "series28": {
        "title": "Series28",
        "statement": r"An integer \(N\) and a sequence of \(N\) real numbers \(A_1,\dots,A_N\) are given. Output \(A_1^N, A_2^{N-1}, \dots, A_{N-1}^2, A_N^1\).",
        "input_format": r"\(N\) then \(N\) reals",
        "output_format": r"\(N\) real numbers, one per line",
        "difficulty": Problem.Difficulty.HARD,
    },
    "series29": {
        "title": "Series29",
        "statement": r"Integers \(K\), \(N\) and \(K\) sequences of integers are given. Each given sequence contains \(N\) elements. Find the total sum of all elements of all given sequences.",
        "input_format": r"\(K\)\n\(N\) then \(K\cdot N\) integers, one per line",
        "output_format": r"Single integer",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series30": {
        "title": "Series30",
        "statement": r"Integers \(K\), \(N\) and \(K\) sequences of integers are given, each with \(N\) elements. Find the sum of elements for each given sequence.",
        "input_format": r"\(K\)\n\(N\) then \(K\cdot N\) integers, one per line",
        "output_format": r"\(K\) lines: sums",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series31": {
        "title": "Series31",
        "statement": r"Integers \(K\), \(N\) and \(K\) sequences of integers are given. Each given sequence contains \(N\) elements. Find the amount of sequences containing an element with the value 2.",
        "input_format": r"\(K\)\n\(N\) then \(K\cdot N\) integers, one per line",
        "output_format": r"Single integer",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series32": {
        "title": "Series32",
        "statement": r"Integers \(K\), \(N\) and \(K\) sequences of integers are given. Each given sequence contains \(N\) elements. Output the order number of the first element with the value 2 for each given sequence (or 0 if no 2 in a sequence).",
        "input_format": r"\(K\)\n\(N\) then \(K\cdot N\) integers, one per line",
        "output_format": r"\(K\) lines",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series33": {
        "title": "Series33",
        "statement": r"Integers \(K\), \(N\) and \(K\) sequences of integers are given. Each given sequence contains \(N\) elements. Output the order number of the last element with the value 2 for each given sequence (or 0 if no 2 in a sequence).",
        "input_format": r"\(K\)\n\(N\) then \(K\cdot N\) integers, one per line",
        "output_format": r"\(K\) lines",
        "difficulty": Problem.Difficulty.EASY,
    },
    "series34": {
        "title": "Series34",
        "statement": r"Integers \(K\), \(N\) and \(K\) sequences of integers are given. Output the sum of elements of each sequence if it contains a 2, otherwise output 0.",
        "input_format": r"\(K\)\n\(N\) then \(K\cdot N\) integers, one per line",
        "output_format": r"\(K\) lines",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series35": {
        "title": "Series35",
        "statement": r"An integer \(K\) and \(K\) sequences of nonzero integers are given. Each sequence is terminated by 0 (not an element). Output the length of each sequence and also the total length.",
        "input_format": r"\(K\) then \(K\) sequences terminated by 0",
        "output_format": r"\(K\) lines: lengths; last line: total",
        "difficulty": Problem.Difficulty.MEDIUM,
    },
    "series36": {
        "title": "Series36",
        "statement": r"An integer \(K\) and \(K\) sequences of nonzero integers are given. Each sequence has at least two elements and is terminated by 0. Output the amount of sequences whose elements are in ascending order.",
        "input_format": r"\(K\) then \(K\) sequences terminated by 0",
        "output_format": r"Single integer",
        "difficulty": Problem.Difficulty.HARD,
    },
    "series37": {
        "title": "Series37",
        "statement": r"An integer \(K\) and \(K\) sequences of nonzero integers are given. Each sequence has at least two elements and is terminated by 0. Output the amount of sequences whose elements are in ascending or in descending order.",
        "input_format": r"\(K\) then \(K\) sequences terminated by 0",
        "output_format": r"Single integer",
        "difficulty": Problem.Difficulty.HARD,
    },
    "series38": {
        "title": "Series38",
        "statement": r"An integer \(K\) and \(K\) sequences of nonzero integers are given. Each sequence has at least two elements and is terminated by 0. For each sequence output 1 if ascending, −1 if descending, otherwise 0.",
        "input_format": r"\(K\) then \(K\) sequences terminated by 0",
        "output_format": r"\(K\) lines",
        "difficulty": Problem.Difficulty.HARD,
    },
    "series39": {
        "title": "Series39",
        "statement": r"An integer \(K\) and \(K\) sequences of nonzero integers are given. Each sequence has at least three elements and is terminated by 0. Output the amount of sawtooth sequences.",
        "input_format": r"\(K\) then \(K\) sequences terminated by 0",
        "output_format": r"Single integer",
        "difficulty": Problem.Difficulty.HARD,
    },
    "series40": {
        "title": "Series40",
        "statement": r"An integer \(K\) and \(K\) sequences of nonzero integers are given. Each sequence has at least three elements and is terminated by 0. For each sequence output its length if it is sawtooth, otherwise output the order number of its first element that is not a tooth.",
        "input_format": r"\(K\) then \(K\) sequences terminated by 0",
        "output_format": r"\(K\) lines",
        "difficulty": Problem.Difficulty.HARD,
    },
}


class Command(BaseCommand):
    help = "Import Abramyan Series1..Series40 problems and generate tests via Problem.save()."

    def add_arguments(self, parser):
        parser.add_argument("--start", type=int, default=1)
        parser.add_argument("--end", type=int, default=40)
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument(
            "--meta-file",
            help="Optional path to a .py or .json file providing a META mapping (slug -> fields).",
        )
        parser.add_argument(
            "--meta-var",
            default="META",
            help="Variable name inside the Python meta file (default: META).",
        )
        parser.add_argument(
            "--update-meta",
            action="store_true",
            help="Update Problem text fields from META even if it already exists.",
        )

    def _load_external_meta(self, path: str, var_name: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Meta file not found: {path}")
        if path.endswith(".py"):
            spec = importlib.util.spec_from_file_location("abramyan_meta_series", path)
            mod = importlib.util.module_from_spec(spec)  # type: ignore
            assert spec and spec.loader
            spec.loader.exec_module(mod)  # type: ignore
            if not hasattr(mod, var_name):
                raise ValueError(f"Variable {var_name} not found in {path}")
            data = getattr(mod, var_name)
            if not isinstance(data, dict):
                raise TypeError(f"{var_name} in {path} must be a dict")
            return data
        if path.endswith(".json"):
            import json

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise TypeError(f"JSON meta in {path} must be a dict")
            return data
        raise ValueError("Unsupported meta file type. Use .py or .json")

    def handle(self, *args, **opts):
        start, end, dry = opts["start"], opts["end"], opts["dry_run"]
        meta_file = opts.get("meta_file")
        meta_var = opts.get("meta_var") or "META"
        do_update_meta = bool(opts.get("update_meta"))

        logger.info("Importing Abramyan Series problems", extra={"range": f"{start}-{end}", "dry_run": dry})

        effective_meta = dict(META)
        if meta_file:
            try:
                ext_meta = self._load_external_meta(meta_file, meta_var)
                effective_meta.update(ext_meta)
                self.stdout.write(self.style.SUCCESS(f"Loaded META from {meta_file}"))
                logger.info("Loaded external META", extra={"meta_file": meta_file, "count": len(ext_meta)})
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to load META: {e}"))
                logger.info("Failed to load META", extra={"meta_file": meta_file})
                return

        tag, _ = Tag.objects.get_or_create(name="series", defaults={"slug": "series"})
        section, _ = BookSection.objects.get_or_create(slug="series", defaults={"name": "Series"})

        created, updated, linked, failed = 0, 0, 0, []

        for i in range(start, end + 1):
            slug = f"series{i}"
            base = os.path.join(SERIES_ROOT, slug)
            etalon = os.path.join(base, "etalon_solution.py")
            gen = os.path.join(base, "generator.py")
            checker = os.path.join(base, "checker.py")

            if not (os.path.exists(etalon) and os.path.exists(gen)):
                failed.append(f"{slug}: missing generator/etalon")
                logger.info("Missing generator/etalon", extra={"slug": slug, "base": base})
                continue

            meta = effective_meta.get(slug, {})

            try:
                try:
                    p = Problem.objects.get(slug=slug)
                    was_created = False
                except Problem.DoesNotExist:
                    p = Problem(
                        slug=slug,
                        is_hidden=True,
                        title=meta.get("title", slug.upper()),
                        time_limit_ms=meta.get("time_limit_ms", 2000),
                        memory_limit_mb=meta.get("memory_limit_mb", 256),
                        statement=meta.get("statement", f"{slug.upper()} — auto-imported."),
                        input_format=meta.get("input_format"),
                        output_format=meta.get("output_format"),
                        difficulty=meta.get("difficulty", Problem.Difficulty.EASY),
                        note=meta.get("note", ""),
                    )
                    was_created = True

                if do_update_meta and meta:
                    p.title = meta.get("title", p.title)
                    p.statement = meta.get("statement", p.statement)
                    p.input_format = meta.get("input_format", p.input_format)
                    p.output_format = meta.get("output_format", p.output_format)
                    p.difficulty = meta.get("difficulty", p.difficulty)
                    p.note = meta.get("note", p.note)
                    p.time_limit_ms = meta.get("time_limit_ms", p.time_limit_ms)
                    p.memory_limit_mb = meta.get("memory_limit_mb", p.memory_limit_mb)

                with open(etalon, "rb") as f:
                    p.etalon_solution.save("etalon_solution.py", File(f), save=False)
                with open(gen, "rb") as f:
                    p.generator_test.save("generator.py", File(f), save=False)
                if os.path.exists(checker):
                    with open(checker, "rb") as f:
                        p.checker.save("checker.py", File(f), save=False)

                if dry:
                    self.stdout.write(self.style.WARNING(f"[dry-run] {slug} ready"))
                    continue

                p.save()
                p.tags.add(tag)

                if not BookProblem.objects.filter(section=section, problem=p).exists():
                    BookProblem.objects.create(section=section, problem=p)
                    linked += 1

                if was_created:
                    created += 1
                else:
                    updated += 1

                self.stdout.write(self.style.SUCCESS(f"Imported {slug}"))
                logger.info("Imported series problem", extra={"slug": slug, "was_created": was_created})
            except Exception as e:
                failed.append(f"{slug}: {e}")
                self.stdout.write(self.style.ERROR(f"Failed {slug}: {e}"))
                logger.info("Failed importing series problem", extra={"slug": slug})

        self.stdout.write(self.style.SUCCESS(f"Created={created}, Updated={updated}, Linked={linked}, Failed={len(failed)}"))
        for f in failed:
            self.stdout.write(self.style.ERROR(f))

        logger.info(
            "Series import finished",
            extra={"created": created, "updated": updated, "linked": linked, "failed": len(failed)},
        )
