from rest_framework.serializers import ModelSerializer
from .models import Degree, Job, Skill, DataOrigin, Address, Qualification, User


class DegreeSerializer(ModelSerializer):
    class Meta:
        model = Degree
        fields = ('id', 'name', 'description')


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'zip_code', 'country', 'state', 'city', 'street', 'street_number')


class QualificationSerializer(ModelSerializer):
    class Meta:
        model = Qualification
        fields = ('id', 'name', 'description', 'degree_id')


class SkillRelationSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')


class DataOriginSerializer(ModelSerializer):
    class Meta:
        model = DataOrigin
        fields = ('id', 'name', 'url')


class DataOriginRelationSerializer(ModelSerializer):
    class Meta:
        model = DataOrigin
        fields = ('id', 'name')


class JobSerializer(ModelSerializer):
    skills = SkillRelationSerializer(many=True, read_only=True)
    origin_id = DataOriginRelationSerializer(read_only=True)

    class Meta:
        model = Job
        fields = (
            'id', 'original_id', 'url', 'number', 'title', 'state', 'created_at', 'closed_at', 'description',
            'location', 'origin_id', 'skills'
        )


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'original_id', 'url', 'name', 'color', 'description', 'origin_id')


class UserSerializer(ModelSerializer):
    skills = SkillRelationSerializer(many=True, read_only=True)
    qualifications = QualificationSerializer(many=True, read_only=True)

    class Meta:
        ref_name = 'User'
        model = User
        fields = ('id', 'email', 'name', 'avatar_url', 'address_id', 'birth_date', 'skills', 'qualifications')


class UserCreationSerializer(ModelSerializer):
    class Meta:
        ref_name = 'UserCreation'
        model = User
        fields = (
            'id', 'email', 'name', 'password', 'avatar_url', 'address_id', 'birth_date', 'skills', 'qualifications'
        )

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
