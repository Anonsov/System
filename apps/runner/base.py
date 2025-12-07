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
    
    @abstractmethod
    def prepare_files(self, code):
        """read the name of the function cmon"""
        pass
    
    @abstractmethod
    def get_compile_command(self, docker_file_path):
        """docker command for compiling if needed"""
        pass
    
    @abstractmethod
    def get_run_command(self, docker_file_path, memory_limit):
        """docker run"""
        pass
    
    def cleanup(self):
        """cleaning directories after executing like: .exe and etc"""
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
    
    def get_run_command(self, docker_file_path, memory_limit):
        return [
            "docker", "run", "--rm", "-i", "--network=none",
            f"--memory={memory_limit}m",
            "-v", f"{self.temp_file_path}:{docker_file_path}",
            self.lang_config["docker_image"],
            "python", docker_file_path
        ]


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
    
    def get_run_command(self, docker_file_path, memory_limit):
        return [
            "docker", "run", "--rm", "-i", "--network=none",
            f"--memory={memory_limit}m",
            "-v", f"{self.temp_dir}:/app",
            "-w", "/app",
            self.lang_config["docker_image"],
            "java", "Solver"
        ]
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
    
    def get_run_command(self, docker_file_path, memory_limit):
        return [
            "docker", "run", "--rm", "-i", "--network=none",
            f"--memory={memory_limit}m",
            "-v", f"{self.temp_dir}:/app",
            "-w", "/app",
            self.lang_config["docker_image"],
            "mono", "Program.exe"
        ]
    
    def cleanup(self):
        if self.temp_dir:
            shutil.rmtree(self.temp_dir, ignore_errors=True)          
            
             
class CppRunner(LanguageRunner):
    """cpp runner (deprecated)"""
    
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
    
    def get_run_command(self, docker_file_path, memory_limit):
        return [
            "docker", "run", "--rm", "-i", "--network=none",
            f"--memory={memory_limit}m",
            "-v", f"{self.temp_file_path.replace('.cpp', '.out')}:/code.out",
            self.lang_config["docker_image"],
            "/code.out"
        ]


# main mp
LANGUAGE_RUNNERS = {
    "python": PythonRunner,
    "java": JavaRunner,
    "csharp": CSharpRunner,
    "cpp": CppRunner,
}


class Runner:
    def __init__(self, model):
        self.model = model
        self.base_dir = settings.BASE_DIR  


    def run_all_tests(self, submission_id):
        submission = self.model.objects.get(id=submission_id)
        submission.status = self.model.Status.RUNNING
        submission.save()
        print(f"Submission {submission_id} is running")

        lang_config = LANGUAGES[submission.language]
        runner_class = LANGUAGE_RUNNERS.get(submission.language)
        
        if not runner_class:
            raise ValueError(f"Unsupported language: {submission.language}")
        
        language_runner = runner_class(lang_config)

        testcases_dir = os.path.join(
            self.base_dir,
            "apps", "problems", "testcases", 
            str(submission.problem.uuid), 
            "tests"
        )
        checker_path = os.path.join(
            self.base_dir,
            "apps", "problems", "testcases", 
            str(submission.problem.uuid), 
            "checkers", "checker.py"
        )
        
        test_results = []
        flags = {"TLE": False, "WA": False, "CE": False}
        max_elapsed_time = 0
        solved_count = 0
        test_files = sorted([f for f in os.listdir(testcases_dir) if f.endswith(".in")])

        for filename in test_files:
            test_num = int(filename.split(".")[0])
            input_path = os.path.join(testcases_dir, filename)
            output_path = os.path.join(testcases_dir, f"{test_num}.out")

            with open(input_path, "r") as f:
                input_data = f.read()
            with open(output_path, "r") as f:
                expected_output = f.read()

            result = self._run_single_test(
                language_runner,
                submission.code,
                input_data,
                expected_output,
                submission.problem.time_limit_ms,
                submission.problem.memory_limit_mb,
                test_num,
                checker_path
            )

            test_results.append(result)
            max_elapsed_time = max(max_elapsed_time, result["time"])

            if result["status"] == "TLE":
                flags["TLE"] = True
            elif result["status"] == "WA":
                flags["WA"] = True
            elif result["status"] == "CE":
                flags["CE"] = True
            elif result["status"] == "AC" and not any(flags.values()):
                solved_count += 1

        # overall stuff
        if flags["CE"]:
            overall_status = "CE"
        elif flags["TLE"]:
            overall_status = "TLE"
        elif flags["WA"]:
            overall_status = "WA"
        else:
            overall_status = "AC"

        return {
            "status": overall_status,
            "exec_time_ms": max_elapsed_time,
            "test_results": test_results,
            "score": solved_count
        }

    def _run_single_test(self, language_runner, code, input_data, expected_output,
                         time_limit_ms, memory_limit, test_num, checker_path):
        """for single tests (i use it above - in run_all_tests methof)"""
        try:
            # Prepare files
            docker_file_path = language_runner.prepare_files(code)

            # if lang is not python, compile it
            compile_cmd = language_runner.get_compile_command(docker_file_path)
            if compile_cmd:
                comp = subprocess.run(compile_cmd, text=True, capture_output=True, env=env)
                if comp.returncode != 0:
                    return {
                        "test": test_num,
                        "status": "CE",
                        "stdout": comp.stdout,
                        "stderr": comp.stderr,
                        "time": 0
                    }
                    
                    
            run_cmd = language_runner.get_run_command(docker_file_path, memory_limit)
            start_time = time.perf_counter()
            proc = subprocess.run(
                run_cmd,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=time_limit_ms / 1000,
                env=env
            )
            elapsed_time = time.perf_counter() - start_time

            if proc.returncode != 0:
                return {
                    "test": test_num,
                    "status": "CE",
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
            return {
                "test": test_num,
                "status": "CE",
                "stdout": "",
                "stderr": str(e),
                "time": 0
            }
        finally:
            language_runner.cleanup()

    def _check_output(self, user_output, expected_output, checker_path=None):
        """this part is done by gpt, so i don't know, it just helps for catching the check funciton from checker.py"""
        if checker_path and os.path.exists(checker_path):
            spec = importlib.util.spec_from_file_location("checker", checker_path)
            checker = importlib.util.module_from_spec(spec) #type: ignore 
            spec.loader.exec_module(checker) #type: ignore 
            return checker.check(user_output, expected_output)
        return user_output.strip() == expected_output.strip()