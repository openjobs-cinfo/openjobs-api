from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from .managers import CustomUserManager


class Address(models.Model):
    class Meta:
        db_table = 'address'

    zip_code = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    street_number = models.CharField(max_length=20)


class Degree(models.Model):
    class Meta:
        db_table = 'degree'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Qualification(models.Model):
    class Meta:
        db_table = 'qualification'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    degree_id = models.ForeignKey(Degree, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class DataOrigin(models.Model):
    class Meta:
        db_table = 'data_origin'

    name = models.CharField(max_length=255)
    url = models.TextField(blank=True, null=True)


class Skill(models.Model):
    class Meta:
        db_table = 'skill'

    original_id = models.IntegerField()
    url = models.CharField(max_length=1000)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    origin_id = models.ForeignKey(DataOrigin, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Job(models.Model):
    class Meta:
        db_table = 'job'

    original_id = models.IntegerField()
    url = models.CharField(max_length=1000)
    number = models.IntegerField()
    title = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    created_at = models.DateField()
    closed_at = models.DateField()
    description = models.TextField()
    location = models.CharField(max_length=1000)
    origin_id = models.ForeignKey(DataOrigin, on_delete=models.RESTRICT)
    skills = models.ManyToManyField(Skill, related_name='jobs')

    def __str__(self):
        return self.title


class User(AbstractUser):
    class Meta:
        db_table = 'sysuser'

    username = None
    first_name = None
    last_name = None
    email = models.EmailField('email', unique=True)
    name = models.CharField(max_length=255)
    avatar_url = models.CharField(max_length=1000, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    address_id = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill, related_name='skilled_users')
    qualifications = models.ManyToManyField(Qualification, related_name='qualified_users')

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password']

    objects = CustomUserManager()

    def get_full_name(self):
        return self.name.strip()

    def get_short_name(self):
        short_name = self.name.strip().split(' ')
        short_name = f'{short_name[0]} {short_name[-1]}'
        return short_name

    def __str__(self):
        return self.email
