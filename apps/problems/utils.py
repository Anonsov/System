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
                 score: int):

        self.solution_path = solution_path
        self.generator_path = generator_path
        self.tests_path = tests_path
        self.score = score
        
        
    def input_generator(self):
        ### subprocess version ###
        outputs = subprocess.run(["python3", f"{self.generator_path}"],
                                  capture_output=True,
                                  text=True)
        ### subprocess version ###
        
        try:
            results = json.loads(outputs.stdout.strip())
        except json.JSONDecodeError as e:
            print(f"Error happened while decoding from string to JSON", e)
            results = []
        
        
        for i, test in enumerate(results, start=1):
            lines = test["input"]
            self.write_to_file(lines, self.tests_path, i)
            
            
    def output_generator(self):
        input_files = sorted([f for f in os.listdir(self.tests_path)])
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
                    timeout=1,
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
    
    
    # def show_testcases(self) -> dict:
    #     testcases = {}
    #     for i in range(1, 3):
    #         input_path = f"{self.tests_path}/{i}.in"
    #         output_path = f"{self.tests_path}/{i}.out"
            
    #         input_data = self.open_file_read(input_path)
    #         output_data = self.open_file_read(output_path)
            
    #         testcases[i] = {
    #             "input": input_data,
    #             "output": output_data
    #         }
    #     return testcases
            
            
    # def open_file_read(self, path: str):
    #     with open(path, "r") as f:
    #         content = f.readlines()
    #         return content       
        
        
    def write_to_file(self, lines, tests_path: str, num: int):
        with open(f"{tests_path}/{num}.in", 'w') as f:
            for line in lines:
                f.write(f"{line}\n")
        
        
    def main_generator(self):
        self.input_generator()
        self.output_generator()
        
        
class TestcaseReturner:
    def __init__(self, tests_path: str):
        self.tests_path = tests_path
    
    
    def show_testcases(self) -> dict:
        testcases = {}
        for i in range(2, 5):
            input_path = os.path.join(self.tests_path, f"{i}.in")
            output_path = os.path.join(self.tests_path, f"{i}.out")
            
            input_data = self.open_file_read(input_path)
            output_data = self.open_file_read(output_path)
            
            testcases[i] = {
                "input": input_data,
                "output": output_data
            }
        return testcases
            
            
    def open_file_read(self, path: str):
        with open(path, "r") as f:
            content = f.readlines()
            return content       
        
    