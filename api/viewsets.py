from rest_framework.viewsets import ModelViewSet
from .models import Degree, Job, Skill, DataOrigin, Address, Qualification
from .serializers import DegreeSerializer, JobSerializer, SkillSerializer, DataOriginSerializer, \
    AddressSerializer, QualificationSerializer


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class DegreeViewSet(ModelViewSet):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer


class QualificationViewSet(ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class JobViewSet(ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class DataOriginViewSet(ModelViewSet):
    queryset = DataOrigin.objects.all()
    serializer_class = DataOriginSerializer
