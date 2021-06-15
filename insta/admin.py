from django.contrib import admin
from . import models
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Saved)