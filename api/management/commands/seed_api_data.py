from django.core.management.base import BaseCommand, CommandError
from django_seed import Seed
from api.models import User, Skill, Qualification, Job, Degree, Address, DataOrigin
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Run custom data seeds.'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--model', nargs='+', help='', type=str)
        parser.add_argument('-n', '--number', help='defines the number of data to be seeded', type=int, default=5)

    def run_address_seed(self, seeder, options):
        return seeder.add_entity(Address, options['number'], {
            'zip_code': lambda x: seeder.faker.postcode(),
            'country': lambda x: seeder.faker.country(),
            'state': lambda x: seeder.faker.state(),
            'city': lambda x: seeder.faker.city(),
            'street': lambda x: seeder.faker.street_name(),
            'street_number': lambda x: seeder.faker.building_number(),
        })

    def run_degree_seed(self, seeder, options):
        degrees = ['Médio', 'Técnico', 'Superior', 'Pós-graduação', 'Mestrado', 'Doutorado', 'Escola']
        degree_generator = (degree for degree in degrees)
        ids = seeder.add_entity(Degree, len(degrees), {'name': lambda x: degree_generator.__next__()})
        return ids

    def run_qualification_seed(self, seeder, options):
        degree_ids = Degree.objects.all().values_list('id', flat=True)
        return seeder.add_entity(Qualification, options['number'], {
            'name': lambda x: seeder.faker.job(),
            'degree_id': lambda x: Degree.objects.get(id=seeder.faker.random_element(elements=degree_ids))
        })

    def run_dataorigin_seed(self, seeder, options):
        return seeder.add_entity(DataOrigin, options['number'], {
            'name': lambda x: seeder.faker.company(),
            'url': lambda x: seeder.faker.url()
        })

    def run_skill_seed(self, seeder, options):
        data_origin_ids = DataOrigin.objects.all()
        return seeder.add_entity(Skill, options['number'], {
            'name': lambda x: seeder.faker.pystr(max_chars=20),
            'url': lambda x: seeder.faker.url(),
            'color': lambda x: seeder.faker.color(),
            'origin_id': lambda x: seeder.faker.random_element(data_origin_ids)
        })

    def run_job_seed(self, seeder, options):
        data_origin_ids = DataOrigin.objects.all()
        return seeder.add_entity(Job, options['number'], {
            'title': lambda x: seeder.faker.job(),
            'url': lambda x: seeder.faker.url(),
            'state': lambda x: seeder.faker.state(),
            'created_at': lambda x: seeder.faker.date(),
            'closed_at': lambda x: seeder.faker.date(),
            'origin_id': lambda x: seeder.faker.random_element(data_origin_ids)
        })

    def run_user_seed(self, seeder, options):
        addresses = Address.objects.all()
        if not addresses:
            self.run_address_seed(seeder, {'number': 1})
            addresses = Address.objects.all()

        return seeder.add_entity(User, options['number'], {
            'email': lambda x: seeder.faker.email(),
            'name': lambda x: seeder.faker.name(),
            'avatar_url': lambda x: seeder.faker.url(),
            'birth_date': lambda x: seeder.faker.date(),
            'password': lambda x: make_password("123456789"),
            'address_id': lambda x: seeder.faker.random_element(addresses),
            'last_login': lambda x: None,
            'is_superuser': lambda x: 0,
            'is_staff': lambda x: 0,
        })

    def handle(self, *args, **options):
        mapping = {
            'address': self.run_address_seed,
            'degree': self.run_degree_seed,
            'qualification': self.run_qualification_seed,
            'dataorigin': self.run_dataorigin_seed,
            'skill': self.run_skill_seed,
            'job': self.run_job_seed,
            'user': self.run_user_seed,
        }

        seeder = Seed.seeder(locale='pt_BR')

        if not options['model']:
            for model in mapping.values():
                model(seeder, options)
        else:
            for model in options['model']:
                try:
                    mapping[model.lower()](seeder, options)
                except KeyError:
                    self.stderr(f"{model} model not found")

        pks = seeder.execute()

        if User in pks:
            pk_new_users = pks[User]
            all_skills = list(Skill.objects.all())
            all_qualifications = list(Qualification.objects.all())
            for pk_user in pk_new_users:
                user = User.objects.get(id=pk_user)

                # Adding User Skills
                user_skills = seeder.faker.random_elements(
                    all_skills,
                    length=seeder.faker.random_int(min=0, max=len(all_skills)),
                    unique=True
                )
                user.skills.set(list(user_skills))

                # Adding User Qualifications
                max_qualifications = 3 if len(all_qualifications) >= 3 else len(all_qualifications)
                user_qualifications = seeder.faker.random_elements(
                    all_qualifications,
                    length=seeder.faker.random_int(min=0, max=max_qualifications),
                    unique=True
                )
                user.qualifications.set(list(user_qualifications))
