from django.contrib import admin
from .models import Contest, Problem, Submittion, RegistContestUser

# Register your models here.
admin.site.register(Contest)
admin.site.register(Problem)
admin.site.register(Submittion)
admin.site.register(RegistContestUser)
