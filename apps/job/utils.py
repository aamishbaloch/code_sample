from apps.job.models import Job
from libs.utils import get_random_int


def get_jobs_list():
    jobs = []
    for job in Job.objects.all():
        jobs.append({
            'title': job.title,
            'rnadom_id': get_random_int(),
        })
    return jobs


def get_jobs_generator():
    for job in Job.objects.all():
        job_updated = {
            'title': job.title,
            'rnadom_id': get_random_int(),
        }
        yield job_updated
