from rest_framework import serializers

from apps.organization.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    active_jobs = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        exclude = ('created', 'modified')

    def __init__(self, *args, **kwargs):
        super(OrganizationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.query_params.get('fields'):
            fields = request.query_params.get('fields')
            if fields:
                fields = fields.split(',')
                allowed = set(fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)

    def get_active_jobs(self, obj):
        if obj.id in self.context['request'].active_jobs:
            return len(self.context['request'].active_jobs[obj.id])
        return 0
