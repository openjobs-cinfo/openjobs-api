from rest_framework.viewsets import ModelViewSet
from .models import Degree, Job, Skill, DataOrigin, Address, Qualification
from .serializers import DegreeSerializer, JobSerializer, SkillSerializer, DataOriginSerializer, \
    AddressSerializer, QualificationSerializer

class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filterset_fields = {
        'zip_code': ['iexact', 'icontains'],
        'country': ['iexact', 'icontains'],
        'state': ['iexact', 'icontains'],
        'city': ['iexact', 'icontains'],
        'street': ['iexact', 'icontains'],
        'street_number': ['iexact', 'icontains'],
    }


class DegreeViewSet(ModelViewSet):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer
    filterset_fields = {
        'name': ['iexact', 'icontains'],
        'description': ['icontains'],
    }


class QualificationViewSet(ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer
    filterset_fields = {
        'name': ['iexact', 'icontains'],
        'description': ['iexact', 'icontains'],
        'degree_id__name': ['iexact', 'icontains'],
        'degree_id__id': ['iexact'],
    }


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filterset_fields = {
        'name': ['iexact', 'icontains'],
        'description': ['iexact', 'icontains'],
        'origin_id__name': ['iexact', 'icontains'],
        'origin_id__id': ['iexact'],
    }


class JobViewSet(ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filterset_fields = {
        'title': ['iexact', 'icontains'],
        'state': ['iexact', 'icontains'],
        'description': ['iexact', 'icontains'],
        'location': ['iexact', 'icontains'],
        'origin_id__name': ['iexact', 'icontains'],
        'origin_id__id': ['iexact', 'icontains'],
        'skills__id': ['iexact']
    }


class DataOriginViewSet(ModelViewSet):
    queryset = DataOrigin.objects.all()
    serializer_class = DataOriginSerializer
    filterset_fields = {
        'name': ['iexact', 'icontains'],
        'url': ['iexact', 'icontains'],
    }
