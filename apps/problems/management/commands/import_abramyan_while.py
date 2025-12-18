import os
import importlib.util
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from apps.problems.models import Problem, Tag
from apps.archive.models import BookSection, BookProblem
import logging
logger = logging.getLogger(__name__)


WHILE_ROOT = os.path.join(settings.BASE_DIR, 'Abramyan', 'while')
META = {

    'while1': {
        'title': 'While1',
        'statement': r'Given positive real numbers \(A\) and \(B\) \((A > B)\). A segment of length \(A\) contains the maximum possible number of segments of length \(B\) without overlaps. Without using multiplication and division, find the length of the unused part of segment \(A\).',
        'input_format': r'\(A\)\n\(B\)',
        'output_format': r'Single real: unused length',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while2': {
        'title': 'While2',
        'statement': r'Given positive real numbers \(A\) and \(B\) \((A > B)\). A segment of length \(A\) contains the maximum possible number of segments of length \(B\) without overlaps. Without using multiplication and division, find the number of segments of length \(B\).',
        'input_format': r'\(A\)\n\(B\)',
        'output_format': r'Single integer: number of segments',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while3': {
        'title': 'While3',
        'statement': r'Given positive integers \(N\) and \(K\). Using addition and subtraction only, find the quotient and remainder of integer division \(N\) by \(K\).',
        'input_format': r'\(N\)\n\(K\)',
        'output_format': r'Two integers: quotient and remainder',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while4': {
        'title': 'While4',
        'statement': r'Given an integer \(N > 0\). If \(N\) is an exact power of \(3\), output True; otherwise output False.',
        'input_format': r'\(N\)',
        'output_format': r'True or False',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while5': {
        'title': 'While5',
        'statement': r'Given an integer \(N > 0\) such that \(N = 2^{K}\). Find and output the exponent \(K\).',
        'input_format': r'\(N\)',
        'output_format': r'Single integer: \(K\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while6': {
        'title': 'While6',
        'statement': r'Given an integer \(N > 0\), compute the double factorial \(N!! = N(N-2)(N-4)\dots\). Use a real variable to avoid overflow.',
        'input_format': r'\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'while7': {
        'title': 'While7',
        'statement': r'Given an integer \(N > 0\), find the smallest positive integer \(K\) such that \(K^{2} > N\). Do not use root extraction.',
        'input_format': r'\(N\)',
        'output_format': r'Single integer: \(K\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while8': {
        'title': 'While8',
        'statement': r'Given an integer \(N > 0\), find the largest integer \(K\) such that \(K^{2} \le N\). Do not use root extraction.',
        'input_format': r'\(N\)',
        'output_format': r'Single integer: \(K\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while9': {
        'title': 'While9',
        'statement': r'Given an integer \(N > 1\), find the smallest integer \(K\) such that \(3^{K} > N\).',
        'input_format': r'\(N\)',
        'output_format': r'Single integer: \(K\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while10': {
        'title': 'While10',
        'statement': r'Given an integer \(N > 1\), find the largest integer \(K\) such that \(3^{K} < N\).',
        'input_format': r'\(N\)',
        'output_format': r'Single integer: \(K\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while11': {
        'title': 'While11',
        'statement': r'Given an integer \(N > 1\), find the smallest integer \(K\) such that \(1+2+\dots+K \ge N\). Output \(K\) and the sum.',
        'input_format': r'\(N\)',
        'output_format': r'Two integers: \(K\) and sum',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while12': {
        'title': 'While12',
        'statement': r'Given an integer \(N > 1\), find the largest integer \(K\) such that \(1+2+\dots+K \le N\). Output \(K\) and the sum.',
        'input_format': r'\(N\)',
        'output_format': r'Two integers: \(K\) and sum',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while13': {
        'title': 'While13',
        'statement': r'Given a real number \(A > 1\), find the smallest integer \(K\) such that \(1+\frac12+\dots+\frac1K > A\).',
        'input_format': r'\(A\)',
        'output_format': r'Integer \(K\) and real sum',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'while14': {
        'title': 'While14',
        'statement': r'Given a real number \(A > 1\), find the largest integer \(K\) such that \(1+\frac12+\dots+\frac1K < A\).',
        'input_format': r'\(A\)',
        'output_format': r'Integer \(K\) and real sum',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'while15': {
        'title': 'While15',
        'statement': r'A principal of 1000 euro is invested at \(P\%\) annually \((0 < P < 25)\). Find how many years \(K\) are required for the amount to exceed 1100.',
        'input_format': r'\(P\)',
        'output_format': r'Integer \(K\) and real amount',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'while16': {
        'title': 'While16',
        'statement': r'A skier runs 10 km on the first day and increases the distance by \(P\%\) daily \((0 < P < 50)\). Find the number of days until the total exceeds 200 km.',
        'input_format': r'\(P\)',
        'output_format': r'Integer \(K\) and real total distance',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'while17': {
        'title': 'While17',
        'statement': r'Given an integer \(N > 0\), output all its digits starting from the rightmost digit.',
        'input_format': r'\(N\)',
        'output_format': r'Digits printed line by line',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while18': {
        'title': 'While18',
        'statement': r'Given an integer \(N > 0\), find the count and sum of its digits.',
        'input_format': r'\(N\)',
        'output_format': r'Two integers: count and sum',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while19': {
        'title': 'While19',
        'statement': r'Given an integer \(N > 0\), output the number obtained by reversing its digits.',
        'input_format': r'\(N\)',
        'output_format': r'Single integer',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while20': {
        'title': 'While20',
        'statement': r'Given an integer \(N > 0\), determine whether its decimal representation contains the digit \(2\).',
        'input_format': r'\(N\)',
        'output_format': r'True or False',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while21': {
        'title': 'While21',
        'statement': r'Given an integer \(N > 0\), determine whether its decimal representation contains any odd digit.',
        'input_format': r'\(N\)',
        'output_format': r'True or False',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while22': {
        'title': 'While22',
        'statement': r'Given an integer \(N > 1\), determine whether \(N\) is a prime number.',
        'input_format': r'\(N\)',
        'output_format': r'True or False',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'while23': {
        'title': 'While23',
        'statement': r'Given positive integers \(A\) and \(B\), find their greatest common divisor using the Euclidean algorithm.',
        'input_format': r'\(A\)\n\(B\)',
        'output_format': r'Single integer: GCD',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'while24': {
        'title': 'While24',
        'statement': r'Given an integer \(N > 1\), determine whether it is a Fibonacci number.',
        'input_format': r'\(N\)',
        'output_format': r'True or False',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'while25': {
        'title': 'While25',
        'statement': r'Given an integer \(N > 1\), find the first Fibonacci number greater than \(N\).',
        'input_format': r'\(N\)',
        'output_format': r'Single integer',
        'difficulty': Problem.Difficulty.EASY,
    },

    'while26': {
        'title': 'While26',
        'statement': r'Given a Fibonacci number \(N\), output the previous and next Fibonacci numbers.',
        'input_format': r'\(N\)',
        'output_format': r'Two integers',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'while27': {
        'title': 'While27',
        'statement': r'Given a Fibonacci number \(N\), find its index \(K\).',
        'input_format': r'\(N\)',
        'output_format': r'Single integer',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'while28': {
        'title': 'While28',
        'statement': r'Given \(\varepsilon > 0\), find the smallest index \(K\) such that \(|A_{K} - A_{K-1}| < \varepsilon\), where \(A_{1}=2,\; A_{k}=2+\frac{1}{A_{k-1}}\).',
        'input_format': r'\(\varepsilon\)',
        'output_format': r'Integer \(K\) and two real numbers',
        'difficulty': Problem.Difficulty.HARD,
    },

    'while29': {
        'title': 'While29',
        'statement': r'Given \(\varepsilon > 0\), find the smallest index \(K\) such that \(|A_{K} - A_{K-1}| < \varepsilon\), where \(A_{1}=1,\; A_{2}=2,\; A_{k}=\frac{A_{k-2}+2A_{k-1}}{3}\).',
        'input_format': r'\(\varepsilon\)',
        'output_format': r'Integer \(K\) and two real numbers',
        'difficulty': Problem.Difficulty.HARD,
    },

    'while30': {
        'title': 'While30',
        'statement': r'Given real numbers \(A\), \(B\), \(C\). A rectangle of size \(A \times B\) contains the maximum number of squares of side \(C\). Without using multiplication or division, find the number of squares.',
        'input_format': r'\(A\)\n\(B\)\n\(C\)',
        'output_format': r'Single integer',
        'difficulty': Problem.Difficulty.MEDIUM,
    },
}


class Command(BaseCommand):
    help = "Import Abramyan While1..While30 problems and generate tests via Problem.save()."

    def add_arguments(self, parser):
        parser.add_argument('--start', type=int, default=1)
        parser.add_argument('--end', type=int, default=30)
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--meta-file', help='Optional path to a .py or .json file providing a META mapping (slug -> fields).')
        parser.add_argument('--meta-var', default='META', help='Variable name inside the Python meta file (default: META).')
        parser.add_argument('--update-meta', action='store_true', help='Update Problem text fields from META even if it already exists.')

    def _load_external_meta(self, path: str, var_name: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Meta file not found: {path}")
        if path.endswith('.py'):
            spec = importlib.util.spec_from_file_location('abramyan_meta', path)
            mod = importlib.util.module_from_spec(spec)  # type: ignore
            assert spec and spec.loader
            spec.loader.exec_module(mod)  # type: ignore
            if not hasattr(mod, var_name):
                raise ValueError(f"Variable {var_name} not found in {path}")
            data = getattr(mod, var_name)
            if not isinstance(data, dict):
                raise TypeError(f"{var_name} in {path} must be a dict")
            return data
        elif path.endswith('.json'):
            import json
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise TypeError(f"JSON meta in {path} must be a dict")
            return data
        else:
            raise ValueError('Unsupported meta file type. Use .py or .json')

    def handle(self, *args, **opts):
        start, end, dry = opts['start'], opts['end'], opts['dry_run']
        logger.debug(f"Handle started {start, end, dry}")
        meta_file = opts.get('meta_file')
        meta_var = opts.get('meta_var') or 'META'
        do_update_meta = bool(opts.get('update_meta'))

        effective_meta = dict(META)
        if meta_file:
            try:
                ext_meta = self._load_external_meta(meta_file, meta_var)
                effective_meta.update(ext_meta)
                self.stdout.write(self.style.SUCCESS(f"Loaded META from {meta_file}"))
                logger.debug(f"Successfully added META file")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to load META: {e}"))
                logger.warning(f"Failed to load META")
                return

        tag, _ = Tag.objects.get_or_create(name='while', defaults={'slug': 'while'})
        section, _ = BookSection.objects.get_or_create(slug='while', defaults={'name': 'While'})
        created, updated, linked, failed = 0, 0, 0, []

        for i in range(start, end + 1):
            slug = f'while{i}'
            base = os.path.join(WHILE_ROOT, slug)
            etalon = os.path.join(base, 'etalon_solution.py')
            gen = os.path.join(base, 'generator.py')
            checker = os.path.join(base, 'checker.py')

            if not (os.path.exists(etalon) and os.path.exists(gen)):
                failed.append(f'{slug}: missing generator/etalon')
                continue

            meta = effective_meta.get(slug, {})

            # Manual get-or-new to avoid initial save() before files are assigned
            try:
                p = Problem.objects.get(slug=slug)
                was_created = False
            except Problem.DoesNotExist:
                p = Problem(
                    slug=slug,
                    is_hidden=True,
                    title=meta.get('title', slug.upper()),
                    time_limit_ms=meta.get('time_limit_ms', 2000),
                    memory_limit_mb=meta.get('memory_limit_mb', 256),
                    statement=meta.get('statement', f'{slug.upper()} — auto-imported.'),
                    input_format=meta.get('input_format'),
                    output_format=meta.get('output_format'),
                    difficulty=meta.get('difficulty', Problem.Difficulty.EASY),
                    note=meta.get('note', ''),
                )
                was_created = True

            # Update text fields from META if requested
            if do_update_meta and meta:
                p.title = meta.get('title', p.title)
                p.statement = meta.get('statement', p.statement)
                p.input_format = meta.get('input_format', p.input_format)
                p.output_format = meta.get('output_format', p.output_format)
                p.difficulty = meta.get('difficulty', p.difficulty)
                p.note = meta.get('note', p.note)
                p.time_limit_ms = meta.get('time_limit_ms', p.time_limit_ms)
                p.memory_limit_mb = meta.get('memory_limit_mb', p.memory_limit_mb)
                logger.debug(f"Problem created: {slug}")
            # Attach files BEFORE first save
            with open(etalon, 'rb') as f:
                p.etalon_solution.save('etalon_solution.py', File(f), save=False)
            with open(gen, 'rb') as f:
                p.generator_test.save('generator.py', File(f), save=False)
            if os.path.exists(checker):
                with open(checker, 'rb') as f:
                    p.checker.save('checker.py', File(f), save=False)
            logger.debug("Files attached: checkers, generator, solutions")
            if dry:
                self.stdout.write(self.style.WARNING(f'[dry-run] {slug} ready (would import and link)'))
                continue

            p.save()  # triggers Runner
            p.tags.add(tag)

            # Link to archive section
            if not BookProblem.objects.filter(section=section, problem=p).exists():
                BookProblem.objects.create(section=section, problem=p)
                linked += 1
                logger.debug(f"Connected problem into a BookProblem mmodel")
            created += 1 if was_created else 0
            updated += 0 if was_created else 1
            self.stdout.write(self.style.SUCCESS(f'Imported {slug}'))
            logger.debug(f"Successfully imported {slug}")
        self.stdout.write(self.style.SUCCESS(f'Created={created}, Updated={updated}, Linked={linked}, Failed={len(failed)}'))
        for f in failed:
            self.stdout.write(self.style.ERROR(f))
        logger.debug(f'Created={created}, Updated={updated}, Linked={linked}, Failed={len(failed)}')