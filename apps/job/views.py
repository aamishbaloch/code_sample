import memory_profiler
import time

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.job.models import Job
from apps.job.serializers import JobSerializer
from apps.job.utils import get_jobs_generator, get_jobs_list


class JobView(ListAPIView):
    """
    View for listing organizations

    **Example requests**:

        GET /jobs/list
    """
    serializer_class = JobSerializer
    queryset = Job.objects.filter(active=True).order_by('id')


class JobRandomIdView(APIView):
    """
    View for listing jobs with a randon JOB ID for each job.
    Main purpose is to show the power of generators in python to do memory efficient operations.

    **Example requests**:

        GET /jobs/random_id
    """
    def get(self, request, format=None):
        memory_before = 'Memory (Before) : {}Mb'.format(memory_profiler.memory_usage())
        t1 = time.clock()
        # jobs = get_jobs_list()
        jobs = get_jobs_generator()
        t2 = time.clock()
        memory_after = 'Memory (After) : {}Mb'.format(memory_profiler.memory_usage())
        time_took = 'Took {} Seconds'.format(t2-t1)

        response = {
            'jobs': jobs,
            'time_took': time_took,
            'memory_before': memory_before,
            'memory_after': memory_after,
        }

        return Response(response, status=status.HTTP_200_OK)
