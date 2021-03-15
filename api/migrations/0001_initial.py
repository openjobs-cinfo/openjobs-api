# Generated by Django 3.1.7 on 2021-03-10 14:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_code', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=255)),
                ('street_number', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='DataOrigin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'data_origin',
            },
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'degree',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_id', models.IntegerField()),
                ('url', models.CharField(max_length=1000)),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('origin_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.dataorigin')),
            ],
            options={
                'db_table': 'skill',
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('degree_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.degree')),
            ],
            options={
                'db_table': 'qualification',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_id', models.IntegerField()),
                ('url', models.CharField(max_length=1000)),
                ('number', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=50)),
                ('created_at', models.DateField()),
                ('closed_at', models.DateField()),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=1000)),
                ('origin_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='api.dataorigin')),
                ('skills', models.ManyToManyField(related_name='jobs', to='api.Skill')),
            ],
            options={
                'db_table': 'job',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('name', models.CharField(max_length=255)),
                ('avatar_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('address_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('qualifications', models.ManyToManyField(related_name='qualified_users', to='api.Qualification')),
                ('skills', models.ManyToManyField(related_name='skilled_users', to='api.Skill')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'sysuser',
            },
        ),
    ]