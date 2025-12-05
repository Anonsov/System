import tempfile
import os # type: ignore
import subprocess
import importlib.util
import time


class Runner:
    def __init__(self, model):
        self.model = model
    
    def run_all_tests(self, submission_id):
        
        submission = self.model.objects.get(id__exact=submission_id)
        submission.status = self.model.Status.RUNNING
        submission.save()
        print(submission_id, "is running")
        
        code = submission.code
        language = submission.language
        exec_time_ms = submission.exec_time_ms
        time_limit_ms = submission.problem.time_limit_ms
        uuid = submission.problem.uuid
        
        testcases_dir = f"apps/problems/testcases/{uuid}"
        
        checker_path = os.path.join(testcases_dir, "checker/", "checker.py")
        
        test_results = []
        
        testcases_dir = os.path.join(testcases_dir, "tests")
        directories = sorted(os.listdir(testcases_dir))
        
        solved_count = 0
        overall_result = {}
        
        found_TLE = False
        found_WA = False
        found_CE = False
        max_elapsed_time = 0
        
        for filename in directories:
            if filename.endswith(".in"):
                test_num = filename.split(".")[0]
                
                input_path = os.path.join(testcases_dir, f"{test_num}.in")
                output_path = os.path.join(testcases_dir, f"{test_num}.out")
                
                with open(input_path, "r") as f:
                    input_data = f.read()
                
                with open(output_path, "r") as f:
                    expected_output = f.read()
                
                with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
                    temp_file.write(code)
                    temp_file.flush()
                    temp_file_path = temp_file.name
                    
                try:
                    start_time = time.perf_counter()
                    print("захожу в субпроцесс")
                    proc = subprocess.run(
                        ["python3", temp_file_path],
                        input=input_data,
                        capture_output=True,
                        text=True,
                        timeout=time_limit_ms/1000
                    )
                    print("вышел из субпроцесса", proc.stderr)
                    end_time = time.perf_counter()
                    elapsed_time = end_time - start_time
                    user_output = proc.stdout
                    print("ВОЗВРАЩАЕТ", proc.returncode)
                    print(user_output, "АУТПУТ ЮЗЕРА")
                    if proc.returncode != 0:
                        test_results.append({
                            "test": test_num,
                            "status": "CE",
                            "stdout": user_output,
                            "stderr": proc.stderr,
                            "time": elapsed_time
                        })
                        found_CE = True
                        continue  

                    is_correct = self._check_output(user_output, expected_output, checker_path)   
                    
                    if is_correct:
                        status = "AC"
                        if not found_WA and not found_TLE and not found_CE:
                            solved_count += 1
                            max_elapsed_time = max(elapsed_time, max_elapsed_time)
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
                    # print(test_results)
                
                except subprocess.TimeoutExpired:
                    test_results.append({
                        "test": test_num,
                        "status": "TLE",
                        "stdout": "",
                        "stderr": "Time Limit Exceeded",
                        "time": elapsed_time
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
                    os.remove(temp_file_path)
                print("done", filename)
        print(found_CE, found_TLE, found_WA)
        if found_CE:
            overall_result = {
                'status': "CE",
                "exec_time_ms": max_elapsed_time,
                "test_results": test_results,
                "score": solved_count
            }
            
        elif found_TLE:
            overall_result = {
                'status': "TLE",
                "exec_time_ms": max_elapsed_time,
                "test_results": test_results,
                "score": solved_count
            }
        elif found_WA: 
            overall_result = {
                'status': "WA",
                "exec_time_ms": max_elapsed_time,
                "test_results": test_results,
                "score": solved_count
            }
        else:
            overall_result = {
                'status': "AC",
                "exec_time_ms": max_elapsed_time,
                "test_results": test_results,
                "score": solved_count
            }
        return overall_result
                  
    
                       
    def _check_output(self, user_output, expected_output, checker_path=None):
        if checker_path and os.path.exists(checker_path):
            spec = importlib.util.spec_from_file_location("checker", checker_path)
            checker = importlib.util.module_from_spec(spec) # type: ignore
            spec.loader.exec_module(checker) # type: ignore
            return checker.check(user_output, expected_output)
        else:
            return user_output.strip() == expected_output.strip()
    
