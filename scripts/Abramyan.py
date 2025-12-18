import os
import uuid
from django.conf import settings
from django.core.files import File
from apps.problems.models import Problem, Tag

FOR_ROOT = os.path.join(settings.BASE_DIR, 'Abramyan', 'for')

# Handle all For1..For40
TASKS = [{"slug": f"for{i}"} for i in range(1, 41)]

META = {

    'for1': {
        'title': 'For1',
        'statement': r'Given integers \(K\) and \(N\) \((N > 0)\), print \(K\) exactly \(N\) times, each on a new line.',
        'input_format': r'\(K\)\n\(N\)',
        'output_format': r'\(N\) lines, each line is \(K\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for2': {
        'title': 'For2',
        'statement': r'Given \(A\) and \(B\) \((A < B)\), output all integers from \(A\) to \(B\) inclusive in ascending order, and also output their count \(N\).',
        'input_format': r'\(A\)\n\(B\)',
        'output_format': r'First line: \(N = B - A + 1\). Next \(N\) lines: \(A, A+1, \dots, B\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for3': {
        'title': 'For3',
        'statement': r'Given \(A\) and \(B\) \((A < B)\), output all integers in \((A, B)\) in descending order and output their count \(N\).',
        'input_format': r'\(A\)\n\(B\)',
        'output_format': r'First line: \(N = \max(0, B - A - 1)\). Next \(N\) lines: \(B-1, B-2, \dots, A+1\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for4': {
        'title': 'For4',
        'statement': r'Given price \(P\) for \(1\) kg, output the cost of \(1,2,\dots,10\) kg.',
        'input_format': r'\(P\)',
        'output_format': r'10 lines: \(P\cdot1, P\cdot2, \dots, P\cdot10\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for5': {
        'title': 'For5',
        'statement': r'Given price \(P\) for \(1\) kg, output the cost of \(0.1, 0.2, \dots, 1.0\) kg.',
        'input_format': r'\(P\)',
        'output_format': r'10 lines: \(P\cdot0.1, P\cdot0.2, \dots, P\cdot1.0\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for6': {
        'title': 'For6',
        'statement': r'Given price \(P\) for \(1\) kg, output the cost of \(1.2, 1.4, 1.6, 1.8, 2.0\) kg.',
        'input_format': r'\(P\)',
        'output_format': r'5 lines: \(P\cdot1.2, P\cdot1.4, P\cdot1.6, P\cdot1.8, P\cdot2.0\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for7': {
        'title': 'For7',
        'statement': r'Given \(A\) and \(B\) \((A < B)\), compute \(S = A + (A+1) + \dots + B\).',
        'input_format': r'\(A\)\n\(B\)',
        'output_format': r'Single integer: \(S\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for8': {
        'title': 'For8',
        'statement': r'Given \(A\) and \(B\) \((A < B)\), compute \(P = A\cdot(A+1)\cdot\dots\cdot B\).',
        'input_format': r'\(A\)\n\(B\)',
        'output_format': r'Single real: \(P\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for9': {
        'title': 'For9',
        'statement': r'Given \(A\) and \(B\) \((A < B)\), compute \(S = A^{2} + (A+1)^{2} + \dots + B^{2}\).',
        'input_format': r'\(A\)\n\(B\)',
        'output_format': r'Single integer: \(S\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for10': {
        'title': 'For10',
        'statement': r'Given \(N > 0\), compute \(H_{N} = 1 + \frac{1}{2} + \frac{1}{3} + \dots + \frac{1}{N}\).',
        'input_format': r'\(N\)',
        'output_format': r'Single real: \(H_{N}\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for11': {
        'title': 'For11',
        'statement': r'Given \(N > 0\), compute \(S = N^{2} + (N+1)^{2} + \dots + (2N)^{2}\).',
        'input_format': r'\(N\)',
        'output_format': r'Single integer: \(S\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for12': {
        'title': 'For12',
        'statement': r'Given \(N > 0\), compute the product \(1.1 \cdot 1.2 \cdot 1.3 \cdots\) of \(N\) factors.',
        'input_format': r'\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for13': {
        'title': 'For13',
        'statement': r'Given \(N > 0\), compute the alternating sum \(1.1 - 1.2 + 1.3 - \dots\) of \(N\) terms.',
        'input_format': r'\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for14': {
        'title': 'For14',
        'statement': r'Given \(N > 0\), compute \(N^{2}\) using odd numbers \(1 + 3 + 5 + \dots + (2N-1)\). Output partial sums.',
        'input_format': r'\(N\)',
        'output_format': r'\(N\) lines: \(1^{2}, 2^{2}, \dots, N^{2}\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for15': {
        'title': 'For15',
        'statement': r'Given real \(A\) and integer \(N > 0\), compute \(A^{N}\) as a product.',
        'input_format': r'\(A\)\n\(N\)',
        'output_format': r'Single real: \(A^{N}\)',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for16': {
        'title': 'For16',
        'statement': r'Given real \(A\) and integer \(N > 0\), output \(A^{1}, A^{2}, \dots, A^{N}\).',
        'input_format': r'\(A\)\n\(N\)',
        'output_format': r'\(N\) lines',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for17': {
        'title': 'For17',
        'statement': r'Given real \(A\) and integer \(N > 0\), compute \(S = 1 + A + A^{2} + \dots + A^{N}\).',
        'input_format': r'\(A\)\n\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for18': {
        'title': 'For18',
        'statement': r'Given real \(A\) and integer \(N > 0\), compute \(S = 1 - A + A^{2} - \dots + (-1)^{N}A^{N}\).',
        'input_format': r'\(A\)\n\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for19': {
        'title': 'For19',
        'statement': r'Given \(N > 0\), compute \(N! = 1\cdot2\cdot\dots\cdot N\).',
        'input_format': r'\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for20': {
        'title': 'For20',
        'statement': r'Given \(N > 0\), compute \(S = 1! + 2! + \dots + N!\).',
        'input_format': r'\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for21': {
        'title': 'For21',
        'statement': r'Given \(N > 0\), compute \(1 + \frac{1}{1!} + \frac{1}{2!} + \dots + \frac{1}{N!}\).',
        'input_format': r'\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for22': {
        'title': 'For22',
        'statement': r'Given real \(X\) and integer \(N > 0\), compute \(1 + X + \frac{X^{2}}{2!} + \dots + \frac{X^{N}}{N!}\).',
        'input_format': r'\(X\)\n\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for23': {
        'title': 'For23',
        'statement': r'Given real \(X\) and integer \(N > 0\), compute \(X - \frac{X^{3}}{3!} + \frac{X^{5}}{5!} - \dots\).',
        'input_format': r'\(X\)\n\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for24': {
        'title': 'For24',
        'statement': r'Given real \(X\) and integer \(N > 0\), compute \(1 - \frac{X^{2}}{2!} + \frac{X^{4}}{4!} - \dots\).',
        'input_format': r'\(X\)\n\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for25': {
        'title': 'For25',
        'statement': r'Given real \(X\) \((|X| < 1)\) and integer \(N > 0\), compute \(X - \frac{X^{2}}{2} + \frac{X^{3}}{3} - \dots + (-1)^{N-1}\frac{X^{N}}{N}\).',
        'input_format': r'\(X\)\n\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for26': {
        'title': 'For26',
        'statement': r'Given real \(X\) \((|X| < 1)\) and integer \(N > 0\), compute \(X - \frac{X^{3}}{3} + \frac{X^{5}}{5} - \dots\).',
        'input_format': r'\(X\)\n\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for27': {
        'title': 'For27',
        'statement': r'Given real \(X\) \((|X| < 1)\) and integer \(N > 0\), compute sine series terms.',
        'input_format': r'\(X\)\n\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.HARD,
    },

    'for28': {
        'title': 'For28',
        'statement': r'Given real \(X\) \((|X| < 1)\) and integer \(N > 0\), compute the binomial series for \(\sqrt{1+X}\).',
        'input_format': r'\(X\)\n\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for29': {
        'title': 'For29',
        'statement': r'Given \(N > 1\) and real numbers \(A < B\), divide \([A,B]\) into \(N\) equal parts.',
        'input_format': r'\(N\)\n\(A\)\n\(B\)',
        'output_format': r'First line: \(H = \frac{B-A}{N}\). Next \(N+1\) lines.',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for30': {
        'title': 'For30',
        'statement': r'Given \(N > 1\) and real numbers \(A < B\), compute \(F(x) = 1 - \sin x\) at partition points.',
        'input_format': r'\(N\)\n\(A\)\n\(B\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for31': {
        'title': 'For31',
        'statement': r'Given \(N > 0\), sequence defined by \(A_{0}=2,\; A_{k}=2+\frac{1}{A_{k-1}}\).',
        'input_format': r'\(N\)',
        'output_format': r'\(N\) lines',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for32': {
        'title': 'For32',
        'statement': r'Given \(N > 0\), sequence defined by \(A_{0}=1,\; A_{k}=\frac{A_{k-1}+1}{k}\).',
        'input_format': r'\(N\)',
        'output_format': r'\(N\) lines',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for33': {
        'title': 'For33',
        'statement': r'Given \(N > 0\), Fibonacci numbers \(F_{1}=1,\; F_{2}=1,\; F_{k}=F_{k-1}+F_{k-2}\).',
        'input_format': r'\(N\)',
        'output_format': r'\(N\) lines',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for34': {
        'title': 'For34',
        'statement': r'Given \(N > 1\), sequence defined by \(A_{1}=1,\; A_{2}=2,\; A_{k}=\frac{A_{k-2}+2A_{k-1}}{3}\).',
        'input_format': r'\(N\)',
        'output_format': r'\(N\) lines',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for35': {
        'title': 'For35',
        'statement': r'Given \(N > 2\), sequence defined by \(A_{k}=A_{k-1}+A_{k-2}-2A_{k-3}\).',
        'input_format': r'\(N\)',
        'output_format': r'\(N\) lines',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for36': {
        'title': 'For36',
        'statement': r'Given integers \(N, K > 0\), compute \(S = 1^{K} + 2^{K} + \dots + N^{K}\).',
        'input_format': r'\(N\)\n\(K\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for37': {
        'title': 'For37',
        'statement': r'Given \(N > 0\), compute \(S = 1^{1} + 2^{2} + \dots + N^{N}\).',
        'input_format': r'\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for38': {
        'title': 'For38',
        'statement': r'Given \(N > 0\), compute \(S = 1^{N} + 2^{N-1} + \dots + N^{1}\).',
        'input_format': r'\(N\)',
        'output_format': r'Single real',
        'difficulty': Problem.Difficulty.MEDIUM,
    },

    'for39': {
        'title': 'For39',
        'statement': r'Given integers \(A < B\), output each integer \(k \in [A,B]\) exactly \(k\) times.',
        'input_format': r'\(A\)\n\(B\)',
        'output_format': r'Each number on a new line',
        'difficulty': Problem.Difficulty.EASY,
    },

    'for40': {
        'title': 'For40',
        'statement': r'Given integers \(A < B\), output \(A\) once, \(A+1\) twice, \dots, \(B\) printed incrementally.',
        'input_format': r'\(A\)\n\(B\)',
        'output_format': r'Each number on a new line',
        'difficulty': Problem.Difficulty.EASY,
    },
}


def ensure_tag(name='for'):
    tag, _ = Tag.objects.get_or_create(name=name, defaults={'slug': name})
    return tag


def get_meta(slug: str):
    if slug in META:
        return META[slug]
    # default meta for remaining tasks
    num = int(slug[3:])
    return {
        'title': f'For{num}',
        'statement': f'Abramyan task For{num}',
        'input_format': '',
        'output_format': '',
        'difficulty': Problem.Difficulty.EASY,
    }


def create_problem(slug):
    meta = get_meta(slug)
    p = Problem(
        title=meta['title'],
        statement=meta['statement'],
        input_format=meta['input_format'],
        output_format=meta['output_format'],
        difficulty=meta['difficulty'],
        is_hidden=False,
        note='',
    )

    # Attach files from Abramyan/for/<slug>/ BEFORE first save
    base = os.path.join(FOR_ROOT, slug)
    etalon = os.path.join(base, 'etalon_solution.py')
    gen = os.path.join(base, 'generator.py')
    checker = os.path.join(base, 'checker.py')

    if not (os.path.exists(etalon) and os.path.exists(gen)):
        raise FileNotFoundError(f"Missing generator/etalon for {slug} in {base}")

    with open(etalon, 'rb') as f:
        p.etalon_solution.save('etalon_solution.py', File(f), save=False)
    with open(gen, 'rb') as f:
        p.generator_test.save('generator.py', File(f), save=False)
    if os.path.exists(checker):
        with open(checker, 'rb') as f:
            p.checker.save('checker.py', File(f), save=False)

    # Now save once to trigger Problem.save and Runner
    p.save()

    # Tag it
    tag = ensure_tag('for')
    p.tags.add(tag)

    return p


def main():
    created = []
    for t in TASKS:
        try:
            created.append(create_problem(t['slug']))
        except Exception as e:
            print(f"Failed {t['slug']}: {e}")
    print(f"Created {len(created)} problems")


if __name__ == '__main__':
    main()
