from rest_framework.generics import ListCreateAPIView

from apps.job.models import Job
from apps.organization.models import Organization
from apps.organization.serializers import OrganizationSerializer


class OrganizationView(ListCreateAPIView):
    """
    View for creating and listing organizations
    Returns organizations with the count of all active jobs

    **Example requests**:

        GET /organizations/
    """
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        active_jobs = {}
        organization_jobs = Job.objects.filter(active=True).values_list('organization_id', 'id')
        [active_jobs.setdefault(organization_id, []).append(id) for (organization_id, id) in organization_jobs]
        self.request.active_jobs = active_jobs
        return Organization.objects.filter(active=True).order_by('id')

    def get_serializer_context(self):
        return {'request': self.request}

