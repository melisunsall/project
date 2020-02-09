from django.contrib import admin
from .models import Intern,Advisor,Appointment,Department,UserProfile,Comment ,File
# Register your models here.

admin.site.register(Intern)
admin.site.register(Advisor)
admin.site.register(Department)
admin.site.register(UserProfile)
admin.site.register(Appointment)
admin.site.register(Comment)
admin.site.register(File)
