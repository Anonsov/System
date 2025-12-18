import os
import shutil
import sys

# Ensure project root is in sys.path to import apps.problems.utils
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from apps.problems.utils import Runner

FOR_DIR = os.path.join(BASE_DIR, 'Abramyan', 'for')

TASKS = [f'for{i}' for i in range(1, 41)]  # check For1..For40


def run_task(slug: str):
    task_dir = os.path.join(FOR_DIR, slug)
    gen = os.path.join(task_dir, 'generator.py')
    sol = os.path.join(task_dir, 'etalon_solution.py')
    tests = os.path.join(task_dir, 'tests')

    if not (os.path.exists(gen) and os.path.exists(sol)):
        print(f"[SKIP] {slug}: missing generator or solution")
        return

    # clean tests dir
    if os.path.exists(tests):
        shutil.rmtree(tests)
    os.makedirs(tests, exist_ok=True)

    r = Runner(solution_path=sol, generator_path=gen, tests_path=tests, timeout=2.0)
    r.main_generator()

    ins = sorted(f for f in os.listdir(tests) if f.endswith('.in'))
    outs = sorted(f for f in os.listdir(tests) if f.endswith('.out'))

    print(f"[OK] {slug}: generated {len(ins)} inputs and {len(outs)} outputs -> {tests}")
    # Show first pair
    if ins and outs:
        i0 = ins[0].split('.')[0]
        with open(os.path.join(tests, f"{i0}.in")) as fi, open(os.path.join(tests, f"{i0}.out")) as fo:
            in_preview = ''.join(fi.readlines()[:3]).rstrip()
            out_preview = ''.join(fo.readlines()[:3]).rstrip()
            print(f"  sample {i0}.in ->\n    {in_preview}")
            print(f"  sample {i0}.out ->\n    {out_preview}")


def main():
    for slug in TASKS:
        run_task(slug)


if __name__ == '__main__':
    main()
