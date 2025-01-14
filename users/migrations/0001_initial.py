# Generated by Django 5.1.4 on 2025-01-14 04:29

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('contact_details', models.TextField()),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('links', models.URLField(validators=[django.core.validators.URLValidator()])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('ADMIN', 'Administrator'), ('SALES', 'Sales'), ('PRESALES', 'Presales'), ('VIEWER', 'Viewer')], default='VIEWER', max_length=20)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('department', models.CharField(blank=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=100)),
                ('link', models.URLField(validators=[django.core.validators.URLValidator()])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='users.customer')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(choices=[('P1', 'P1 - Critical'), ('P2', 'P2 - High'), ('P3', 'P3 - Medium')], max_length=20)),
                ('bandwidth', models.CharField(default='100Mbps', max_length=100)),
                ('gateway', models.CharField(choices=[('JAV', 'JAV'), ('SUB', 'SUB'), ('BHI', 'BHI'), ('PAK', 'PAK')], default='JAV', max_length=20)),
                ('terminal_count', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('terminal_type', models.CharField(choices=[('1m2_3W_MDM2510', '1m2 3W MDM2510'), ('1m8_5W_MDM2510', '1m8 5W MDM2510'), ('2m4_8W_MDM2510', '2m4 8W MDM2510')], default='1m2_3W_MDM2510', max_length=50)),
                ('customer', models.CharField(max_length=200)),
                ('sales_director', models.CharField(max_length=200)),
                ('presales_owner', models.EmailField(default='admin@example.com', max_length=254)),
                ('submission_date', models.DateField()),
                ('proposal_link', models.URLField(default='https://example.com', validators=[django.core.validators.URLValidator()])),
                ('commercial_value', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.CharField(choices=[('ONGOING', 'Ongoing'), ('BLOCKED', 'Blocked'), ('CLOSED', 'Closed')], default='ONGOING', max_length=20)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(help_text='Select the project this proposal belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to='users.project')),
            ],
            options={
                'ordering': ['-submission_date'],
                'permissions': [('can_view_all_proposals', 'Can view all proposals'), ('can_edit_all_proposals', 'Can edit all proposals')],
            },
        ),
    ]
