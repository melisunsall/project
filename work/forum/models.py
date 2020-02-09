from __future__ import unicode_literals
import datetime
from datetime import timezone, timedelta
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .validators import validate_file_extension


# Create your models here
class Department(models.Model):
    department_name = models.CharField(max_length=250)
    dep_logo = models.FileField()

    def __str__(self):
        return self.department_name

    def get_absolute_url(self):
        return reverse('forum:detail', kwargs={'pk': self.pk})


class Advisor(models.Model):
    user = models.OneToOneField(
        User,
        default=None,
        null=True,
        on_delete=models.CASCADE)
    advisor_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=250)
    advisor_department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('forum:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.advisor_name


class Intern(models.Model):
    Rating_CHOICES = (
        (1, 'Poor'),
        (2, 'Average'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent')
    )
    technical_skills = models.IntegerField(choices=Rating_CHOICES, default=1)
    experience = models.IntegerField(choices=Rating_CHOICES, default=1)
    team_work = models.IntegerField(choices=Rating_CHOICES, default=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    app_date = models.DateTimeField('date applied', auto_now_add=True, blank=True)
    votes = models.IntegerField(default=0)
    is_favourite = models.BooleanField(default=False)
    is_accepted = models.IntegerField(default=0)
    profile_photo = models.ImageField(default="default-picture_0_0.png", null=True, blank=True)
    inter_date = models.DateField(
        max_length=10,
        help_text="format : YYYY-MM-DD",
        null=True)
    resume = models.FileField(validators=[validate_file_extension])

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('forum:interns')




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default-picture_0_0.png', null=True, blank=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    intern = models.OneToOneField(Intern, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    complete = models.BooleanField(default=False)

    def __str__(self):
        if self.intern.is_accepted == 0:
            url = reverse('forum:intern', args=(self.intern.id,))
            return f'Appointment with <a href="{url}">{self.intern.name}  </a> <strong> {self.user.username}<strong>'
        else:
            return f'Interview with {self.intern.name} has done.'

    def get_absolute_url(self):
        return reverse('forum:calendar')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    text = models.TextField(max_length=160)
    like = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.text} --by{self.user.username}'


class File(models.Model):
    file = models.FileField()
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
