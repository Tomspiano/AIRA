from django.contrib import admin
from . import Airplane,models


admin.site.register(Airplane.airplane)
admin.site.register(Airplane.Ticket)
admin.site.register(Airplane.flight)
admin.site.register(Airplane.company)
admin.site.register(models.Tickets)
# Register your models here.
