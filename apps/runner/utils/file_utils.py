import os
FILE_PATH_PROBLEMS_TESTCASES = "apps/problems"

def get_folder_submission_id(submission_id: str):
    file_path = os.path.join(FILE_PATH_PROBLEMS_TESTCASES, "testcases", submission_id)
    return file_path


