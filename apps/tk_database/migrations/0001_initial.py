# Generated by Django 4.1.4 on 2022-12-22 13:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GeoRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Hike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField(blank=True, choices=[(1, 'Первая'), (2, 'Вторая'), (3, 'Третья'), (4, 'Четвертая'), (5, 'Пятая'), (6, 'Шестая')], default=None, null=True)),
                ('sub_category', models.IntegerField(blank=True, choices=[(1, 'с эл. 1'), (2, 'с эл. 2'), (3, 'с эл. 3'), (4, 'с эл. 4'), (5, 'с эл. 5'), (6, 'с эл. 6')], default=None, null=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.FilePathField(blank=True, default=None, null=True, path='/img')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_completed', models.BooleanField()),
                ('is_private', models.BooleanField()),
                ('GeoRegion', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, to='tk_database.georegion')),
                ('instructor', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='hike_instructor', to=settings.AUTH_USER_MODEL)),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='hike_leader', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HikeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(choices=[('M', 'Муж.'), ('F', 'Жен.'), ('U', 'Неизвестен')], default='U', max_length=1)),
                ('birthday', models.DateField(blank=True, default=None, null=True)),
                ('phone_home', models.CharField(blank=True, default=None, max_length=32, null=True)),
                ('phone_mobile', models.CharField(blank=True, default=None, max_length=32, null=True)),
                ('phone_relative', models.CharField(blank=True, default=None, max_length=32, null=True)),
                ('employment', models.CharField(choices=[('unemployed', 'Безработный(-ая)'), ('employed', 'Трудоустроен(-а)'), ('student', 'Студент(-ка)'), ('unknown', 'Неизвестно')], default='unknown', max_length=32)),
                ('work_place', models.CharField(blank=True, default=None, max_length=1024, null=True)),
                ('sports_category', models.CharField(blank=True, choices=[('3', 'Третья'), ('2', 'Вторая'), ('1', 'Первая'), ('KMS', 'КМС'), ('MASTER', 'Мастер спорта')], default=None, max_length=32, null=True)),
                ('sports_category_expiration_date', models.DateField(blank=True, default=None, null=True)),
                ('max_height', models.IntegerField(default=0)),
                ('max_camp_height', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HikeReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual_start_date', models.DateField()),
                ('actual_end_date', models.DateField()),
                ('actual_path', models.TextField()),
                ('report_file', models.FilePathField(path='/report')),
                ('report_url', models.URLField()),
                ('hike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tk_database.hike')),
            ],
        ),
        migrations.CreateModel(
            name='HikeMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=255)),
                ('hike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tk_database.hike')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='hike',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tk_database.hiketype'),
        ),
    ]
