from django.contrib import admin
from .models import User, Airport, Flight, Person

admin.site.register(User)
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Person)
