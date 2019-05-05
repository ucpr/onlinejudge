from django.contrib import admin
from .models import Contest, Problem, Submittion

# Register your models here.
admin.site.register(Contest)
admin.site.register(Problem)
admin.site.register(Submittion)
