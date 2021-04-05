from django.db.models.query import QuerySet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
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
        'description': ['icontains'],
        'institution': ['iexact', 'icontains'],
        'time_course': ['iexact'],
        'degree_id__name': ['iexact', 'icontains'],
        'degree_id__id': ['iexact'],
    }


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filterset_fields = {
        'name': ['iexact', 'icontains'],
        'description': ['icontains'],
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


class JobRecommendationViewSet(GenericViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.all()
        return queryset

    def get_recommended_jobs(self, user):
        user_skills = user.skills.all()
        recommended_jobs = QuerySet(model=Job)
        for skill in user_skills:
            recommended_jobs = recommended_jobs | skill.jobs.all()
        recommended_jobs = recommended_jobs.distinct()
        return recommended_jobs

    @action(methods=["get"], detail=False, url_path="recommended_jobs")
    def recommended_jobs_paginated(self, request):
        user = request.user
        jobs = self.get_recommended_jobs(user)
        page = self.paginate_queryset(jobs)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=["get"], detail=False, url_path="recommended_jobs/skill_percents")
    def jobs_percent_by_skills(self, request):
        user = request.user
        jobs = self.get_recommended_jobs(user)
        percents = dict()
        for skill in user.skills.all():
            percents[skill.name] = jobs.filter(skills__id=skill.id).count()
        total = sum([n for n in percents.values()])
        for skill in percents.items():
            percents[skill[0]] = round(skill[1] / total * 100, 2)
        return Response(percents)
