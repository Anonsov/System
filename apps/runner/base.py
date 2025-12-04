import tempfile, os
import subprocess
import importlib.util
import time


class Runner:
    def __init__(self, model):
        self.model = model
    
    # def run_all_tests(self,submission_id):
    #     submission = self.model.objects.get(id=submission_id)
    #     submission.status = self.model.Status.RUNNING
    #     submission.save(update_fields=["status"])
    #     code = submission.code
    #     language = submission.language
    #     timeout = submission.exec_time_ms
    #     problem_uuid = submission.problem.uuid

    #     testcases_dir = f"apps/problems/testcases/{problem_uuid}/"
    #     checker_path = os.path.join(testcases_dir, "checker/", "checker.py")
    #     test_results = []
        
    #     for filename in sorted(os.listdir(testcases_dir)):
    #         if filename.endswith(".in"):
    #             test_num = filename.split(".")[0]
    #             input_path = os.path.join(testcases_dir, f"{test_num}.in")
    #             output_path = os.path.join(testcases_dir, f"{test_num}.out")
                
    #             with open(input_path, "r") as f:
    #                 input_data = f.read()
                
    #             with open(output_path, "r") as f:
    #                 expected_output = f.read()
                
    #             with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
    #                 temp_file.write(code)
    #                 temp_file.flush()
    #                 temp_file_path = temp_file.name
                
    #             try:
    #                 start_time = time.perf_counter()
    #                 proc = subprocess.run(
    #                 ["python3", temp_file_path],
    #                 capture_output=True,
    #                 text=True,
    #                 input=input_data,
    #                 timeout=timeout
    #             )
    #                 end_time = time.perf_counter()
    #                 elapsed_time = end_time - start_time
    #                 user_output = proc.stdout
    #                 print("дошел до корректировщика")
    #                 is_correct = self.check_output(user_output, expected_output, checker_path)
                    
    #                 if is_correct:
    #                     status = "AC"
    #                 else:
    #                     status = "WA"
                    
    #                 test_results.append({
    #                     "test": test_num,
    #                     "status": status,
    #                     "stdout": user_output,
    #                     "stderr": proc.stderr,
    #                     "time": elapsed_time
    #                 })         
    #                 print(test_results)          
    #             except subprocess.TimeoutExpired:
    #                 test_results.append({
    #                     "test": test_num,
    #                     "status": "TLE",
    #                     "stdout": "",
    #                     "stderr": "Time Limit Exceeded",
    #                     "time": elapsed_time
    #                 })
    #             except Exception as e:
    #                 test_results.append({
    #                     "test": test_num,
    #                     "status": "ERROR",
    #                     "stdout": "",
    #                     "stderr": str(e),
    #                     "time": elapsed_time
    #                 })
    #             finally:
    #                 os.remove(temp_file_path)
    #         print("done", filename)
    #     return test_results
    
    def __put_run_status(self, submission_id):
        submission = self.model.objects.get(id__exact=submission_id)
        submission.status = self.model.Status.RUNNING
        submission.save()
        print(submission_id, "is running")
        return submission    
    
    
    def run_all_tests(self, submission_id):
        
        submission = self.__put_run_status(submission_id)
        
        code = submission.code
        language = submission.language
        exec_time_ms = submission.exec_time_ms
        uuid = submission.problem.uuid
        
        testcases_dir = f"apps/problems/testcases/{uuid}"
        
        checker_path = os.path.join(testcases_dir, "checker/", "checker.py")
        
        for filename in sorted(os.listdir(testcases_dir)):
            if filename.endswith(".in"):
                test_num = filename.split(".")[0]
                
                input_path = os.path.join(testcases_dir, f"{test_num}.in")
                output_path = os.path.join(testcases_dir, f"{test_num}.out")
                
                with open(input_path, "r") as f:
                    input_data = f.read()
                
                with open(output_path, "r") as f:
                    output_data = f.read()

                
        
        
        
        
    def _check_output(self, user_output, expected_output, checker_path=None):
        if checker_path and os.path.exists(checker_path):
            spec = importlib.util.spec_from_file_location("checker", checker_path)
            checker = importlib.util.module_from_spec(spec) # type: ignore
            spec.loader.exec_module(checker) # type: ignore
            return checker.check(user_output, expected_output)
        else:
            return user_output.strip() == expected_output.strip()
    
