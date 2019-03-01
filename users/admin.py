from django.contrib import admin
from users.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'photo',
        'account'
    ]


admin.site.register(Profile, ProfileAdmin)

