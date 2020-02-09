# Generated by Django 2.0.13 on 2019-08-22 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_remove_appointment_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('intern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Intern')),
            ],
        ),
        migrations.AlterField(
            model_name='appointment',
            name='intern',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='forum.Intern'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
