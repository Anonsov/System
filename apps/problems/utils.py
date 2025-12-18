import os
import shutil
from abc import abstractmethod
import subprocess
import json

class Runner:
    """
    expect path_to_etalon_solution = apps/problems/testcase/<slug>/etalon_solution/etalon_solution.py\n
    expect path_to_generator_test = apps/problems/testcase/<slug>/etalon_solution/generator_test.py\n
    expect etalon_io_path = apps/.../etalon_io_path\n
    expect score as int\n
    """
    def __init__(self, solution_path: str,
                 generator_path: str,
                 tests_path: str,
                 timeout: float):

        self.solution_path = solution_path
        self.generator_path = generator_path
        self.tests_path = os.path.join(tests_path)
        self.timeout = timeout
        
        
    def input_generator(self):
        
        outputs = subprocess.run(["python3", f"{self.generator_path}"],
                                  capture_output=True,
                                  text=True)
        try:
            results = json.loads(outputs.stdout.strip())
            
            os.makedirs(self.tests_path, exist_ok=True)
            
        except json.JSONDecodeError as e:
            print(f"Error happened while decoding from string to JSON", e)
        
        for i, test in enumerate(results, start=1):
            lines = test["input"]
            self.write_to_file(lines, self.tests_path, i)
            

    def output_generator(self):
          
        # Only process input files (*.in) in numeric order
        input_files = sorted(
            [f for f in os.listdir(self.tests_path) if f.endswith('.in')],
            key=lambda name: int(name.split('.')[0])
        )
        
        for input_file in input_files:
            test_num = input_file.split('.')[0]
            input_path = os.path.join(self.tests_path, input_file)
            with open(input_path, 'r') as f:
                input_data = f.read()
            try:
                result = subprocess.run(
                    ["python3", self.solution_path],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                )
                output_path = os.path.join(self.tests_path, f"{test_num}.out")
                with open(output_path, 'w') as f:
                    f.write(result.stdout)
            except subprocess.TimeoutExpired:
                print(f"Timeout on test {test_num}")
                output_path = os.path.join(self.tests_path, f"{test_num}.out")
                with open(output_path, 'w') as f:
                    f.write("TIMEOUT\n")
            except Exception as e:
                print(f"Error running test {test_num}: {e}")
                output_path = os.path.join(self.tests_path, f"{test_num}.out")
                with open(output_path, 'w') as f:
                    f.write(f"ERROR: {str(e)}\n")
                    
        
    def write_to_file(self, lines, tests_path: str, num: int):
        with open(f"{tests_path}/{num}.in", 'w+') as f:
            for line in lines:
                f.write(f"{line}\n")
        
        
    def main_generator(self):
        self.input_generator()
        self.output_generator()
        
        
class TestcaseReturner:
    def __init__(self, tests_path: str):
        self.tests_path = tests_path
    
    
    def show_testcases(self, limit: int = 3) -> dict:
        testcases = {}

        # pick existing *.in tests in numeric order
        in_files = sorted(
            (f for f in os.listdir(self.tests_path) if f.endswith(".in")),
            key=lambda name: int(name.split(".")[0]),
        )

        for fname in in_files[:limit]:
            i = int(fname.split(".")[0])
            input_path = os.path.join(self.tests_path, f"{i}.in")
            output_path = os.path.join(self.tests_path, f"{i}.out")

            # skip not completed pairs
            if not os.path.exists(output_path):
                continue

            input_data = self.open_file_read(input_path)
            output_data = self.open_file_read(output_path)

            testcases[i] = {"input": input_data, "output": output_data}

        return testcases
            
            
    def open_file_read(self, path: str):
        with open(path, "r") as f:
            return f.readlines()


