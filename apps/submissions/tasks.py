from celery import shared_task

@shared_task(bind=True, queue="judge", acks_late=True)
def judge_submission(self, submission_id: int):
    from apps.submissions.models import Submission
    from apps.runner.base import Runner

    runner = Runner(Submission)
    return runner.run_all_tests(submission_id)
