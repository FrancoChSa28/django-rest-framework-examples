# Generated by Django 3.2.5 on 2023-08-24 03:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Name')),
                ('zip_code', models.CharField(max_length=50, verbose_name='zip_code')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'City',
                'db_table': 'tbl_cities',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PetCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, default='', max_length=5000, null=True, verbose_name='Description')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
            options={
                'verbose_name': 'Pet Category',
                'verbose_name_plural': 'Pet Category',
                'db_table': 'tbl_pet_categories',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, default='', max_length=5000, null=True, verbose_name='Description')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tag',
                'db_table': 'tbl_tags',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('description', models.TextField(blank=True, default='', max_length=5000, null=True, verbose_name='Description')),
                ('photoUrls', models.FileField(upload_to='pets/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])),
                ('status', models.IntegerField(choices=[(1, 'available'), (2, 'pending'), (3, 'sold')], default=1)),
                ('latitude', models.CharField(blank=True, max_length=64, null=True)),
                ('longitude', models.CharField(blank=True, max_length=64, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=20, null=True)),
                ('mailing_address', models.CharField(blank=True, max_length=255, null=True)),
                ('facebook', models.URLField(blank=True, max_length=255, null=True)),
                ('twitter', models.URLField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pets.petcategory')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pets.city')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pets', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, null=True, to='pets.Tag')),
            ],
            options={
                'verbose_name': 'Pet',
                'verbose_name_plural': 'Pet',
                'db_table': 'tbl_pets',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(verbose_name='quantity')),
                ('shipDate', models.DateField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'placed'), (2, 'approved'), (3, 'delivered')], default=1)),
                ('complete', models.BooleanField(default=False, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pets.pet')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Order',
                'db_table': 'tbl_orders',
                'ordering': ('created_at',),
            },
        ),
    ]
