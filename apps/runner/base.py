import tempfile
import os
import subprocess
import importlib.util
import time
from apps.runner.languages import LANGUAGES

env = os.environ.copy()
env["DOCKER_HOST"] = "unix:///var/run/docker.sock"

class Runner:
    def __init__(self, model):
        self.model = model

    def run_all_tests(self, submission_id):
        submission = self.model.objects.get(id=submission_id)
        submission.status = self.model.Status.RUNNING
        submission.save()
        print(submission_id, "is running")

        code = submission.code
        language = submission.language

        time_limit_ms = submission.problem.time_limit_ms
        memory_limit = submission.problem.memory_limit_mb
        uuid = submission.problem.uuid

        testcases_dir = f"apps/problems/testcases/{uuid}/tests"
        checker_path = f"apps/problems/testcases/{uuid}/checker/checker.py"

        test_results = []
        solved_count = 0
        overall_result = {}

        found_TLE = found_WA = found_CE = False
        max_elapsed_time = 0

        directories = sorted(os.listdir(testcases_dir))

        for filename in directories:
            if not filename.endswith(".in"):
                continue

            test_num = int(filename.split(".")[0])
            input_path = os.path.join(testcases_dir, f"{test_num}.in")
            output_path = os.path.join(testcases_dir, f"{test_num}.out")

            with open(input_path, "r") as f:
                input_data = f.read()
            with open(output_path, "r") as f:
                expected_output = f.read()

            lang = LANGUAGES[language]

            # --- Prepare temp file for code ---
            if language == "java":
                temp_dir = tempfile.mkdtemp()
                temp_file_path = os.path.join(temp_dir, "Solver.java")
                with open(temp_file_path, "w") as temp_file:
                    temp_file.write(code)
                docker_file_path = "/app/Solver.java"
                docker_workdir = "/app"
            else:
                with tempfile.NamedTemporaryFile(mode="w", suffix=lang["extension"], delete=False) as temp_file:
                    temp_file.write(code)
                    temp_file.flush()
                    temp_file_path = temp_file.name
                docker_file_path = "/code" + lang["extension"]
                docker_workdir = "/"
                temp_dir = None
            try:
                # --- Compile phase (if needed) ---
                compile_cmd = lang.get("compile")
                if compile_cmd:
                    formatted_compile = [
                        part.format(file=docker_file_path, classname="Solver", exe=docker_file_path.replace(".cs", ".exe"))
                        for part in compile_cmd
                    ]
                    if language == "java":
                        # Mount entire directory for Java
                        comp = subprocess.run(
                            [
                                "docker", "run", "--rm",
                                "-v", f"{temp_dir}:/app",
                                "-w", "/app",
                                lang["docker_image"], *formatted_compile
                            ],
                            text=True,
                            capture_output=True,
                            env=env
                        )
                    else:
                        comp = subprocess.run(
                            [
                                "docker", "run", "--rm",
                                "-v", f"{temp_file_path}:{docker_file_path}",
                                lang["docker_image"], *formatted_compile
                            ],
                            text=True,
                            capture_output=True,
                            env=env
                        )
                                
                    if comp.returncode != 0:
                        found_CE = True
                        test_results.append({
                            "test": test_num,
                            "status": "CE",
                            "stdout": comp.stdout,
                            "stderr": comp.stderr,
                            "time": 0
                        })
                        continue

                # --- Run phase ---
                run_cmd = [
                    part.format(file=docker_file_path, classname="Solver", exe=docker_file_path.replace(".cs", ".exe"))
                    for part in lang["run"]
                ]
                if language == "java":
                    docker_run_cmd = [
                        "docker", "run", "--rm", "-i", "--network=none",
                        f"--memory={memory_limit}m",
                        "-v", f"{temp_dir}:/app",
                        "-w", "/app",
                        lang["docker_image"], *run_cmd
                    ]
                else:
                    docker_run_cmd = [
                        "docker", "run", "--rm", "-i","--network=none",
                        f"--memory={memory_limit}m",
                        "-v", f"{temp_file_path}:{docker_file_path}",
                        lang["docker_image"], *run_cmd
                    ]

                start_time = time.perf_counter()
                print(input_data)
                proc = subprocess.run(
                    docker_run_cmd,
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=time_limit_ms / 1000,
                    env=env
                )
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                max_elapsed_time = max(max_elapsed_time, elapsed_time)

                user_output = proc.stdout

                # If runtime error (for interpreted languages)
                if proc.returncode != 0:
                    found_CE = True
                    test_results.append({
                        "test": test_num,
                        "status": "CE",
                        "stdout": user_output,
                        "stderr": proc.stderr,
                        "time": elapsed_time
                    })
                    continue

                is_correct = self._check_output(user_output, expected_output, checker_path)

                if is_correct:
                    status = "AC"
                    if not (found_WA or found_TLE or found_CE):
                        solved_count += 1
                else:
                    status = "WA"
                    found_WA = True

                test_results.append({
                    "test": test_num,
                    "status": status,
                    "stdout": user_output,
                    "stderr": proc.stderr,
                    "time": elapsed_time
                })

            except subprocess.TimeoutExpired:
                test_results.append({
                    "test": test_num,
                    "status": "TLE",
                    "stdout": "",
                    "stderr": "Time Limit Exceeded",
                    "time": time_limit_ms / 1000
                })
                found_TLE = True
            except Exception as e:
                test_results.append({
                    "test": test_num,
                    "status": "CE",
                    "stdout": "",
                    "stderr": str(e),
                    "time": 0
                })
                found_CE = True
            finally:
                # Clean up temp files
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                if language == "java" and temp_dir:
                    import shutil
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    class_file = temp_file_path.replace(".java", ".class")
                    if os.path.exists(class_file):
                        os.remove(class_file)
                elif os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                exe_file = temp_file_path.replace(".cs", ".exe")
                if os.path.exists(exe_file):
                    os.remove(exe_file)

        # --- Overall result ---
        if found_CE:
            overall_status = "CE"
        elif found_TLE:
            overall_status = "TLE"
        elif found_WA:
            overall_status = "WA"
        else:
            overall_status = "AC"

        overall_result = {
            "status": overall_status,
            "exec_time_ms": max_elapsed_time,
            "test_results": test_results,
            "score": solved_count
        }

        return overall_result

    def _check_output(self, user_output, expected_output, checker_path=None):
        if checker_path and os.path.exists(checker_path):
            spec = importlib.util.spec_from_file_location("checker", checker_path)
            checker = importlib.util.module_from_spec(spec)  # type: ignore
            spec.loader.exec_module(checker)  # type: ignore
            return checker.check(user_output, expected_output)
        else:
            return user_output.strip() == expected_output.strip()