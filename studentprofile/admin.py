from django.contrib import admin
from studentprofile.models import profile, UserProfile, Githubmodel, TeamTreeHousemodel, Codewarsmodel, CodeCademymodel, stacklistmodel

admin.site.register(profile)
admin.site.register(UserProfile)
admin.site.register(Githubmodel)
admin.site.register(stacklistmodel)
admin.site.register(CodeCademymodel)
admin.site.register(Codewarsmodel)
