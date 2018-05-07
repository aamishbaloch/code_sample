from rest_framework.generics import ListAPIView

from apps.job.models import Job
from apps.job.serializers import JobSerializer


class JobView(ListAPIView):
    """
    View for listing organizations

    **Example requests**:

        GET /jobs/list
    """
    serializer_class = JobSerializer
    queryset = Job.objects.filter(active=True).order_by('id')

