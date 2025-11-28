from abc import ABC, abstractmethod
import subprocess
import tempfile

class BaseRunner(ABC):
    @abstractmethod
    def run(self, submission_id, code: str, input_data: str):
        """_summary_

        Run the code
        then i should return: {
            stdout: ...
            stderr: ...
            exit_code: ...
        }
        """
        pass
    

class BaseChecker(ABC):
    @abstractmethod
    def checker(self, expected, actual) -> bool:
        """
        there i will just check the expected and actual data
        and also implement the checker.py that i upload while
        creating the problem itself
        i will import it there and push the checker and just return
        bool value
        """
        pass
    
    
class BaseExecutor(ABC):
    @abstractmethod
    def execute_submission(self, submission_id):
        """
        there i will just execute the submission
        i think just from the word "execute", everything is defined
        """
        pass
    
# class LocalRunner(BaseRunner):
#     def run(self, submission_id, code: str, input_data: str):
#         with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
#             f.write(code.encode())
#             f.flush()
            
#             result = subprocess.run(
#                 ["python3", f.name],
#                 input=input_data.encode(),
#                 capture_output=True,
#                 timeout=2
#             )
            
#             return {
#                 "stdout": result.stdout.decode(),
#                 "stderr": result.stderr.decode(),
#                 "exit_code": result.returncode
#             }