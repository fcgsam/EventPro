from django.contrib import admin

# Register your models here.
from .models import *
from userAcc.models import *

# Register your models here.
admin.site.register(Event)
admin.site.register(Task)
admin.site.register(CustomUser)
admin.site.register(Attendee)