import tempfile
import os
import subprocess
import importlib.util
import time
import shutil
from abc import ABC, abstractmethod
from apps.runner.languages import LANGUAGES
from django.conf import settings


env = os.environ.copy()
env["DOCKER_HOST"] = "unix:///var/run/docker.sock"


class LanguageRunner(ABC):
    """base class in order to identify lenguages and etc"""

    def __init__(self, lang_config):
        self.lang_config = lang_config
        self.temp_dir = None
        self.temp_file_path = None
        self.container_id = None  

    @abstractmethod
    def prepare_files(self, code):
        """read the name of the function cmon"""
        pass

    @abstractmethod
    def get_compile_command(self, docker_file_path):
        """docker command for compiling if needed"""
        pass

    @abstractmethod
    def get_exec_command(self, docker_file_path):
        """docker exec for running already container"""
        pass

    def _container_mount_args(self):
        """
        return (args:list[str], workdir:str|None) for docker run
        """
        if self.temp_dir:
            return (["-v", f"{self.temp_dir}:/app", "-w", "/app"], "/app")
        if self.temp_file_path:
            # python maps host file to /code.py 
            return (["-v", f"{self.temp_file_path}:/code.py"], None)
        raise RuntimeError("No prepared files to mount (temp_dir/temp_file_path missing)")

    def start_container(self, memory_limit_mb: int):
        """
        start a long-running container once per submission, so each test can use docker exec.
        """
        if self.container_id:
            return self.container_id

        mount_args, _workdir = self._container_mount_args()

        cmd = [
            "docker", "run", "-d", "--rm",
            "--network=none",
            f"--memory={memory_limit_mb}m",
            *mount_args,
            self.lang_config["docker_image"],
            "sh", "-lc", "sleep infinity",
        ]
        p = subprocess.run(cmd, text=True, capture_output=True, env=env)
        if p.returncode != 0:
            raise RuntimeError(f"Failed to start container: {p.stderr.strip() or p.stdout.strip()}")

        self.container_id = p.stdout.strip()
        return self.container_id

    def stop_container(self):
        if not self.container_id:
            return
        subprocess.run(["docker", "rm", "-f", self.container_id], check=False, env=env)
        self.container_id = None

    def exec_in_container(self, exec_args, input_data: str, timeout_sec: float):
        """
        Execute a command in the persistent container.
        exec_args is list[str], like ["python3", "/code.py"] or ["java", "Solver"].
        """
        if not self.container_id:
            raise RuntimeError("Container not started")

        cmd = ["docker", "exec", "-i", self.container_id] + exec_args
        return subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            env=env,
        )

    def cleanup(self):
        """cleaning directories after executing like: .exe and etc"""
        """but firstly i should stop the conatiner, maybe it will use some mounted files"""
        self.stop_container()

        if self.temp_dir:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        elif self.temp_file_path and os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path)


class PythonRunner(LanguageRunner):
    """Read the name of the class"""

    def prepare_files(self, code):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            self.temp_file_path = f.name
        return "/code.py"

    def get_compile_command(self, docker_file_path):
        return None

    def get_exec_command(self, docker_file_path):
        return ["python3", docker_file_path]


class JavaRunner(LanguageRunner):
    """Java runner (shit lang)"""

    def prepare_files(self, code):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file_path = os.path.join(self.temp_dir, "Solver.java")
        with open(self.temp_file_path, "w") as f:
            f.write(code)
        return "/app/Solver.java"

    def get_compile_command(self, docker_file_path):
        return [
            "docker", "run", "--rm",
            "-v", f"{self.temp_dir}:/app",
            "-w", "/app",
            self.lang_config["docker_image"],
            "javac", "Solver.java"
        ]

    def get_exec_command(self, docker_file_path):
        return ["java", "Solver"]


class CSharpRunner(LanguageRunner):
    """cs runner """

    def prepare_files(self, code):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file_path = os.path.join(self.temp_dir, "Program.cs")
        with open(self.temp_file_path, "w") as f:
            f.write(code)
        return "/app/Program.cs"

    def get_compile_command(self, docker_file_path):
        return [
            "docker", "run", "--rm",
            "-v", f"{self.temp_dir}:/app",
            "-w", "/app",
            self.lang_config["docker_image"],
            "mcs", "-out:Program.exe", "Program.cs"
        ]

    def get_exec_command(self, docker_file_path):
        return ["mono", "Program.exe"]


class CppRunner(LanguageRunner):
    """
    cpp runner (deprecated)

    NOTE: This one is still using one-off container execution if you ever enable it.
    You can port it to exec model later (needs mounting compiled binary into /app).
    """

    def prepare_files(self, code):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".cpp", delete=False) as f:
            f.write(code)
            self.temp_file_path = f.name
        return "/code.cpp"

    def get_compile_command(self, docker_file_path):
        return [
            "docker", "run", "--rm",
            "-v", f"{self.temp_file_path}:{docker_file_path}",
            self.lang_config["docker_image"],
            "g++", "-o", "/code.out", docker_file_path
        ]

    def get_exec_command(self, docker_file_path):
        # Not implemented in exec-mode for now
        raise NotImplementedError("CPP exec-mode not implemented")


LANGUAGE_RUNNERS = {
    "python": PythonRunner,
    "java": JavaRunner,
    "csharp": CSharpRunner,
    "cpp": CppRunner,
}


class Runner:
    def __init__(self, model):
        self.model = model
        print("RUNNING---------")
        self.base_dir = settings.BASE_DIR

    def run_all_tests(self, submission_id):
        submission = self.model.objects.get(id=submission_id)
        submission.status = self.model.Status.RUNNING
        submission.save(update_fields=["status"])
        print(f"Submission {submission_id} is running")

        lang_config = LANGUAGES[submission.language]
        runner_class = LANGUAGE_RUNNERS.get(submission.language)
        if not runner_class:
            raise ValueError(f"Unsupported language: {submission.language}")

        language_runner = runner_class(lang_config)

        until_base_dir = os.path.dirname(submission.problem.generator_test.path)
        tests_dir = os.path.join(until_base_dir, "tests")
        checker_path = submission.problem.checker.path

        test_results = []
        flags = {"TLE": False, "WA": False, "CE": False}
        max_elapsed_time = 0.0
        solved_count = 0

        test_files = sorted([f for f in os.listdir(tests_dir) if f.endswith(".in")])

        docker_file_path = None
        compiled_ok = True

        try:
            # for preparing only once
            docker_file_path = language_runner.prepare_files(submission.code)

            # 2) compile once if its compilable language
            compile_cmd = language_runner.get_compile_command(docker_file_path)
            if compile_cmd:
                comp = subprocess.run(compile_cmd, text=True, capture_output=True, env=env)
                if comp.returncode != 0:
                    compiled_ok = False
                    flags["CE"] = True
                    test_results.append({
                        "test": 0,
                        "status": "CE",
                        "stdout": comp.stdout,
                        "stderr": comp.stderr,
                        "time": 0,
                    })

            # 3) start container once if compiled is ok
            if compiled_ok:
                language_runner.start_container(memory_limit_mb=submission.problem.memory_limit_mb)

                # 4) through docker exec run n tests
                for filename in test_files:
                    test_num = int(filename.split(".")[0])
                    input_path = os.path.join(tests_dir, filename)
                    output_path = os.path.join(tests_dir, f"{test_num}.out")

                    with open(input_path, "r") as f:
                        input_data = f.read()
                    with open(output_path, "r") as f:
                        expected_output = f.read()

                    result = self._run_single_test_prepared(
                        language_runner=language_runner,
                        docker_file_path=docker_file_path,
                        input_data=input_data,
                        expected_output=expected_output,
                        time_limit_ms=submission.problem.time_limit_ms,
                        memory_limit=submission.problem.memory_limit_mb,
                        test_num=test_num,
                        checker_path=checker_path,
                    )

                    test_results.append(result)
                    max_elapsed_time = max(max_elapsed_time, float(result.get("time", 0.0)))

                    if result["status"] == "TLE":
                        flags["TLE"] = True
                    elif result["status"] == "WA":
                        flags["WA"] = True
                    elif result["status"] == "CE":
                        flags["CE"] = True
                    elif result["status"] == "AC" and not any(flags.values()):
                        solved_count += 1

        finally:
            #remove the container
            language_runner.cleanup()

        if flags["CE"]:
            overall_status = "CE"
        elif flags["TLE"]:
            overall_status = "TLE"
        elif flags["WA"]:
            overall_status = "WA"
        else:
            overall_status = "AC"

        submission.score = solved_count
        submission.status = overall_status
        submission.test_results = test_results
        submission.exec_time_ms = max_elapsed_time
        submission.save(update_fields=["test_results", "exec_time_ms", "score", "status"])

        self._update_user_score(submission)

        return {
            "status": overall_status,
            "exec_time_ms": max_elapsed_time,
            "test_results": test_results,
            "score": solved_count,
        }

    def _update_user_score(self, submission):
        user = submission.user
        problem = submission.problem
        new_score = submission.score
        max_score_sub = self.model.objects.filter(
            user=user,
            problem=problem
        ).exclude(id=submission.id).order_by('-score').first()

        profile = user.profile

        if not max_score_sub:
            profile.score += new_score
        else:
            max_score = max_score_sub.score
            if new_score > max_score:
                profile.score += (new_score - max_score)

        profile.save()

    def _run_single_test_prepared(
        self,
        language_runner,
        docker_file_path,
        input_data,
        expected_output,
        time_limit_ms,
        memory_limit,
        test_num,
        checker_path,
    ):  
        """let's say files are already prepared and compiled or unned and container is also running"""
        """so we will run a single test there"""
        
        try:
            exec_args = language_runner.get_exec_command(docker_file_path)

            start_time = time.perf_counter()

            # container is already running, this is close to runtime execution.
            # lets add a bit seconds in order to this work good, like just for finding and another things statically
            timeout_sec = (time_limit_ms / 1000) + 0.2

            proc = language_runner.exec_in_container(
                exec_args=exec_args,
                input_data=input_data,
                timeout_sec=timeout_sec,
            )
            elapsed_time = time.perf_counter() - start_time

            if proc.returncode != 0:
                return {
                    "test": test_num,
                    "status": "RE",
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                    "time": elapsed_time
                }

            is_correct = self._check_output(proc.stdout, expected_output, checker_path)
            status = "AC" if is_correct else "WA"

            return {
                "test": test_num,
                "status": status,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "time": elapsed_time
            }

        except subprocess.TimeoutExpired:
            return {
                "test": test_num,
                "status": "TLE",
                "stdout": "",
                "stderr": "Time Limit Exceeded",
                "time": time_limit_ms / 1000
            }
        except Exception as e:
            # This is not necessarily CE; could be internal infra error.
            return {
                "test": test_num,
                "status": "CE",
                "stdout": "",
                "stderr": str(e),
                "time": 0
            }

    def _check_output(self, user_output, expected_output, checker_path=None):
        """this part is done by gpt, so i don't know, it just helps for catching the check funciton from checker.py"""
        if checker_path and os.path.exists(checker_path):
            spec = importlib.util.spec_from_file_location("checker", checker_path)
            checker = importlib.util.module_from_spec(spec)  # type: ignore
            spec.loader.exec_module(checker)  # type: ignore
            return checker.check(user_output, expected_output)
        return user_output.strip() == expected_output.strip()